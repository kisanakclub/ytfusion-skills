#!/usr/bin/env python3
"""Capture native channel-stats with synthetic data; never start the app or Google.

Requires Jinja2, Playwright and a local Chart.js 4.4.0 UMD file. All browser
requests are intercepted. Only templates/static files and two pure report
modules from the supplied source checkout are read; no app/config/auth import.
"""
import argparse
import asyncio
from datetime import date, datetime, timedelta, timezone
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlparse

from jinja2 import Environment, FileSystemLoader
from playwright.async_api import async_playwright

SOURCE_FILES = (
    'src/templates/base.html', 'src/templates/channel_statistics.html',
    'src/templates/partials/channel_publishing.html',
    'src/static/css/channel_publishing.css', 'src/static/js/channel_publishing.js',
    'src/static/js/hds_time.js', 'src/channel_analytics.py', 'src/channel_publishing.py',
)
NOW = datetime(2026, 11, 27, 5, tzinfo=timezone.utc)
sys.dont_write_bytecode = True


def module(source, name):
    spec = importlib.util.spec_from_file_location(name, source / 'src' / (name + '.py'))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def fixtures(source):
    analytics = module(source, 'channel_analytics')
    publishing = module(source, 'channel_publishing')
    channels, publications = [], []
    start, end = date(2026, 9, 1), date(2026, 11, 25)
    for index, (name, title, color) in enumerate((
        ('Aurora_Studio', 'Aurora Studio', '#34d399'),
        ('Quiet_Atlas', 'Quiet Atlas', '#60a5fa'),
        ('Paper_Garden', 'Paper Garden', '#c084fc'),
    )):
        rows = [[(start + timedelta(days=day)).isoformat(),
                 round(1200 + index * 600 + day * 12 + 400 * math.sin(day / 5 + index))]
                for day in range((end - start).days + 1)]
        views = analytics.daily_report(rows, start, end)
        earnings = analytics.daily_report([[day, 0 if index == 1 and day == end.isoformat()
                                            else round(value * .0021, 2)] for day, value in rows], start, end)
        earnings['periods'] = analytics.earnings_months(earnings, NOW.date())
        watch_start = end - timedelta(days=364)
        watch = analytics.daily_report([[(watch_start + timedelta(days=day)).isoformat(),
                                        (1200 + index * 600) * 4.2] for day in range(365)], watch_start, end)
        paired = dict(earnings, basis_values={'views': views['values'],
                                            'engagedViews': [int(value * .7) for value in views['values']]})
        report = dict(report_version=2, report_timezone='America/Los_Angeles', currency='USD',
                      fetched_at=NOW.isoformat(), reports=dict(views=views, earnings=earnings, watch_time=watch,
                      rpm=analytics.rpm_report(paired, 'views'), rpm_engaged=analytics.rpm_report(paired, 'engagedViews')),
                      chart_labels=views['dates'], chart_values=views['values'],
                      earnings_chart_labels=earnings['dates'], earnings_chart_values=earnings['values'],
                      watch_hours_365d=round(watch['available_total'] / 60),
                      earnings_this_month=earnings['periods']['this_month']['value'],
                      earnings_last_month=earnings['periods']['last_month']['value'])
        for metric, data in (('views', views), ('earnings', earnings)):
            report.update({metric + '_' + key: value for key, value in data['totals'].items()})
            report[metric + '_available'] = data['available_total']
        if index == 2:
            # Explicit permission state alongside nonzero and zero-capable reports.
            for key in ('earnings', 'rpm', 'rpm_engaged'):
                report['reports'][key] = {'status': 'permission_required', 'error': 'Enable earnings access',
                                          'dates': [], 'values': []}
            for key in list(report):
                if key.startswith('earnings_'):
                    report[key] = [] if key.endswith(('labels', 'values')) else None
        channels.append(dict(internal_name=name, title=title, channel_id='UC_SYNTHETIC_' + str(index),
                             custom_url='@' + name.lower(), thumbnail_url='/avatar-' + str(index) + '.svg',
                             subscriber_count=[12400, 5800, 740][index], video_count=[87, 42, 18][index],
                             is_monetized=[True, True, None][index], analytics=report))
        videos = []
        for day in range(8):
            stamp = (NOW - timedelta(days=2 + day * (index + 2))).replace(hour=12, minute=day % 3 * 15)
            videos.append(dict(video_id='synthetic-public-' + str(day), title='Example published video',
                               published_at=stamp.isoformat(), privacy='public'))
        for day in range(2 if index != 1 else 0):
            stamp = (NOW + timedelta(days=2 + day * 3)).replace(hour=12, minute=30)
            videos.append(dict(video_id='synthetic-scheduled-' + str(day),
                               title=['A Quiet Morning in the Studio', 'Small Spaces, Thoughtful Details'][day],
                               publish_at=stamp.isoformat(), published_at=NOW.isoformat(), privacy='private'))
        publications.append(publishing.summarize(dict(internal_name=name, title=title,
            thumbnail_url='/avatar-' + str(index) + '.svg', status='available', checked_at=NOW.isoformat(),
            videos=videos, scanned_videos=50, complete=False, next_page_token='synthetic-next'), now=NOW))
    return channels, publications


