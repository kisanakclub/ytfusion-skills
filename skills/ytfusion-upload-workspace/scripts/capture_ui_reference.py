#!/usr/bin/env python3
"""Capture native YT Upload using fictional fixtures and intercepted requests.

Requires Jinja2, Playwright and Chromium. Reads only supplied templates/static
assets; no app import, server, live queue, account or credential is loaded.
"""
import argparse
import asyncio
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import subprocess
from urllib.parse import parse_qs, urlparse

from jinja2 import Environment, FileSystemLoader
from playwright.async_api import async_playwright

NOW = datetime(2026, 11, 27, 5, tzinfo=timezone.utc)
SOURCE_FILES = (
    'src/templates/base.html', 'src/templates/yt_upload.html',
    'src/static/js/hds_time.js', 'src/static/js/yt_drive_inbox.js',
    'src/static/js/yt_drive_jobs.js', 'src/static/js/yt_channel_queue.js',
    'src/static/js/yt_queue_schedule.js', 'src/static/js/yt_upload_clock.js',
    'src/static/js/yt_queue_order.js', 'src/static/js/yt_upload_progress.js',
    'src/static/js/yt_completed_groups.js', 'src/static/js/hds_upload_sync.js',
    'src/static/js/yt_project_activity.js', 'src/static/css/yt_project_activity.css',
    'src/static/css/yt_drive_inbox.css', 'src/static/css/yt_channel_queue.css',
    'src/static/css/yt_queue_schedule.css',
)


def fixtures():
    names = ['A Quiet Courtyard in the Morning', 'Small Spaces, Thoughtful Details',
             'Warm Wood and Natural Light', 'A Studio for Slow Afternoons',
             'A Home Built Around the Garden']
    rows = []
    for index, title in enumerate(names):
        manifest = dict(jobId=f'synthetic-package-{index}', projectName=f'project-{index}',
                        draftName='Final', projectId=f'synthetic-project-{index}',
                        projectRef=dict(projectType='batch', batchKey='Quiet Spaces', projectKey=f'project-{index}'),
                        collectionId='synthetic-collection', collectionName='Studio Collection',
                        batchName='Quiet Spaces', sourceProfile=dict(profileId='synthetic-profile', displayName='Aurora Studio'),
                        original_duration_seconds=720 + index * 85,
                        youtube=dict(title=title, description='Fictional reference video.', tags=['design'],
                                     category='22', privacy='private'))
        row = dict(manifest=manifest, manifestPath=f'Studio/Metadata/{index}.json',
                   driveCreatedAt=(NOW - timedelta(hours=index)).isoformat(),
                   root='Synthetic Drive', matchCount=1,
                   video=dict(id=f'synthetic-file-{index}', name=f'{title}.mp4',
                              size=(index + 2) * 320000000), thumbnail=dict(id=f'thumb-{index}'))
        if index == 2:
            row['uploadHistory'] = dict(videoId='synthetic-upload', channel='Aurora Studio',
                                        url='https://www.youtube.com/watch?v=synthetic-upload')
        if index == 3:
            row['video'] = None
        rows.append(row)
    queues = [dict(id='synthetic-private', channel='aurora', mode='private', name='Studio Collection', paused=True,
                   settings={}, created=NOW.timestamp()),
              dict(id='synthetic-scheduled', channel='quiet', mode='scheduled', name='', paused=True,
                   settings={}, created=NOW.timestamp())]
    jobs = []
    for index in range(2):
        payload = dict(title=names[index], channel_id='aurora', channel_name='Aurora Studio',
                       privacy='private', video_name=names[index] + '.mp4', video_path=f'drive://synthetic-file-{index}',
                       project=f'project-{index}', draft_name='Final', _drive_job_id=f'synthetic-package-{index}',
                       original_duration_seconds=720 + index * 85,
                       _drive_source=dict(root='Synthetic Drive', manifestPath=rows[index]['manifestPath'],
                                          videoPath=f'Studio/Videos/{index}.mp4'),
                       collectionName='Studio Collection', collectionId='synthetic-collection')
        jobs.append(dict(id=f'synthetic-job-{index}', queue_id=queues[0]['id'], channel='aurora', state='queued',
                         position=index, created=NOW.timestamp(), updated=NOW.timestamp(),
                         run_at=NOW.timestamp() + (index + 2) * 86400, estimate_minutes=25,
                         payload=payload, result={}, progress={}))
    for index in range(len(rows), 56):
        title = f'Quiet Spaces · Episode {index + 1}'
        manifest = dict(rows[0]['manifest'], jobId=f'synthetic-package-{index}',
                        projectId=f'synthetic-project-{index}', projectName=f'project-{index}',
                        projectRef=dict(projectType='batch', batchKey='Quiet Spaces', projectKey=f'project-{index}'),
                        youtube=dict(rows[0]['manifest']['youtube'], title=title))
        rows.append(dict(rows[0], manifest=manifest, manifestPath=f'Studio/Metadata/{index}.json',
                         driveCreatedAt=(NOW - timedelta(hours=index)).isoformat(),
                         video=dict(id=f'synthetic-file-{index}', name=f'{title}.mp4', size=320000000)))
    return rows, dict(jobs=jobs, queues=queues, paused=[], reservations=[])


