# Native UI reference

Open these images when creating or revising a Muse dashboard, and supply the
images plus the relevant written/data brief to the artifact builder. The user
should not need to take screenshots for ordinary setup. These are captures of
the native templates with synthetic channels and metrics, not a public demo or
live account evidence. Do not copy sample identities, amounts or worker states
into an instance assignment or real snapshot.

## Reuse the current native CSS

The assigned YtFusion checkout is the visual source of truth. Read the current
template structure and CSS, including inline styles and the final cascade:
`src/templates/base.html` for theme/font/common controls,
`src/templates/channel_statistics.html`, `src/static/css/channel_insights.css`,
`src/static/css/channel_publishing.css`, and
`src/templates/partials/management_teal_theme.html`. Follow template load order;
a base rule may be superseded by a later feature or theme rule.

Import the relevant source styles into the artifact build and transfer required
inline rules/custom properties. Match native class/element structure in the host
components so the rules apply. Scope global selectors to the artifact root and
adapt shell/data bindings. A VM-local `/static` URL does not host CSS for the
artifact: supply current files through supported builder inputs or their exact
CSS contents with source paths/revision. Keep those as generated build assets;
do not maintain a second stylesheet in this skill repo. On an assigned UI
update, regenerate from the updated checkout rather than patching an old copy.

Preserve native font/fallback, type size/weight/line-height, theme, control
shapes, spacing, radii, table widths and responsive rules. Verify font
availability; a family declaration alone does not prove its face loaded. Do not
introduce a new heading font, pill controls or card system by builder preference.
Reuse the native chart library where supported, or match its typography, colors,
grid, strokes and tooltips in the host chart. Keep API/cache behavior unchanged.

Compare same-size desktop/narrow screenshots and representative computed styles:
header/filter/earnings height, table text, dialog width, topic/date controls,
primary strip and plot. Include long titles, empty/pending states and Privacy.
Remove duplicate footer totals in favor of native compact coverage. Functional
QA alone is not visual acceptance. Record specific host-driven differences.
Derive numeric values from the current source, not a fixed token table copied
into this guide. Source CSS, installed skill and delivered artifact are separate
verification steps; a repo pull alone does not update a dashboard.

## Statistics

![Native Statistics: compact header, tabs, filters, earnings summary and channel table](ui/statistics-desktop.png)

Preserve the table-first density, restrained teal accents, aligned numbers,
category/search controls and chart cells. The Chart header has a shared interval
selector with a 90d default; each row shows a cached views sparkline. The modal
retains its separate period controls and 30d default. The current header groups Privacy,
tab-specific Refresh and its retrieval time at the right. The app sidebar is
cropped out; a Muse artifact does not need to reproduce unrelated app navigation.
Keep unavailable revenue distinct from zero.

The main header uses a small framed action group: a bright teal Refresh button,
secondary Privacy and an info icon, with the timestamp beneath the action row.
Use equal-height controls, consistent inset padding, and a fine divider above
the left-aligned timestamp row; keep the info control aligned with the buttons.
Keep the group compact (under 80px high), including on mobile; avoid a large card
or an ungrouped line of controls and metadata.

![Compact header action group](ui/statistics-header.png)

Tips expands from the filter row,
and earnings totals form a thin strip with per-channel coverage. Keep the table
near the top instead of stacking large control cards. Connected Gmail addresses
appear below channel names and in dialog headers. Non-Gmail saved identities
display Brand; unknowns remain Email not saved. Mask them and Studio links in
Privacy. Sample account identities in these images are synthetic.

![Native chart dialog with period controls, dated series and metric selection](ui/statistics-chart.png)

![Overview with loaded average video length and cached Reach state](ui/statistics-overview-loaded.png)

![Selectable daily net-subscriber chart](ui/statistics-subscribers.png)

Views and Engaged views are simultaneous lines, with one date tooltip and
distinct legend colors. Show total subscribers separately from net growth.
Average video length has its own Load/Refresh and explicit video-count coverage.
Overview starts with Views, Engaged views, Watch time and Subscribers change,
with total subscribers as context. Engaged views includes its same-period
percentage of Views; no extra query.
Last 48h* uses the latest two reported daily dates, with the dates and a visible
non-realtime cue; it is not the Studio rolling-hour feed.
The graph follows this single compact primary
row. Average view duration, average viewed, original runtime and saved Reach
appear below as supporting metrics. Do not lead with original runtime or repeat
the totals in large footer cards. Definitions/retrieval dates use tooltips.
Impressions/CTR are saved Reach summaries: Pending is visible without a new
Reporting request. Preserve these data boundaries in the Muse artifact.

