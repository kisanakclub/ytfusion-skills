# Private Muse channel Analytics dashboard

## Deliver an app the user can reopen

Use Muse's current artifact and client-surface documentation to choose a
supported private interactive app. On the inspected Muse host, the supported
surface is a fullstack artifact (`artifact.create_web_fullstack`), with server
logic and persistent database. Verify the current documentation and private
delivery before creating it; keep credential access in trusted VM execution.

Name the persistent artifact for the instance's channel Analytics and keep it in
**Library**. Present its artifact card in the user's chosen chat; use the main
chat for coordination and refresh requests unless a side chat is requested.
Keep any explicit later chat preference. When the user changes the destination,
handoff the existing task and show the same artifact card there; do not create
another dashboard or duplicate an in-flight build/refresh. A prior side chat may
remain as history without becoming the required entry point. On the inspected host,
artifacts do not have their own built-in side chat; these are separate surfaces.
If a separate chat was requested, provide its dashboard context. If direct side-chat
creation is unavailable, give the actual supported UI route; do not invent a chat
URL or create a Codex thread. Do not require a new chat just to answer a quick question.

Store the artifact identity, actual reopen link/location, private backend/cache
binding and user preferences in instance context. Reopen/update the same artifact
after refresh or new conversations. Verify persistence by closing and reopening
the artifact viewer. A local HTML file, screenshot, temporary preview server or
main-chat table alone does not fulfill a request for a reusable Muse dashboard.

Do not assume a bare VM localhost server is visible to Muse's user-facing browser.
Use the host's supported artifact routing, backend execution and persistent data
storage. Do not expose an unauthenticated public port, embed Google credentials in
JavaScript, or publish private Analytics on the Firebase branding site. If the
artifact delivery would make data public, stop before that exposure and offer a
supported private delivery instead. Existing API credentials in the VM should
allow routine refresh without the Mac or another Google login.

## Match channel-stats thoughtfully

Open the [bundled screenshots and source map](ui-reference.md) before designing
and give those images to the artifact builder alongside the data/behavior brief.
Read the assigned source page plus its included partials and CSS/JS, not only
the top-level template. Use the actual composition, density and interactions.
The user should not need to supply screenshots for standard setup. An explicit
user screenshot can refine the brief; keep private captures out of this repo.
Synthetic sample channels/values are never account assignments or real app data.
Use English for dashboard labels by default, matching the owner's UI preference
and native channel-stats; keep chat replies in the user's language. An explicit
UI language choice overrides that default. Follow the native hierarchy:

- Compact header: title/icon at left; Privacy, the active tab's supported refresh
  action and its small last-update line grouped at right. Use the native restrained
  divider/accent. Below it, preserve Statistics / Publishing tabs and shared filters.
- One collapsed **Info & Tips** row for freshness, permissions and data definitions.
  Do not fill the default page with repeated date/source paragraphs, revenue
  warning panels, implementation details or four large summary cards.
- One filter toolbar: Category dropdown, Search channels and a visible count.
- The channel table is the main content. Follow native column order: internal
  name when assigned, YouTube Channel (avatar/name/handle/link), Monetization, Subs, Videos,
  Watch Hrs (365d), 24h\*, 48h\*, Chart, Earnings 24h\*, Earnings this month,
  Earnings last month, Earnings chart, and operational
  Status when a real source exists. Keep numbers aligned and typography compact.
  Show **Monetization** as its own visible, sortable column beside channel identity:
  **Monetized** for explicit `true`, **Not monetized** for explicit `false`, and
  **Unknown** when absent/unavailable. Use readable text with restrained styling;
  a dollar/question-mark icon or tooltip beside the channel name is insufficient.
  Keep this channel status separate from revenue permission/errors and worker Status.
  Use compact clickable views sparklines in the Chart column. Its shared period
  selector offers 7d/14d/30d/90d/180d, defaults to 90d and remembers the choice.
  Draw from the cached daily series; missing dates remain gaps. Keep the canvas
  inside its column and monetary values in their own cells. Sorting Chart uses
  the selected interval. Earnings retain their dedicated chart button.
