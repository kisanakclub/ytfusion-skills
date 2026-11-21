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

Read the installed `src/templates/channel_statistics.html` before designing:
header/filter/table/modal markup, final CSS overrides and the filter/sort/chart
functions. Use its actual composition, density and interactions as the baseline.
When the user supplies a screenshot, give that reference to the artifact builder
as well as the source-based brief. Keep private screenshots out of this shared
repo; their sample channels/values are not new account assignments or app data.
Use English for dashboard labels by default, matching the owner's UI preference
and native channel-stats; keep chat replies in the user's language. An explicit
UI language choice overrides that default. Follow the native hierarchy:

- Compact header: title/icon and a small last-update line at left, Privacy and
  the supported refresh action at right. Use the native restrained divider/accent.
- One collapsed **Info & Tips** row for freshness, permissions and data definitions.
  Do not fill the default page with repeated date/source paragraphs, revenue
  warning panels, implementation details or four large summary cards.
- One filter toolbar: Category dropdown, Search channels and a visible count.
- The channel table is the main content. Follow native column order: internal
  name when assigned, YouTube Channel (avatar/name/handle/link), Subs, Videos,
  Watch Hrs (365d), 24h\*, 48h\*, Chart, Earnings 24h/Earnings, and operational
  Status when a real source exists. Keep numbers aligned and typography compact.
  Use chart icon buttons in dedicated cells rather than hiding charts behind a
  generic Detail button and a long inline report.
- Put periods, metric selection, detailed summaries and any optional daily table
  inside the chart dialog. A 30-day initial graph is useful; preserve later choices.

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
Offer **7d / 14d / 30d / 90d / 180d / Available range**, with Views and Watch time
working from real dated series. Earnings can have a separate native-style chart
action when access exists. Use the [data contract](data-contract.md) for calendar
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
Privacy mode should mask channel identity and sensitive amounts in the visible
view; disclose it as a display aid, not access control or protection for exports.
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
4. Compare the rendered default page to the native/source screenshot: compact
   header, collapsed info, filter toolbar and table; no unnecessary summary-card
   strip, revenue banner or repeated technical prose. Check a narrow viewport
   without clipping chart controls or causing whole-page horizontal overflow.
5. Reopening keeps the artifact, saved preferences and last valid snapshot, and
   the chosen chat contains the artifact card or actual reopen link.

Use temporary non-user fixtures only for states that cannot be safely observed;
keep fixture coverage distinct from live proof. Do not attach a public demo
containing private channel data. Report the stable entry point, connected count,
data cutoff and any feature not yet verified. The maintainer owns reusable skill
changes; Muse may implement the private dashboard and report lessons, without
rewriting this shared skill package on its own.
