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
import re
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
    'src/channel_content.py', 'src/static/js/channel_content.js', 'src/static/js/agent_setup.js',
    'docs/CHANNEL_STATISTICS_PRODUCT_PRINCIPLES.md', 'AGENTS.md',
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
        views['basis_values'] = {'subscribersGained':[8 for _ in rows], 'subscribersLost':[2 for _ in rows],
            'engagedViews':[round(value*.72) for _,value in rows]}
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
                      subscribers=analytics.subscriber_report(views),
                      engaged_views=analytics.daily_report([[day,round(value*.72)] for day,value in rows],start,end),
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
                             account_email=['example.creator@gmail.com','example-brand@pages.plusgoogle.com',None][index],
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
    pending_reach = False
    traffic_reach_pending = False
    optional_reports = {}
    content_calls, content_catalogs, content_reports = [], {}, {}
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
            if path == '/api/channel-statistics/content' and request.request.method == 'POST':
                body=request.request.post_data_json
                content_calls.append(body)
                action=body.get('action','peek');channel=body['channel'];page_index=body.get('page',0)
                catalog=content_catalogs.get(channel,dict(status='not_loaded',loaded_pages=0,fetched_at=None))
                if action in ('catalog','more'):
                    page_index=page_index+1 if action=='more' else 0
                    catalog=dict(status='available',loaded_pages=page_index+1,fetched_at=NOW.isoformat())
                    content_catalogs[channel]=catalog
                report_key=(channel,body['period'],page_index)
                perf=content_reports.get((report_key,'performance'),dict(status='not_loaded'))
                money=content_reports.get((report_key,'earnings'),dict(status='not_loaded'))
                if action in ('performance','earnings','performance_earnings'):
                    days=2 if body['period']=='48h' else 730 if body['period']=='all' else int(body['period'][:-1]) if body['period']!='custom' else 30
                    loaded=dict(status='available',fetched_at=NOW.isoformat(),requested_start=body.get('start',(date(2026,11,25)-timedelta(days=days-1)).isoformat()),requested_end=body.get('end','2026-11-25'))
                    for group in ('performance','earnings') if action=='performance_earnings' else (action,):
                        content_reports[(report_key,group)]=loaded
                        if group=='performance':perf=loaded
                        else:money=loaded
                videos=[]
                if catalog['loaded_pages']:
                    for i,title in enumerate(['A Quiet Modern Home with Warm Natural Materials','Small Spaces, Beautiful Everyday Details','Designing a Calm Courtyard Home','Light and Texture in a Thoughtful Interior','A Simple Home Built Around Nature','Open-Plan Spaces for Everyday Living']):
                        videos.append(dict(video_id=f'{page_index*10+i:011d}',title=title,published_at=f'2026-11-{25-i-page_index*5:02d}T12:00:00Z',duration='PT18M40S',
                            privacy='public',comments=i,thumbnail='https://i.ytimg.com/vi/AbCdEf_1-23/mqdefault.jpg',
                            performance=dict(views=2000-i*250,engagedViews=1400-i*160,estimatedMinutesWatched=8400-i*500,averageViewDuration=252,averageViewPercentage=22.5) if perf.get('fetched_at') else None,
                            earnings=dict(estimatedRevenue=4.25-i*.3) if money.get('fetched_at') else None,
                            reach=dict(impressions=20000-i*1000,ctr=6.4-i*.2,complete=False)))
                await request.fulfill(json=dict(success=True,report=dict(catalog=catalog,performance=perf,earnings=money,videos=videos,
                    page=page_index,loaded_pages=catalog['loaded_pages'],loaded_videos=catalog['loaded_pages']*6,has_more=catalog['loaded_pages']<2,reach=dict(status='available'))))
            elif path == '/api/channel-statistics/detail' and request.request.method == 'POST':
                body = request.request.post_data_json
                detail_calls.append(body)
                section = body['section']
                report = dict(status='available', fetched_at=NOW.isoformat(),
                              requested_start='2026-10-27', requested_end='2026-11-25',data_through='2026-11-25',api='youtubereporting' if section=='reach' else 'youtubeAnalytics',project={'project_id':'example-studio','owner':'owner@example.test'},usage={'youtubeAnalytics':{'requests':1,'quota_units':1}})
                if section == 'overview':
                    report['metrics'] = dict(views=63800,engagedViews=45936,estimatedMinutesWatched=267960,
                                            averageViewDuration=252, averageViewPercentage=42.7,
                                            subscribersGained=240,subscribersLost=60)
                    report['reach_summary']=dict(status='pending',fetched_at=NOW.isoformat())
                    if body['period']=='48h':
                        report.update(requested_start='2026-11-24',requested_end='2026-11-25')
                        daily=channels[0]['analytics']['reports']
                        total=sum(daily['views']['values'][-2:])
                        report['metrics'].update(views=total,engagedViews=sum(daily['engaged_views']['values'][-2:]),
                            estimatedMinutesWatched=total*4.2,subscribersGained=16,subscribersLost=4)
                elif section == 'audience':
                    report.update(countries=[dict(country=code, views=count, percentage=percent, watch_hours=count*4.2/60,average_duration=252,average_percentage=42.7)
                        for code, count, percent in [('US',25520,40),('ID',15950,25),('GB',9570,15),('CA',6380,10)]],
                        total_views=63800, unreported_views=6380)
                elif section in ('demographics','viewing','videos','video_lengths'):
                    cache_key=(body['channel'],body['period'],section)
                    if not body.get('refresh'):
                        report=optional_reports.get(cache_key,dict(status='not_loaded'))
                    else:
                        if section=='demographics':
                            report.update(ages=[dict(code='age'+code,percentage=p) for code,p in [('18-24',2),('25-34',12),('35-44',21),('45-54',31),('55-64',24),('65-',10)]],
                                genders=[dict(code='female',percentage=29),dict(code='male',percentage=71)])
                        elif section=='viewing':
                            report.update(devices=[dict(code=code,percentage=p) for code,p in [('TV',74),('DESKTOP',11),('MOBILE',10),('TABLET',5)]],
                                subscriptions=[dict(code='SUBSCRIBED',percentage=8),dict(code='UNSUBSCRIBED',percentage=92)])
                        elif section=='video_lengths':
                            report.update(average_length=1240,video_count=42,length_count=40,limited=False)
                        else:
                            report.update(videos=[dict(video_id='AbCdEf_1-23',title=title,published_at='2026-11-01T12:00:00Z',
                                duration='PT18M40S',views=2300-i*350,engaged_views=1650-i*250,reach=dict(impressions=24000-i*3000,ctr=5.6-i*.3,complete=False),
                                watch_hours=180-i*20,average_duration=288-i*12,average_percentage=25.7-i,
                                thumbnail='https://i.ytimg.com/vi/AbCdEf_1-23/mqdefault.jpg') for i,title in enumerate([
                                'Inside a Quiet Modern Home: Thoughtful Spaces for Everyday Living','Natural Materials and Light in a Small Open-Plan Home',
                                'A Courtyard Home with Beautiful Everyday Details','Small Spaces, Warm Light and Timeless Materials','A Calm Living Room Designed Around Nature'])])
                            report.update(video_reach_available=True,reach_status='available')
                        optional_reports[cache_key]=report
                elif section == 'reach':
                    dates = channels[0]['analytics']['reports']['views']['dates']
                    rates = [round(4.3+math.sin(i/7)*.8,2) for i in range(len(dates))]
                    common = dict(status='available', dates=dates, latest_reported_day=dates[-1])
                    report['reports'] = dict(
                        impressions=dict(common, values=[16000+i*75 for i in range(len(dates))]),
                        ctr=dict(common, values=rates, impression_values=[16000+i*75 for i in range(len(dates))],
                                 weighted_values=[rate*(16000+i*75) for i,rate in enumerate(rates)]))
                    if pending_reach:
                        report.update(status='pending', reports={}, data_through=None,
                            next_check_at=(NOW+timedelta(hours=1)).isoformat(),
                            message='YouTube is preparing daily Reach reports. Refresh this report later; the first report can take 48 hours.')
                elif section == 'traffic':
                    report.update(reach_status='available',reach_updated=NOW.isoformat(),apis=['youtubeAnalytics','youtubereporting'],estimate='1–2 Analytics queries; Reporting checks and new report downloads when needed.')
                    definitions=[('SUBSCRIBER','Browse features',32602,73.9),('RELATED_VIDEO','Suggested videos',8083,18.3),('YT_SEARCH','YouTube search',1286,2.9),('NO_LINK_OTHER','Direct or unknown',808,1.8),('YT_CHANNEL','Channel pages',449,1.0)]
                    if body.get('source') == 'SUBSCRIBER':
                        definitions=[('what-to-watch','Home',32246,98.9),('my-subscriptions','Subscriptions',182,.6),('my-history','Watch history',85,.3),('watch-later','Watch later',62,.2),('PP','Personalized playlists',26,.1)]
                    elif body.get('source') == 'RELATED_VIDEO':
                        definitions=[('AbCdEf_1-23','Inside a Quiet Modern Home: Thoughtful Spaces for Everyday Living',614,5.9),('Studio_Ref1','Natural Materials and Light in a Small Open-Plan Home',343,3.3),('DesignVid03','DesignVid03',131,1.3)]
                    dates=channels[0]['analytics']['reports']['views']['dates'][-30:]
                    report['sources']=[dict(code=code,label=label,views=count,percentage=percent,watch_hours=count*3.4/60,average_duration=204+i*25,average_percentage=36.5+i*3,reach=dict(impressions=count*5,ctr=6.7-i*.5),daily=[dict(day=day,views=round(count/30*(1+.4*math.sin(j/3+i)))) for j,day in enumerate(dates)]) for i,(code,label,count,percent) in enumerate(definitions)]
                    if traffic_reach_pending:
                        report.update(reach_status='pending',reach_message='YouTube is preparing daily Reach reports. Open Reach for its last check and next manual check.')
                        for row in report['sources']:row['reach']=None
                    if body.get('source'):
                        report['detail_trend']=[dict(day=day,views=round(1080*(1+.4*math.sin(j/3)))) for j,day in enumerate(dates)]
                        for row in report['sources']:
                            row['daily']=[]
                            if body['source']=='RELATED_VIDEO':
                                row.update(video_title=row['label'] if row['code']!='DesignVid03' else None,
                                    video_url='https://www.youtube.com/watch?v='+row['code'])
                        if body['source']=='RELATED_VIDEO':
                            report.update(video_titles_fetched_at=NOW.isoformat(),video_titles_usage={'requests':1,'quota_units':1},apis=['youtubeAnalytics','youtubereporting','youtube'])
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
            elif parsed.hostname == 'i.ytimg.com':
                await request.fulfill(content_type='image/svg+xml',body='<svg xmlns="http://www.w3.org/2000/svg" width="128" height="72"><rect width="128" height="72" fill="#28534f"/><rect x="22" y="13" width="84" height="47" fill="#a98d69"/><rect x="30" y="21" width="42" height="31" fill="#183e40"/><rect x="80" y="21" width="18" height="31" fill="#54776b"/></svg>')
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
        assert await page.locator('.cs-header-actions').evaluate("node=>node.getBoundingClientRect().height<=80")
        assert await page.locator('#lastUpdated').evaluate("node=>node.getBoundingClientRect().top>document.getElementById('refreshBtn').getBoundingClientRect().bottom"), 'Timestamp sits below the action row'
        assert await page.locator('#csStatisticsContent').evaluate("node=>node.getBoundingClientRect().top-document.querySelector('#mainWrapper > .container').getBoundingClientRect().top<320"), 'Compact controls should keep the table near the top'
        assert 'example.creator@gmail.com' in await page.locator('#statsTableBody').inner_text()
        assert 'pages.plusgoogle.com' not in await page.locator('#statsTableBody').inner_text()
        await area.screenshot(path=str(output / 'statistics-desktop.png'))
        await page.locator('.cs-header-actions').screenshot(path=str(output/'statistics-header.png'))
        await page.set_viewport_size({'width':430,'height':1000})
        assert await page.locator('.cs-header-actions').evaluate("node=>node.scrollWidth<=node.clientWidth+1 && node.getBoundingClientRect().height<=80")
        await page.locator('.cs-header-actions').screenshot(path=str(output/'statistics-header-mobile.png'))
        await page.set_viewport_size({'width':1600,'height':1000})
        await page.locator('[aria-label="Open views chart"]').first.click()
        await page.wait_for_function("document.getElementById('insightsOverviewDetails').textContent.includes('42.7%')")
        assert 'example.creator@gmail.com' in await page.locator('#channelAccount').inner_text()
        assert await page.locator('#channelAccount a').get_attribute('href')=='https://studio.youtube.com/channel/UC_SYNTHETIC_0'
        assert await page.locator('#insightsOverview .insights-card > span').all_text_contents()==['Views','Engaged views','Watch time','Subscribers · change']
        assert await page.locator('#insightsOverview').evaluate("node=>{const graph=document.getElementById('insightsPlot'), details=document.getElementById('insightsOverviewDetails'); return node.getBoundingClientRect().bottom<=graph.getBoundingClientRect().top && graph.getBoundingClientRect().bottom<=details.getBoundingClientRect().top}")
        assert await page.locator('#overviewMetricToggle .chart-metric-btn').all_text_contents()==['Views','Watch time','Subscribers']
        await page.clock.run_for(1500)
        assert await page.evaluate('!!currentChart && currentChart.data.datasets[0].data.length > 0')
        assert await page.evaluate("currentChart.data.datasets.length===2 && currentChart.data.datasets[1].label==='Engaged views'")
        assert not await page.locator('[data-metric="subscribers"]').is_disabled()
        assert await page.evaluate("currentChartTimeframe === '30d'")
        await page.locator('.chart-modal-content').screenshot(path=str(output / 'statistics-chart.png'))
        desktop_modal=await page.locator('.chart-modal-content').bounding_box()
        assert await page.locator('#insightsOverview .insights-card').nth(1).get_by_text('72.0% of views',exact=True).is_visible()
        await page.get_by_role('button',name='Last 48h*',exact=True).click()
        await page.wait_for_function("currentChartTimeframe==='48h' && currentChart.data.datasets[0].data.length===2 && document.getElementById('insightsStatus').textContent.includes('not realtime')")
        assert detail_calls[-1]['period']=='48h'
        await page.clock.run_for(500)
        await page.locator('.chart-modal-content').screenshot(path=str(output/'statistics-overview-48h.png'))
        await page.get_by_role('button',name='30d',exact=True).click()
        await page.locator('#insightsLength').get_by_role('button',name='Load data',exact=True).click()
        await page.locator('#insightsLength').get_by_text('20:40',exact=True).wait_for()
        await page.locator('.chart-modal-content').screenshot(path=str(output / 'statistics-overview-loaded.png'))
        before=len(detail_calls)
        await page.get_by_role('button',name='Subscribers',exact=True).click()
        await page.clock.run_for(500)
        assert await page.evaluate("currentChartType==='subscribers' && currentChart.data.datasets[0].data.some(v=>v!==null)")
        assert len(detail_calls)==before
        await page.locator('.chart-modal-content').screenshot(path=str(output / 'statistics-subscribers.png'))
        await page.get_by_role('button',name='Views',exact=True).click()
        await page.locator('#insightsExtra-videos').get_by_role('button',name='Load data',exact=True).click()
        await page.locator('#insightsExtra-videos').get_by_text('18:40',exact=True).first.wait_for()
        await page.locator('#insightsExtra-videos').screenshot(path=str(output / 'statistics-top-videos.png'))
        await page.get_by_role('tab', name='Audience', exact=True).click()
        await page.get_by_text('United States', exact=True).wait_for()
        await page.locator('.chart-modal-content').screenshot(path=str(output / 'statistics-audience.png'))
        assert not any(call.get('refresh') for call in detail_calls if call['section'] in ('demographics','viewing'))
        await page.locator('#insightsExtra-demographics').get_by_role('button',name='Load data',exact=True).click()
        await page.locator('#insightsExtra-demographics').get_by_text('31.0%',exact=True).wait_for()
        await page.locator('#insightsExtra-viewing').get_by_role('button',name='Load data',exact=True).click()
        await page.locator('#insightsExtra-viewing').get_by_text('74.0%',exact=True).wait_for()
        await page.locator('.chart-modal-content').screenshot(path=str(output / 'statistics-audience-loaded.png'))
        before=len([call for call in detail_calls if call.get('refresh')])
        await page.get_by_role('button',name='7d',exact=True).click()
        await page.locator('#insightsExtra-demographics').get_by_role('button',name='Load data',exact=True).wait_for()
        assert len([call for call in detail_calls if call.get('refresh')])==before
        await page.get_by_role('button',name='30d',exact=True).click()
        await page.locator('#insightsExtra-demographics').get_by_text('31.0%',exact=True).wait_for()
        await page.set_viewport_size({'width':430,'height':1000})
        await page.locator('#insightsAudienceExtras').screenshot(path=str(output / 'statistics-audience-mobile.png'))
        assert await page.locator('.chart-modal-content').evaluate('node=>node.scrollWidth<=node.clientWidth+1')
        await page.set_viewport_size({'width':1600,'height':1000})
        await page.get_by_role('tab',name='Content',exact=True).click()
        box=await page.locator('.chart-modal-content').bounding_box()
        assert abs(box['width']-desktop_modal['width'])<1 and abs(box['height']-desktop_modal['height'])<1, 'Content must retain the same dialog size'
        await page.get_by_text('Catalog not loaded',exact=True).wait_for()
        await page.clock.run_for(350)
        assert [call['action'] for call in content_calls]==['peek']
        assert content_calls[-1]['period']=='all'
        assert await page.get_by_role('button',name='Available',exact=True).evaluate("node=>node.classList.contains('active')")
        await page.locator('.chart-modal-content').screenshot(path=str(output/'statistics-content-unloaded.png'))
        await page.locator('.cc-group').nth(0).get_by_role('button',name='Load data',exact=True).click()
        await page.get_by_text('A Quiet Modern Home with Warm Natural Materials',exact=True).wait_for()
        assert [call['action'] for call in content_calls]==['peek','catalog']
        await page.locator('.chart-modal-content').screenshot(path=str(output/'statistics-content-catalog.png'))
        await page.locator('.cc-group').nth(1).get_by_role('button',name='Load data',exact=True).click()
        await page.get_by_role('cell',name='4:12',exact=True).first.wait_for()
        await page.locator('.chart-modal-content').screenshot(path=str(output/'statistics-content.png'))
        assert await page.locator('#contentTableViewport th').filter(has_text=re.compile(r'Earnings\s*USD')).count()==1
        assert await page.get_by_text('70.0% of views',exact=True).first.is_visible()
        before=len(content_calls)
        viewport=page.locator('#contentTableViewport')
        fixed_left=await page.locator('#contentRows td:first-child').first.evaluate('node=>node.getBoundingClientRect().left')
        await page.get_by_role('button',name='Scroll columns right',exact=True).click()
        await page.wait_for_function("document.getElementById('contentTableViewport').scrollLeft>0")
        assert abs(await page.locator('#contentRows td:first-child').first.evaluate('node=>node.getBoundingClientRect().left')-fixed_left)<2
        assert await page.locator('#contentScrollTop').evaluate("node=>Math.abs(node.scrollLeft-document.getElementById('contentTableViewport').scrollLeft)<2")
        assert len(content_calls)==before, 'Column navigation must not query Google'
        await page.locator('.chart-modal-content').screenshot(path=str(output/'statistics-content-scroll-right.png'))
        await viewport.evaluate("node=>{node.scrollLeft=0;node.dispatchEvent(new Event('scroll'))}")
        await page.locator('.cc-group').nth(2).get_by_role('button',name='Load data',exact=True).click()
        await page.get_by_role('cell',name='$4.25',exact=True).wait_for()
        await page.locator('.chart-modal-content').screenshot(path=str(output/'statistics-content-earnings.png'))
        before=len(content_calls)
        await page.locator('#reportRefresh').click()
        await page.wait_for_function("!document.getElementById('reportRefresh').disabled")
        assert [call['action'] for call in content_calls[before:]]==['performance_earnings']
        before=len(content_calls)
        await page.get_by_role('button',name='7d',exact=True).click()
        await page.locator('.cc-group').nth(1).get_by_role('button',name='Load data',exact=True).wait_for()
        assert content_calls[-1]['action']=='peek'
        await page.get_by_text('Performance not loaded for 7d. Use Refresh Content to load it.',exact=True).wait_for()
        await page.clock.run_for(350)
        await page.locator('.chart-modal-content').screenshot(path=str(output/'statistics-content-empty-period.png'))
        await page.locator('#reportRefresh').click()
        await page.wait_for_function("!document.getElementById('reportRefresh').disabled")
        assert [call['action'] for call in content_calls[before:]]==['peek','performance']
        await page.get_by_role('button',name='Available',exact=True).click()
        await page.get_by_role('cell',name='4:12',exact=True).first.wait_for()
        assert len(content_calls)==before+2
        await page.get_by_role('button',name='Load older uploads',exact=True).click()
        await page.locator('.cc-pagination > span').filter(has_text='Page 2 / 2 loaded · 12 videos').wait_for()
        before=len(content_calls)
        await page.get_by_role('button',name='← Previous',exact=True).click()
        await page.locator('.cc-pagination > span').filter(has_text='Page 1 / 2 loaded · 12 videos').wait_for()
        await page.get_by_role('button',name='Next →',exact=True).click()
        assert len(content_calls)==before
        await page.set_viewport_size({'width':430,'height':1000})
        assert await page.locator('.chart-modal-content').evaluate('node=>node.scrollWidth<=node.clientWidth+1')
        await page.locator('#insightsBody').evaluate('node=>node.scrollTop=0')
        await page.locator('.chart-modal-content').screenshot(path=str(output/'statistics-content-mobile.png'))
        await page.set_viewport_size({'width':1600,'height':1000})
        await page.get_by_role('tab', name='Reach', exact=True).click()
        assert await page.get_by_role('button',name='30d',exact=True).evaluate("node=>node.classList.contains('active')")
        await page.wait_for_function("!!currentChart && currentChartType === 'ctr' && currentChart.data.datasets[0].data.length > 0")
        await page.clock.run_for(1200)
        await page.locator('.chart-modal-content').screenshot(path=str(output / 'statistics-reach.png'))
        await page.get_by_role('tab', name='Traffic', exact=True).click()
        await page.get_by_role('button', name='Browse features →', exact=True).wait_for()
        await page.clock.run_for(500)
        nav=page.locator('.insights-tabs');nav_box=await nav.bounding_box()
        assert nav_box['height']>=30, 'Traffic must not collapse navigation into a blank line'
        box=await page.locator('.chart-modal-content').bounding_box()
        assert abs(box['width']-desktop_modal['width'])<1 and abs(box['height']-desktop_modal['height'])<1
        await page.locator('.chart-modal-content').screenshot(path=str(output / 'statistics-traffic.png'))
        await page.locator('#insightsBody').evaluate('node=>node.scrollTop=node.scrollHeight')
        assert await page.locator('#insightsBody').evaluate('node=>node.scrollTop>0'), 'Exercise a genuinely scrolling report'
        scrolled_nav=await nav.bounding_box()
        assert abs(scrolled_nav['y']-nav_box['y'])<1 and await page.locator('.chart-close-btn').is_visible()
        await page.locator('.chart-modal-content').screenshot(path=str(output/'statistics-traffic-scrolled.png'))
        traffic_reach_pending=True
        await page.locator('#reportRefresh').click()
        await page.get_by_role('cell',name='Pending',exact=True).first.wait_for()
        await page.clock.run_for(500)
        await page.locator('#insightsBody').evaluate('node=>node.scrollTop=0')
        await page.locator('.chart-modal-content').screenshot(path=str(output/'statistics-traffic-pending.png'))
        traffic_reach_pending=False
        await page.locator('#reportRefresh').click()
        await page.wait_for_function("!document.getElementById('reportRefresh').disabled")
        await page.get_by_role('button', name='Browse features →', exact=True).click()
        await page.get_by_role('cell', name='Home', exact=True).wait_for()
        await page.locator('.chart-modal-content').screenshot(path=str(output / 'statistics-browse.png'))
        before=len(detail_calls)
        await page.get_by_role('button',name='← All traffic sources',exact=True).click()
        await page.get_by_role('button',name='Browse features →',exact=True).wait_for()
        assert len(detail_calls)==before, 'Returning from Browse uses the saved traffic report'
        await page.get_by_role('button',name='Suggested videos →',exact=True).click()
        await page.get_by_role('link',name='Inside a Quiet Modern Home: Thoughtful Spaces for Everyday Living',exact=True).wait_for()
        assert await page.locator('a.insights-video-link').first.get_attribute('href')=='https://www.youtube.com/watch?v=AbCdEf_1-23'
        await page.locator('.chart-modal-content').screenshot(path=str(output / 'statistics-suggested.png'))
        await page.set_viewport_size({'width':430,'height':1000})
        await page.clock.run_for(300)
        assert await page.locator('.chart-modal-content').evaluate('node => node.getBoundingClientRect().right<=innerWidth && node.scrollWidth<=node.clientWidth+1')
        await page.locator('.chart-modal-content').screenshot(path=str(output / 'statistics-suggested-mobile.png'))
        await page.set_viewport_size({'width':1600,'height':1000})
        await page.get_by_role('button',name='← All traffic sources',exact=True).click()
        await page.get_by_role('button',name='Browse features →',exact=True).wait_for()
        before=len(detail_calls)
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
        pending_reach = True
        await page.locator('#reportRefresh').click()
        await page.wait_for_function("document.getElementById('reportRefresh').disabled && document.getElementById('insightsStatus').textContent.includes('Last checked')")
        assert 'Check again after' in await page.locator('#insightsStatus').inner_text()
        await page.locator('.chart-modal-content').screenshot(path=str(output / 'statistics-reach-pending.png'))
        before = len(detail_calls)
        await page.get_by_role('button', name='7d', exact=True).click()
        await page.clock.run_for(300)
        assert len(detail_calls) == before and await page.locator('#reportRefresh').is_disabled()
        await page.locator('.chart-close-btn').click()
        await page.locator('[aria-label="Open views chart"]').first.click()
        await page.clock.run_for(300)
        assert all(call['section'] in ('overview','videos') and not call.get('refresh') for call in detail_calls[before:]), 'After a Reach check, only reread saved Overview/video reports to decorate their new Reach status'
        await page.set_viewport_size({'width':430, 'height':1000})
        await page.clock.run_for(500)
        await page.wait_for_function('''() => {const node=document.querySelector('.chart-modal-content'), r=node.getBoundingClientRect(); return r.left>=0 && r.right<=innerWidth && node.scrollWidth<=node.clientWidth+1}''')
        await page.locator('.chart-modal-content').screenshot(path=str(output / 'statistics-chart-mobile.png'))
        await page.set_viewport_size({'width':1600, 'height':1000})
        before=len(detail_calls)
        await page.get_by_role('tab',name='Revenue',exact=True).click()
        assert len(detail_calls)==before, 'Revenue starts with saved daily earnings and never loads optional Overview groups'
        assert await page.locator('#revenueMetricToggle').is_visible()
        assert not await page.locator('#overviewMetricToggle').is_visible()
        await page.locator('.chart-modal-content').screenshot(path=str(output / 'statistics-revenue.png'))
        await page.get_by_role('button',name='Estimated RPM',exact=True).click()
        await page.wait_for_function("currentChartType==='rpm' && !document.getElementById('reportRefresh').disabled")
        assert detail_calls[-1]['section']=='rpm' and len(detail_calls)==before+1
        assert await page.locator('#rpmBasisControl').is_visible()
        assert await page.get_by_role('button',name='Estimated RPM',exact=True).get_attribute('aria-pressed')=='true'
        assert await page.get_by_role('button',name='Earnings',exact=True).get_attribute('aria-pressed')=='false'
        await page.clock.run_for(500)
        await page.locator('.chart-modal-content').screenshot(path=str(output / 'statistics-revenue-rpm.png'))
        await page.get_by_role('button',name='Earnings',exact=True).click()
        before=len(detail_calls)
        await page.set_viewport_size({'width':430,'height':1000})
        await page.get_by_role('tab',name='Overview',exact=True).click()
        await page.get_by_role('tab',name='Revenue',exact=True).click()
        assert await page.get_by_role('tab',name='Revenue',exact=True).evaluate('node=>{const r=node.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth}')
        assert await page.locator('.chart-modal-content').evaluate('node=>node.scrollWidth<=node.clientWidth+1')
        await page.locator('.chart-modal-content').screenshot(path=str(output / 'statistics-revenue-mobile.png'))
        await page.set_viewport_size({'width':1600,'height':1000})
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