- When all-channel earnings totals are requested, use a compact summary strip
  for **Total earnings (available history)**, **This month so far**, and **Last month**.
  Totals cover all assigned channels, including those outside the current filter.
  Show how many channels supplied data; unknown/unavailable grants do not become
  zero. Keep USD/other currencies separate and show differing cutoffs/partial
  coverage. Available history is bounded (native up to 730 days), not lifetime.
- Put periods, metric selection, detailed summaries and any optional daily table
  inside the chart dialog. A 30-day initial graph is useful; preserve later choices.
  Keep the mini-chart period independent of the modal's existing
  Latest day/Last 48h*/3d/7d/14d/30d/90d/180d/Available and custom-date controls. The modal opens at 30d; Content starts at Available with its own remembered window.
  Topic tabs are Overview, Content, Reach, Traffic, Audience and Revenue.
  Overview leads with Views / Engaged views / Watch time / subscriber change,
  with current subscriber total as context, followed by the graph. Its graph
  metrics are Views / Watch time / Subscribers. Place API average view duration,
  average percentage viewed, optional original runtime and saved Reach below
  the graph. Revenue owns Earnings / Estimated RPM and the denominator control;
  opening the table's earnings chart selects Revenue directly.
  Audience shows countries, share of channel views and watch time. Traffic shows all source trends, exact source metrics, and Browse/Suggested drill-down. Use total-source trends when per-feature daily Analytics queries are unsupported. Reach shows
  impressions and weighted thumbnail CTR with a graph selector. Fetch each
  detail section on demand and retain its dated cache; see the data contract.

For a full channel-stats-style dashboard, include the read-only
[Publishing overview](publishing.md) with its observed cadence, scheduled-video
details and separate refresh/coverage. An explicitly narrower report can omit
that tab. Do not implement schedule writes merely because native screenshots
show the editor; those require an assigned operation and supported backend.

