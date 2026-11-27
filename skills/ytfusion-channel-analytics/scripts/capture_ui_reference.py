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
    'src/app.py', 'src/templates/base.html', 'src/templates/channel_statistics.html',
    'src/templates/partials/channel_publishing.html',
    'src/static/css/channel_publishing.css', 'src/static/js/channel_publishing.js',
    'src/static/js/hds_time.js', 'src/channel_analytics.py', 'src/channel_publishing.py',
    'src/static/css/channel_insights.css', 'src/static/js/channel_insights.js',
    'src/channel_insights.py', 'src/channel_reach.py',
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
                             google_project={'project_id':'example-studio-'+str(index),'owner':'owner@example.test'}, api_usage={'youtube':{'requests':1,'quota_units':1},'youtubeAnalytics':{'requests':2,'quota_units':2}}, custom_url='@' + name.lower(), thumbnail_url='/avatar-' + str(index) + '.svg',
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
    errors, writes, detail_calls = [], [], []
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
            if path == '/api/channel-statistics/detail' and request.request.method == 'POST':
                body = request.request.post_data_json
                detail_calls.append(body)
                section = body['section']
                report = dict(status='available', fetched_at=NOW.isoformat(),
                              requested_start='2026-10-27', requested_end='2026-11-25',data_through='2026-11-25',api='youtubereporting' if section=='reach' else 'youtubeAnalytics',project={'project_id':'example-studio','owner':'owner@example.test'},usage={'youtubeAnalytics':{'requests':1,'quota_units':1}})
                if section == 'overview':
                    report['metrics'] = dict(views=63800, estimatedMinutesWatched=267960,
                                            averageViewDuration=252, averageViewPercentage=42.7)
                elif section == 'audience':
                    report.update(countries=[dict(country=code, views=count, percentage=percent, watch_hours=count*4.2/60)
                        for code, count, percent in [('US',25520,40),('ID',15950,25),('GB',9570,15),('CA',6380,10)]],
                        total_views=63800, unreported_views=6380)
                elif section == 'reach':
                    dates = channels[0]['analytics']['reports']['views']['dates']
                    rates = [round(4.3+math.sin(i/7)*.8,2) for i in range(len(dates))]
                    common = dict(status='available', dates=dates, latest_reported_day=dates[-1])
                    report['reports'] = dict(
                        impressions=dict(common, values=[16000+i*75 for i in range(len(dates))]),
                        ctr=dict(common, values=rates, impression_values=[16000+i*75 for i in range(len(dates))],
                                 weighted_values=[rate*(16000+i*75) for i,rate in enumerate(rates)]))
                elif section == 'traffic':
                    report.update(reach_status='available',reach_updated=NOW.isoformat(),apis=['youtubeAnalytics','youtubereporting'],estimate='1–2 Analytics queries; Reporting checks and new report downloads when needed.')
                    definitions=[('SUBSCRIBER','Browse features',32602,73.9),('RELATED_VIDEO','Suggested videos',8083,18.3),('YT_SEARCH','YouTube search',1286,2.9),('NO_LINK_OTHER','Direct or unknown',808,1.8),('YT_CHANNEL','Channel pages',449,1.0)]
                    if body.get('source'):
                        definitions=[('what-to-watch','Home',32246,98.9),('my-subscriptions','Subscriptions',182,.6),('my-history','Watch history',85,.3),('watch-later','Watch later',62,.2),('PP','Personalized playlists',26,.1)]
                    dates=channels[0]['analytics']['reports']['views']['dates'][-30:]
                    report['sources']=[dict(code=code,label=label,views=count,percentage=percent,watch_hours=count*3.4/60,average_duration=204+i*25,average_percentage=36.5+i*3,reach=dict(impressions=count*5,ctr=6.7-i*.5),daily=[dict(day=day,views=round(count/30*(1+.4*math.sin(j/3+i)))) for j,day in enumerate(dates)]) for i,(code,label,count,percent) in enumerate(definitions)]
                    if body.get('source'):
                        report['detail_trend']=[dict(day=day,views=round(1080*(1+.4*math.sin(j/3)))) for j,day in enumerate(dates)]
                        for row in report['sources']:
                            row['daily']=[]
                elif section == 'earnings':
                    original=channels[0]['analytics']['reports']['earnings']
                    first,last=body.get('start',original['requested_start']),body.get('end',original['requested_end'])
                    selected=[(d,v) for d,v in zip(original['dates'],original['values']) if first<=d<=last]
                    report.update(requested_start=first,requested_end=last,data_through=last,reports={'earnings':{**original,'dates':[d for d,v in selected],'values':[v for d,v in selected],'requested_start':first,'requested_end':last,'latest_reported_day':last}})
                elif section == 'rpm':
                    report['reports'] = {key:channels[0]['analytics']['reports'][key] for key in ('rpm','rpm_engaged')}
                await request.fulfill(json={'success':True,'report':report})
            elif request.request.method != 'GET':
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
        assert not detail_calls, 'The table must not fetch modal reports'
        assert await page.locator('#miniChartPeriod').input_value() == '90d'
        await page.locator('#miniChartPeriod').select_option('7d')
        assert await page.evaluate("miniChartTimeframe === '7d' && currentChartTimeframe === '30d'")
        assert not detail_calls, 'Changing a mini-chart period must use the cache'
        await page.locator('#miniChartPeriod').select_option('90d')
        assert await page.locator('#statsTableBody tr:first-child td:nth-child(9)').evaluate('cell => {const c=cell.querySelector("canvas").getBoundingClientRect(), r=cell.getBoundingClientRect(); return c.left>=r.left && c.right<=r.right}')
        assert '27 Nov 2026' in await page.locator('#lastUpdated').inner_text()
        # Crop the unmodified page content; the full application sidebar is not part of a Muse artifact.
        area = page.locator('#mainWrapper > .container')
        await area.screenshot(path=str(output / 'statistics-desktop.png'))
        await page.locator('[aria-label="Open views chart"]').first.click()
        await page.wait_for_function("document.getElementById('insightsOverview').textContent.includes('42.7%')")
        await page.clock.run_for(1500)
        assert await page.evaluate('!!currentChart && currentChart.data.datasets[0].data.length > 0')
        assert await page.evaluate("currentChartTimeframe === '30d'")
        await page.locator('.chart-modal-content').screenshot(path=str(output / 'statistics-chart.png'))
        await page.get_by_role('tab', name='Audience', exact=True).click()
        await page.get_by_text('United States', exact=True).wait_for()
        await page.locator('.chart-modal-content').screenshot(path=str(output / 'statistics-audience.png'))
        await page.get_by_role('tab', name='Reach', exact=True).click()
        await page.wait_for_function("!!currentChart && currentChartType === 'ctr' && currentChart.data.datasets[0].data.length > 0")
        await page.clock.run_for(1200)
        await page.locator('.chart-modal-content').screenshot(path=str(output / 'statistics-reach.png'))
        await page.get_by_role('tab', name='Traffic', exact=True).click()
        await page.get_by_role('button', name='Browse features →', exact=True).wait_for()
        await page.clock.run_for(500)
        await page.locator('.chart-modal-content').screenshot(path=str(output / 'statistics-traffic.png'))
        await page.get_by_role('button', name='Browse features →', exact=True).click()
        await page.get_by_role('cell', name='Home', exact=True).wait_for()
        await page.locator('.chart-modal-content').screenshot(path=str(output / 'statistics-browse.png'))
        before=len(detail_calls)
        await page.get_by_role('button',name='← All traffic sources',exact=True).click()
        await page.get_by_role('button',name='Browse features →',exact=True).wait_for()
        assert len(detail_calls)==before, 'Returning from Browse uses the saved traffic report'
        await page.locator('[aria-label="Report API information"]').click()
        await page.locator('#reportApiInfo').screenshot(path=str(output / 'statistics-api-info.png'))
        await page.locator('[aria-label="Report API information"]').click()
        before=len(detail_calls)
        await page.locator('#reportRefresh').click()
        await page.get_by_role('button',name='Browse features →',exact=True).wait_for()
        assert len(detail_calls)==before+1 and detail_calls[-1].get('refresh') is True
        await page.get_by_role('tab', name='Reach', exact=True).click()
        before = len(detail_calls)
        await page.get_by_role('button', name='90d', exact=True).click()
        await page.clock.run_for(300)
        assert len(detail_calls) == before, 'Reach period change must reuse the downloaded report'
        await page.locator('.chart-close-btn').click()
        await page.locator('[aria-label="Open views chart"]').first.click()
        await page.clock.run_for(300)
        assert len(detail_calls) == before, 'Reopening the same overview must reuse its cache'
        await page.set_viewport_size({'width':430, 'height':1000})
        await page.clock.run_for(500)
        await page.wait_for_function('''() => {const node=document.querySelector('.chart-modal-content'), r=node.getBoundingClientRect(); return r.left>=0 && r.right<=innerWidth && node.scrollWidth<=node.clientWidth+1}''')
        await page.locator('.chart-modal-content').screenshot(path=str(output / 'statistics-chart-mobile.png'))
        await page.set_viewport_size({'width':1600, 'height':1000})
        before=len(detail_calls)
        await page.get_by_role('button',name='Earnings',exact=True).click()
        await page.get_by_role('button',name='Latest day',exact=True).click()
        assert len(detail_calls)==before, 'Existing daily earnings serves a shorter interval'
        await page.get_by_role('button',name='Custom dates',exact=True).click()
        await page.locator('#insightsStart').fill('2026-11-01')
        await page.locator('#insightsEnd').fill('2026-11-03')
        await page.get_by_role('button',name='Apply',exact=True).click()
        assert len(detail_calls)==before
        await page.locator('#reportRefresh').click()
        await page.wait_for_function("currentChartTimeframe==='custom' && currentChart.data.datasets[0].data.length===3 && !document.getElementById('reportRefresh').disabled")
        assert detail_calls[-1]['section']=='earnings' and detail_calls[-1]['refresh'] is True
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
                'source_has_local_changes': bool(subprocess.check_output(['git','-C',str(source),'status','--porcelain'],text=True).strip()),
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