![Revenue groups Earnings and Estimated RPM](ui/statistics-revenue.png)

![RPM denominator control inside Revenue](ui/statistics-revenue-rpm.png)

![Revenue navigation at a narrow viewport](ui/statistics-revenue-mobile.png)

Tabs are topics: Overview / Content / Reach / Traffic / Audience / Revenue.
Views, Watch time and Subscribers are graph metrics inside Overview. Earnings
and Estimated RPM belong in Revenue; Impressions and CTR stay inside Reach.
Country/demographics/viewing groups stay in Audience. Keep narrow tab navigation
scrollable without squeezing labels; select Revenue when opening an earnings
chart from the channel table. Grouping never implies a Refresh all cascade.
Every tab uses the same responsive frame dimensions. Header and navigation remain
visible while the body scrolls; Content uses internal horizontal table scrolling.

Use a real chart dialog with period and metric controls. Hover/touch selects the
nearest reporting date across the plot. Dates, units and permission states follow
the data contract; an attractive screenshot alone is not proof of working charts.

![Native Audience with country shares and watch time](ui/statistics-audience.png)

![Audience with independently loaded demographics and viewing habits](ui/statistics-audience-loaded.png)

![Optional Audience cards at a narrow viewport](ui/statistics-audience-mobile.png)

Keep additional groups compact: Demographics pairs age/gender; Viewing habits
pairs devices/subscriber watch time. Each group owns Load data / Refresh and its
own timestamp/range. Empty groups stay unloaded until explicitly requested;
switching tabs/periods or the header refresh must not fetch them. Country average
duration/percentage enrich the existing table query. Overview adds net subscribers
and a daily subscriber metric without another query.

![Top five own videos with original length and viewing performance](ui/statistics-top-videos.png)

The optional Top videos group sits below Overview. Preserve title links, modest
thumbnails, separate original length / average viewing duration, aligned metrics
and its own Load / Refresh. Include Engaged views from that same Analytics query,
plus saved per-video impressions/CTR with pending/partial coverage labels and
Reach's separate control. It uses five ranked rows, not a full channel scan.

![Native Reach with daily impressions CTR](ui/statistics-reach.png)

![Pending Reach with its last check and earliest next manual check](ui/statistics-reach-pending.png)

Pending Reach shows Last checked and Check again after; its check control stays
disabled for one hour. That time permits another manual check, not an automatic
fetch or a promise that Google has prepared the report. Cached reads show Loading
rather than Refreshing, and other report tabs remain usable.

Load Overview, Audience, Reach and Traffic details on demand with their own dated caches.
Keep zero, withheld countries, pending Reach setup and API-disabled states distinct.

![Native Traffic with source table and trends](ui/statistics-traffic.png)

![Long Traffic report with navigation still visible](ui/statistics-traffic-scrolled.png)

![Traffic with explicit pending Impressions/CTR cells](ui/statistics-traffic-pending.png)

![Last 48h selection and same-period Engaged percentage](ui/statistics-overview-48h.png)

Missing Reach values have compact readable states and explanations, not bare
dashes. Keep Pending, Not loaded, No data, Not reported and access failures
distinct; reported zero impressions differs from an actual zero CTR.

![Native Browse detail with valid total-source trend](ui/statistics-browse.png)

![Suggested video titles with clickable watch URLs](ui/statistics-suggested.png)

![Suggested-video detail in a narrow viewport](ui/statistics-suggested-mobile.png)

Use titles as links without separate URL labels or arrows, two-line title
wrapping and aligned metrics. Unknown titles keep their exact link. Optional
title metadata has its own cached Data API lookup; it does not refresh Analytics.

![Clickable API, project and refresh usage information](ui/statistics-api-info.png)

Keep the table/graph relationship, explicit refresh scope and per-report dates.
The Browse table is an aggregate; its graph shows the valid total-source daily
trend, not invented per-feature daily values. API details are progressively
disclosed. Real unavailable/partial Reach states follow the data contract.

![Native chart at a narrow viewport](ui/statistics-chart-mobile.png)

Keep the modal, period controls and summary cards inside the viewport. Sparklines
stay inside their column; the wide channel table scrolls within its container.

![Native Privacy state with hidden identities and monetary placeholders](ui/statistics-privacy.png)

Use the native $$$$ monetary placeholder and mask identity in the dialog too.
The written privacy contract also covers open charts, summaries and tooltips.

## Content inside the channel dialog

![Catalog loaded without automatically loading Performance or Earnings](ui/statistics-content-catalog.png)