async def capture(args):
    source, output = args.source.resolve(), args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    for relative in SOURCE_FILES:
        if not (source / relative).is_file():
            raise ValueError('Required native source missing: ' + relative)
    html = Environment(loader=FileSystemLoader(source / 'src/templates')).get_template('channel_statistics.html').render(
        url_path=lambda path: path, root_path='', url_for=lambda *a, **kw: '/',
        get_flashed_messages=lambda request: [], request={'app': {'state': {}}}, username='UI reference',
        installation_device=lambda: 'local', dashboard_home=lambda request: '/')
    channels, publications = fixtures(source)
    errors, writes = [], []
    async with async_playwright() as playwright:
        options = {'headless': True}
        if args.browser:
            options['executable_path'] = str(args.browser)
        browser = await playwright.chromium.launch(**options)
        page = await browser.new_page(viewport={'width': 1600, 'height': 1000}, device_scale_factor=1)
        page.on('pageerror', lambda error: errors.append(str(error)))
        await page.clock.install(time=NOW)
        await page.add_init_script("localStorage.setItem('theme','dark-mode'); localStorage.setItem('sidebarCollapsed','true');")

        async def route(request):
            parsed = urlparse(request.request.url)
            path = parsed.path
            if request.request.method != 'GET':
                writes.append(path)
                await request.fulfill(status=405, json={'detail': 'Synthetic reference is read-only'})
            elif path.endswith('/chart.umd.min.js'):
                await request.fulfill(path=str(args.chart_js.resolve()), content_type='application/javascript')
            elif parsed.hostname != 'reference.invalid':
                await request.fulfill(status=204, body='')
            elif path == '/channel-stats':
                await request.fulfill(content_type='text/html', body=html)
            elif path.startswith('/static/'):
                asset = (source / 'src' / path.lstrip('/')).resolve()
                if asset.is_relative_to(source / 'src/static') and asset.is_file():
                    await request.fulfill(path=str(asset))
                else:
                    await request.fulfill(status=404, body='')
            elif path.startswith('/avatar-'):
                color = ['#34d399', '#60a5fa', '#c084fc'][int(path[8])]
                svg = '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40"><rect width="40" height="40" rx="10" fill="' + color + '"/><circle cx="20" cy="20" r="9" fill="#153331"/></svg>'
                await request.fulfill(content_type='image/svg+xml', body=svg)
            elif path == '/api/channel-statistics':
                await request.fulfill(json=dict(success=True, channels=channels, last_updated=NOW.isoformat()))
            elif path == '/api/channel-publishing':
                await request.fulfill(json=dict(success=True, channels=publications))
            elif path == '/api/categories':
                await request.fulfill(json={'categories': [{'name': 'Studio', 'count': 2}, {'name': 'Music', 'count': 1}]})
            elif path == '/api/status':
                await request.fulfill(json={row['internal_name']: {'category': 'Music' if i == 1 else 'Studio', 'batches': {}}
                                           for i, row in enumerate(channels)})
            else:
                await request.fulfill(json={'success': True})

        await page.route('**/*', route)
        await page.goto('http://reference.invalid/channel-stats')
        await page.locator('#statsTableBody tr').nth(2).wait_for()
        assert '27 Nov 2026' in await page.locator('#lastUpdated').inner_text()
        # Crop the unmodified page content; the full application sidebar is not part of a Muse artifact.
        area = page.locator('#mainWrapper > .container')
        await area.screenshot(path=str(output / 'statistics-desktop.png'))
        await page.locator('[aria-label="Open views chart"]').first.click()
        await page.clock.run_for(1500)
        assert await page.evaluate('!!currentChart && currentChart.data.datasets[0].data.length > 0')
        await page.locator('.chart-modal-content').screenshot(path=str(output / 'statistics-chart.png'))
        await page.locator('.chart-close-btn').click()
        await page.locator('#privacyBtn').click()
        assert '$$$$' in await page.locator('#statsTableBody').inner_text()
        await area.screenshot(path=str(output / 'statistics-privacy.png'))
        await page.locator('#privacyBtn').click()
        await page.get_by_role('tab', name='Publishing', exact=True).click()
        await page.locator('[data-cp-action="expand"]').first.click()
        await page.locator('.cp-details').wait_for()
        assert '2 days' in await page.locator('#cpRows').inner_text()
        await area.screenshot(path=str(output / 'publishing-desktop.png'))
        await page.set_viewport_size({'width': 430, 'height': 1100})
        await area.screenshot(path=str(output / 'publishing-mobile.png'))
        assert not errors, errors
        assert not writes, writes
        await browser.close()
    revision = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    files = {name: hashlib.sha256((source / name).read_bytes()).hexdigest() for name in SOURCE_FILES}
    manifest = {'source_repository': 'https://github.com/kisanakclub/Yt_FusionX', 'source_commit': revision,
                'synthetic_data': True, 'source_sha256': files,
                'images': sorted(path.name for path in output.glob('*.png'))}
    (output / 'source.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'source_commit': revision, 'images': manifest['images'], 'page_errors': errors,
                      'write_requests': writes}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True, help='Assigned YtFusion checkout (read-only)')
    parser.add_argument('--chart-js', type=Path, required=True, help='Local Chart.js 4.4.0 UMD file')
    parser.add_argument('--browser', type=Path, help='Optional Chromium/Chrome executable')
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1] / 'references/ui')
    asyncio.run(capture(parser.parse_args()))