For 24h\*/48h\*, follow
[latest reported days](data-contract.md#latest-reported-day-and-two-day-columns).
Keep the non-realtime cue compact and dates available by tooltip/subtext without
repeating paragraphs in every row. Show unavailable monetary/worker values as
an em dash or concise state with an accessible explanation. Disable a revenue
chart when its source is unavailable; do not fabricate zero revenue, monetization
or worker status. Unsupported source fields are a data limitation, not a reason
to remove filtering/chart architecture from a reusable multi-channel UI.

### Filtering and chart interactions

Native category metadata comes from `/api/categories` and the channel mapping in
`/api/status`. In executor mode, use assigned/native metadata available to that
instance; missing category is **Uncategorized**. Populate **All Categories** and
category counts from the assigned channel list. A one-channel pilot still gets
the filter; do not hardcode its category or infer one from its title. Category
and case-insensitive search combine, with a correct **Showing X of Y** count.
Search channel/internal names and handles. Preserve filters across sorting and
refresh, and display a concise empty-filter result without dropping cached data.

Make the row's Chart icon open an actual dialog/panel with channel identity,
interactive daily chart, dated tooltips, close control and keyboard dismissal.
Chart inspection should work across the plot area by the nearest reporting date
on the horizontal axis, without requiring an exact point hit. Highlight the
selected point and use a restrained vertical date guide. Keep tooltip date/value
aligned with the selected real report; gaps must not become zero or interpolated
observations. Preserve native mouse/touch interactions and privacy for monetary
charts. Moving the cursor must use cached data, not trigger API requests.
Offer **Latest reported day / Last 48h* / 3d / 7d / 14d / 30d / 90d / 180d / Available / Custom dates**, with Views and Watch time
working from real dated series. Earnings can have a separate native-style chart
action when access exists. Add **Estimated RPM** to the chart's metric selector
within Revenue when that feature is requested. Offer an explicit **Views / Engaged views** basis
in the RPM detail, with dates/units and a weighted period value. RPM uses its own
matched daily monetary report; permission/no-data states remain distinct from
zero. Keep monthly sums tied to calendar periods and their actual coverage.
Use the [data contract](data-contract.md) for calendar
windows, gaps, units and bounded-history labels. Never disable 90/180 days merely
because the first snapshot fetched only 60 days: extend coverage on demand or
fetch the required bounded history once, cache it and identify actual coverage.
Do not call limited API history lifetime.

Keep small period summaries inside the dialog; an optional daily table starts
collapsed. Opening/changing a chart must not reset search, sort or privacy on the
main table. Preserve context on close, restore focus to the opener, and handle
Escape without leaking the dialog or blocking the page.

Use readable tabular numerals, clear selected/sort states, restrained borders,
and a table that stays usable on a narrow screen. Preserve keyboard access,
labelled controls, focus visibility and text equivalents for chart values.
Privacy mode must hide monetary amounts in the channel table, all-channel totals,
monthly columns, and every earnings/RPM surface: chart summary, plotted values, axes/tooltips and any daily table. Use a
plain **`$$$$`** placeholder; keep unavailable/permission states distinct from
zero. A revenue chart can show **Earnings · $$$$** instead of
plotting amounts. Switching privacy on must also update an already open dialog;
switching it off restores values without fetching, altering the snapshot, or
resetting chart period/filter/sort. Verify with disposable UI fixtures containing
both a nonzero amount and valid zero if the live grant has no revenue access;
never write those fixture values into the user's snapshot or request new OAuth
just to test privacy. Keep channel monetization status separate from earnings.
Mask channel identity in table and dialog as already supported. Describe Privacy
as a display aid, not access control or protection for exports.
Empty data, loading, partial permission failure and last-known stale data need
distinct concise states. A failure on one channel must not blank the whole page.

Apply the [data contract](data-contract.md) to labels and calculations. In
particular, don't copy native realtime/lifetime labels, a monetization badge
derived from failed revenue access, or YPP eligibility inferred from watch time.

## Make the controls work

When using the host's artifact builder, pass the metric/date contract along with
the UI brief and structured channel records. Inspect its result: a polished build
can still sum the last N rows instead of calendar dates or hardcode the first
snapshot's channel count/history length. Show the selected start/end dates and
actual availability; use a dynamic **Available range** choice for bounded history.
The refresh path must rediscover assigned connections and render a channel list.
When adding category/internal-name or 365-day watch-hours fields, extend the
snapshot action's validation, durable storage and readback together. An existing
action may silently strip new fields. Write/read the actual snapshot and confirm
the new values survive before relying on them in the UI; values passed only in a
builder prompt do not establish persistence.

Keep Google calls and credential refresh in the trusted backend. Send only the
assigned channels' necessary data to the artifact. Store the last successful
dated snapshot privately, so opening Library is fast and does not repeat every
Google API query. Filters/sorting/chart selection should use cached data when
possible; preserve selection and scroll position while refreshing.

Distinguish loading a saved report from refreshing Google data. Show Last checked
for pending Reach, with Check again after from `next_check_at`. Keep its check
control unavailable until that time; a local timer may re-enable it but must not
fetch. The executor also enforces this one-hour delay across periods/sessions.
Other tabs stay usable. Preserve the host's existing Update via chat handoff
where direct refresh is unavailable; opening that panel does not send a request.

Suggested-video detail rows show only a readable title linking to the canonical
YouTube watch URL, with no separate URL line or external-link arrow. Preserve exact video IDs;
never title-case or replace underscores in them. Clamp long titles to two lines
in a bounded first column and keep other metrics aligned. Escape external titles
and construct links only from valid IDs, with safe new-tab attributes. Fallback
to the exact ID/link when metadata is unavailable; core information must not
depend on hovering. Keep optional Data API title lookup separate from Analytics
snapshot times and reuse its private metadata cache across date windows.

Wire **Refresh** to a supported backend or agent action that fetches the APIs,
updates durable data, and updates the existing artifact. Disable duplicate
concurrent refreshes; show progress, success time and per-channel failures. Do
not label a button Refresh if it merely reloads unchanged embedded JSON. If the
host supports only agent-driven refresh, verify an actual supported handoff before
labelling a control **Ask Muse to update**. Inspect the current manifest/client SDK
and action contract; listing this app's existing actions alone does not establish
whether the host can dispatch an agent. An explanation-only toggle is not a
refresh or a handoff. If dispatch/prefill is unavailable, use clearly labelled
**Open chat** / **Copy update request** actions and the host's official chat
entry point, targeting the user's saved conversation and showing its name. An
explicitly chosen Analytics thread overrides the default main chat; reuse its
verified identity/link instead of creating a new thread or hardwiring `/`.
Distinguish copied text or a draft
from a request submitted by the user; never show requested/running/success just
because an instruction panel opened. Explicitly distinguish an interactive
snapshot from a live updating app until the full refresh path is verified. Never
add automatic periodic refresh merely to make the UI seem live.

Advance the displayed retrieval time only from a successful real API fetch saved
with the snapshot. Reopening the viewer, polling storage or importing old data
must not replace that time with the current clock. Preserve the separate latest
reporting date: fresh retrieval may still return delayed daily Analytics.

Avoid re-querying 730 days on every click. Fetch a bounded useful initial range,
cache/report its coverage, and extend on demand. Preserve the last valid snapshot
when a later request fails. Store operational errors privately; the frontend needs
a short actionable state, not raw OAuth responses, filesystem paths or secrets.

## Verify the delivered result

Use the actual Muse artifact viewer to check:

1. The artifact opens from its saved Library location with real assigned-channel
   data, accurate dates and no credential material in the frontend/data payload.
2. Search and category filtering work together, counts update and sorting keeps
   the filter. Test chart-icon opening/closing, metric and 7/30/90/180-day changes,
   dated tooltips and Escape. Unknown values remain unknown. Verify a chart total
   and the separate 365-day watch-hours figure against their own API responses.
   Check 24h\*/48h\*
   against their dated daily rows, independently of the selected chart period;
   include them in the dashboard's existing privacy behavior.
3. Test the refresh control in the viewer. For a dispatch path, observe the actual
   request/job in the chosen chat/backend, new API retrieval, durable snapshot
   readback and the same artifact rendering the result. For a manual chat fallback,
   test its real navigation/copy actions and the explicit submit step; do not claim
   one-click refresh. A new banner, button toast or reloaded viewer is not evidence
   of a new API request, nor is an updated clock over unchanged cached data.
4. Compare the rendered page with the bundled native references and any relevant
   newer source: compact header, tabs, collapsed info, filters and table, without
   repeated technical prose. Check a narrow viewport, chart and Privacy. Verify
   Publishing details, its own refresh/time, coverage, zero/unavailable states
   and WIB dates; tab/filter clicks must use saved data. Schedule-write controls
   must match the assignment. The screenshots use synthetic data, not live proof.
5. Reopening keeps the artifact, saved preferences and last valid snapshot, and
   the chosen chat contains the artifact card or actual reopen link.

Use temporary non-user fixtures only for states that cannot be safely observed;
keep fixture coverage distinct from live proof. Do not attach a public demo
containing private channel data. Report the stable entry point, connected count,
data cutoff and any feature not yet verified. The maintainer owns reusable skill
changes; Muse may implement the private dashboard and report lessons, without
rewriting this shared skill package on its own.

## Manual refresh and dated snapshots

Additional cards are explicit opt-in groups: Demographics (age + gender),
Viewing habits (devices + subscriber watch time), and Top videos. Each has
Load data before its first fetch, then its own Refresh and retrieval/range label.
Opening the modal, switching periods or refreshing the header never fetches
these groups from Google. Read saved snapshots only; a missing period stays
unloaded. Do not introduce a Refresh all details cascade. Group compatible cards
so age/gender share one query and device/subscriber watch time share one query.
Top videos fetches five ranked rows and batched metadata only when requested.
Average video length is a separate compact Overview card with its own Load /
Refresh and known/returned video count; it is not the average of the top five.
Preserve bounded Top 200 and missing-duration coverage when applicable.
Use one thin primary strip before the graph and supporting averages/Reach after
it, rather than large cards. Keep counts inline and put verbose definitions/
retrieval times in tooltips. Graph coverage is a concise footer, not duplicate
large totals. Topic tabs and metric buttons are separate navigation levels.
Keep one stable responsive dialog size for every tab/state, a persistent header/
tab bar and a scrolling body; wide tables scroll within that body. Show the
Engaged/Views same-period percentage inline, with unavailable zero denominators.
Last 48h* means two reported dates, with actual dates and a visible non-realtime
cue. Missing Impressions/CTR cells use the cached state/reason instead of a bare
dash; distinguish no saved row, zero impressions and a valid 0.0% CTR.
Overview shows total subscribers separately from gained/lost/net, and exposes
the subscriber graph even when an old cache needs an explicit refresh. Views
and Engaged views are two simultaneous lines with a shared tooltip, not a mode
picker. Its Impressions/CTR cards only read saved Reach data and expose Pending,
unloaded or partial coverage; use Reach's own control to check Google.
Preserve these controls and cache semantics in the Muse artifact/executor.

Content is a separate per-channel modal tab for available uploads, beyond the
top-five summary. Use the current native Content captures: compact Catalog /
Performance / Earnings controls with independent Load/Refresh and timestamps,
one loaded-page search/sort bar, a dense scrolling video table and explicit
Load older uploads. Keep catalog collection (50 IDs max per action), page metrics
and money separate in the executor as well as the UI. Opening Content is a cache
read, not setup-time permission to scan every video. A period change reads its
saved performance or stays unloaded; page navigation over loaded pages is cached.
Per-video impressions/CTR read the existing Reach index. Comments are current
catalog totals, not selected-period comments. Follow development-principles and
the data contract for exact fields, privacy, ownership and query combinations.

Content has one page-local header Load/Refresh: Performance plus already-loaded
Earnings for the selected page/period, combined in one compatible query when
both requested and granted, with one Catalog page first only if absent.
Catalog refresh remains explicit for new uploads. Keep Earnings visible near
Views/Engaged views with Not loaded/permission/empty states; show Engaged share
as a local same-period percentage. Missing-period text directs the user to
Refresh Content rather than leaving unexplained blanks. Pin the video column
and table header, keep a top horizontal scrollbar with left/right controls, and
put page navigation above the bounded table. Panning is local and remembers
its position without refreshing data.
Content defaults to Available (bounded up to 730 days), independently from other
topics' 30d window; restore each period/custom date selection when switching.
Cache Google's direct period aggregate, rather than claiming exact smaller-range
totals from daily sums/weighted averages. Group refreshes remain independent;
an access/metric rejection of the combined query allows one basic fallback only.

Keep main actions in a compact subtly framed group with a bright teal primary
Refresh and a timestamp below the action row, Tips behind an explicit
toggle, filters in one responsive row, and earnings totals in a thin strip with
channel coverage visible and longer cutoff details in tooltips. Display the
connected account beside channel identity in Statistics and report headers,
with Studio links and full Privacy handling. Show Gmail/Googlemail values,
other saved identities as Brand, and missing metadata as Email not saved.
The project manager in API information is a separate field.

Keep Refresh overview at page level and Refresh [current report] inside the
modal. Detail caches survive channel/tab changes and overview refresh; old
successful snapshots are displayed with their original dates until an explicit
report refresh or an uncached range is requested. Country/search/graph cursor
interactions reuse data. Keep Updated and Data through near the report; use
Requested through if the API does not disclose an actual last day. API/project,
recorded project manager, request estimates and last usage belong in a clickable
info panel, not a confirmation dialog or a wall of text. Disable duplicate
refresh while running, retain last good data on failure, and keep per-component
coverage honest. Apply the same behavior in an independent Muse executor and
its existing artifact. For an artifact that cannot call its backend directly,
state how its refresh action dispatches to the assigned Analytics chat; never
make a snapshot reload look like a new API fetch.