![Content with explicit page Performance and saved Reach](ui/statistics-content.png)

![Content at a narrow viewport](ui/statistics-content-mobile.png)

![Content columns scrolled while video identity stays pinned](ui/statistics-content-scroll-right.png)

![Visible per-video earnings and Engaged share](ui/statistics-content-earnings.png)

![Unloaded period explains how to fetch its metrics](ui/statistics-content-empty-period.png)

![Initial Content state points to the header Load action](ui/statistics-content-unloaded.png)

Keep Catalog, Performance and Earnings independently loaded and timestamped.
Default to newest uploads and one bounded page, with loaded-page search/sort,
Previous/Next over saved pages and explicit Load older uploads. The same responsive
dialog keeps the table internally scrollable without changing size. Do not fetch
period metrics merely because metadata is shown or the period changes. Show
original length separately from average viewing duration, and preserve unknown,
pending, partial, unavailable and valid-zero values. Use the current data contract
and development principles for the real backend behavior.
Content's reporting interval starts at Available (up to 730 days); other topics
start at 30d. The two windows, including custom dates, restore independently.

Keep Earnings visible next to Views/Engaged views, with its permission/unloaded
state and the local Engaged/Views percentage. Use a bounded viewport with sticky
header/video cells, a synchronized top scrollbar, explicit left/right controls
and page navigation above the table. The header refresh is limited to current
page Performance and previously loaded Earnings combined in one query; one missing Catalog page is
loaded first. Date changes stay cache-only and provide an actionable explanation.

## Publishing

![Native Publishing overview with one channel's scheduled-video details expanded](ui/publishing-desktop.png)

Preserve Statistics / Publishing as separate tabs, the shared filters, observed
cadence/time columns and expandable video lists. Follow
[Publishing behavior](publishing.md), including its separate refresh/cache.
Native write buttons are visible in this source capture; a reporting-only Muse
assignment does not gain permission to edit schedules or upload from this image.
Offer those actions only when an assigned, implemented host route supports them.

![Native Publishing at a narrow viewport with stacked channel details](ui/publishing-mobile.png)

Adapt the component to the artifact viewport. Keep table overflow inside its
scrolling region or use the native stacked presentation; chart/dialog controls
must remain reachable. Do not copy an existing app-shell overflow into Muse.

## Keep the reference current

The [capture manifest](ui/source.json) records the source commit and hashes of
the relevant native files. Compare it with the assigned checkout before a new
build or source-driven UI update. A different commit alone is not a UI change:
inspect the page/partials/CSS/JS diff. Current source and the user's explicit
choices determine behavior; these images document a reviewed baseline.

Read these together:

- src/templates/channel_statistics.html and src/templates/base.html for page
  structure, theme tokens, table/chart behavior and final style overrides.
- src/templates/partials/channel_publishing.html,
  src/static/css/channel_publishing.css and src/static/js/channel_publishing.js
  for the second tab and the shared header. Read referenced helpers as needed.
- src/channel_analytics.py, src/channel_publishing.py, the matching src/app.py
  handlers and docs/channel-publishing.md for real data and action contracts.
- src/channel_insights.py, src/channel_reach.py, src/static/js/channel_insights.js
  and src/static/css/channel_insights.css for lazy detail requests, cache behavior,
  thumbnail Reach and modal layout.

When a UI-affecting source update is assigned, update the same artifact and
inspect desktop, a narrow viewport, chart/Privacy and Publishing details. Keep
the existing connections, data and preferred chat. If the host cannot view
images, use the source plus the written composition above and report that
visual verification is pending; do not make a user's screenshot the default
prerequisite or claim an unseen viewer was verified.

## Rebuild the captures

Maintainers can run scripts/capture_ui_reference.py from this skill using an
assigned YtFusion checkout, Jinja2, Playwright/Chromium and a local copy of the
Chart.js 4.4.0 UMD file used by that checkout:

```bash
python scripts/capture_ui_reference.py --source /path/to/Yt_FusionX --chart-js /path/to/chart.umd.min.js
```

Run from the skill folder, or use the script's absolute path. An optional
--browser argument selects a locally installed Chromium/Chrome. The default
output is references/ui; --output selects another folder. Obtain dependencies
through the host's supported installation process only when needed. This is
a reference-maintenance tool, not a prerequisite for every Muse setup.

The script renders current templates with deterministic fictional data in an
isolated browser, intercepts every page request and rejects write requests.
It does not import src/app.py, start a backend, read account/config files, call
Google, or require a connected Mac. Inspect all generated images before replacing
the reviewed references. Do not change the running application to create them.