async def capture(args):
    source, output = args.source.resolve(), args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    for name in SOURCE_FILES:
        if not (source / name).is_file():
            raise ValueError('Required native source missing: ' + name)
    html = Environment(loader=FileSystemLoader(source / 'src/templates')).get_template('yt_upload.html').render(
        url_path=lambda path: path, root_path='', url_for=lambda *a, **kw: '/',
        get_flashed_messages=lambda request: [], request={'app': {'state': {}}}, username='UI reference',
        installation_device=lambda: 'local', dashboard_home=lambda request: '/',
        hds_collection_context='synthetic-collection')
    rows, snapshot = fixtures()
    errors, writes = [], []
    async with async_playwright() as playwright:
        options = dict(headless=True)
        if args.browser:
            options['executable_path'] = str(args.browser)
        browser = await playwright.chromium.launch(**options)
        page = await browser.new_page(viewport=dict(width=1440, height=1100), device_scale_factor=1)
        page.on('pageerror', lambda error: errors.append(str(error)))
        await page.clock.install(time=NOW)
        await page.add_init_script("localStorage.setItem('theme','dark-mode'); localStorage.setItem('sidebarCollapsed','true');")

        async def route(request):
            req = request.request
            parsed = urlparse(req.url)
            path = parsed.path
            if parsed.hostname != 'reference.invalid':
                await request.fulfill(status=204, body='')
            elif req.method != 'GET':
                # Native status-refresh is a read-like POST; fixtures never contact a backend.
                if path.endswith(('/status_refresh', '/upload_sync')):
                    await request.fulfill(json=dict(success=True, state='done', parts={}, checkedAt=NOW.timestamp()))
                else:
                    writes.append(path)
                    await request.fulfill(status=405, json=dict(success=False, error='Reference is read-only'))
            elif path == '/preview':
                await request.fulfill(content_type='text/html', body=html)
            elif path.startswith('/static/'):
                asset = (source / 'src' / path.lstrip('/')).resolve()
                if asset.is_relative_to(source / 'src/static') and asset.is_file():
                    await request.fulfill(path=str(asset))
                else:
                    await request.fulfill(status=404, body='')
            elif path.endswith('/drive_thumbnail'):
                svg = '<svg xmlns="http://www.w3.org/2000/svg" width="160" height="90"><rect width="160" height="90" fill="#213f43"/><path d="M20 72V37L80 9l60 28v35H20m20 0V44h80v28" fill="#a1b5a1"/><rect x="65" y="42" width="30" height="30" fill="#526d65"/></svg>'
                await request.fulfill(content_type='image/svg+xml', body=svg)
            else:
                data = dict(success=True)
                if path.endswith('/settings'):
                    data.update(installationRole='vps', trashSupported=False)
                elif path.endswith('/init'):
                    data.update(projects=[], channels=[dict(id='aurora', name='Aurora Studio'),
                                                       dict(id='quiet', name='Quiet Atlas')], categories={}, channel_mappings={})
                elif path.endswith('/drive_context'):
                    data.update(ready=True, account='creator@example.com', root='Synthetic Drive')
                elif path.endswith('/drive_inbox'):
                    # The native stream reader consumes NDJSON even for this offline fixture.
                    body = '\n'.join(json.dumps(dict(type='row', row=row)) for row in rows)
                    body += '\n' + json.dumps(dict(type='done', checkedAt=NOW.timestamp())) + '\n'
                    if parse_qs(parsed.query).get('stream') == ['true']:
                        await request.fulfill(content_type='application/x-ndjson', body=body)
                    else:
                        await request.fulfill(json=dict(success=True, rows=rows, available=True, checkedAt=NOW.timestamp()))
                    return
                elif path.endswith('/channel_queue'):
                    data.update(snapshot, server_now=NOW.timestamp())
                elif path.endswith('/status'):
                    data.update(jobs=[], status='idle')
                elif path.endswith('/storage'):
                    data.update(total=80000000000, free=42000000000)
                elif path.endswith('/status_refresh'):
                    data.update(state='done', parts={}, checkedAt=NOW.timestamp())
                elif path.endswith(('/staged', '/recovery')):
                    data.update(rows=[])
                elif path.endswith('/drive_jobs'):
                    data.update(jobs=[])
                elif path.endswith('/parallel_settings'):
                    data.update(max_parallel=1)
                elif path.endswith('/upload_sync'):
                    data.update(state='done', lastSuccess=NOW.timestamp(), revision=1,
                                refresh=dict(state='done', finishedAt=NOW.timestamp(),
                                             parts={key: dict(state='done', checkedAt=NOW.timestamp())
                                                    for key in ('drive', 'history', 'device')}))
                elif path.endswith('/project_activity'):
                    data.update(projects=[], version=1)
                elif path.endswith('/collection-location'):
                    data.update(activePath='/synthetic/Studio Collection',
                                available=True, status='ready')
                await request.fulfill(json=data)

        await page.route('**/*', route)
        await page.goto('http://reference.invalid/preview')
        await page.wait_for_function("_yuMode === 'vps' && yuChannelReady && !document.querySelector('.yu-workspace').inert")
        await page.evaluate("yuShowWorkspace('drive')")
        await page.wait_for_function("_yuDriveRows.length === 56 && !window._yuDriveLoading")
        assert await page.locator('#yuInboxSort').input_value() == 'newest'
        assert await page.locator('[data-yu-sort=arrival]').inner_text() == 'Masuk Drive'
        assert await page.locator('.yu-inbox-arrival time').first.inner_text() == '27 Nov, 12:00 WIB'
        assert 'Aurora Studio' in await page.locator('.yu-inbox-queue-destination').first.inner_text()
        assert 'Mulai upload' in await page.locator('.yu-inbox-queue-destination').first.inner_text()
        assert await page.locator('#yuInboxPagination').is_visible()
        assert await page.locator('#yuDriveRows .yu-library-row').count() == 50
        assert not await page.locator('#yuDriveMsg').inner_text()
        area = page.locator('.yu-page')
        await area.screenshot(path=str(output / 'drive-inbox-desktop.png'))
        await page.set_viewport_size(dict(width=430, height=1100))
        # Omit the native app-shell header, which is not reproduced inside Muse.
        await page.locator('.yu-workspace').screenshot(path=str(output / 'drive-inbox-mobile.png'))
        await page.set_viewport_size(dict(width=1440, height=1100))
        await page.evaluate("yuShowWorkspace('queue'); yuChannelOpen.set('synthetic-private',true);yuRenderQueue();")
        await page.locator('.yu-channel-group').first.wait_for()
        await area.screenshot(path=str(output / 'upload-queue-desktop.png'))
        await page.set_viewport_size(dict(width=430, height=1100))
        await page.locator('.yu-workspace').screenshot(path=str(output / 'upload-queue-mobile.png'))
        await page.set_viewport_size(dict(width=1440, height=1100))
        await page.evaluate("yuOpenQueueSchedule('synthetic-private')")
        await page.locator('#yuQueueScheduleDialog').wait_for(state='visible')
        await page.locator('#yuQueueScheduleDialog').screenshot(path=str(output / 'queue-settings-desktop.png'))
        assert not errors, errors
        assert not writes, writes
        await browser.close()
    manifest = dict(source_repository='https://github.com/kisanakclub/Yt_FusionX',
                    source_commit=subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip(),
                    source_has_local_changes=bool(subprocess.check_output(
                        ['git', '-C', str(source), 'diff', 'HEAD', '--name-only', '--', *SOURCE_FILES], text=True).strip()),
                    synthetic_data=True,
                    source_sha256={name: hashlib.sha256((source / name).read_bytes()).hexdigest() for name in SOURCE_FILES},
                    images=sorted(path.name for path in output.glob('*.png')))
    (output / 'source.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(dict(source_commit=manifest['source_commit'], images=manifest['images'],
                          page_errors=errors, write_requests=writes)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--browser', type=Path)
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1] / 'references/ui')
    asyncio.run(capture(parser.parse_args()))
