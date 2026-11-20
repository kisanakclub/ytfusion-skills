# Private Muse channel Analytics dashboard

## Deliver an app the user can reopen

Use Muse's current artifact and client-surface documentation to choose a
supported private interactive app. On the inspected Muse host, the supported
surface is a fullstack artifact (`artifact.create_web_fullstack`), with server
logic and persistent database. Verify the current documentation and private
delivery before creating it; keep credential access in trusted VM execution.

Name the persistent artifact for the instance's channel Analytics and keep it in
**Library**. Create a separate Analytics side chat when requested, and give that
chat the dashboard link/context for follow-up analysis. On the inspected host,
artifacts do not have their own built-in side chat; these are separate surfaces.
The main chat can announce completion once and link to them. If direct side-chat
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

Read the installed `src/templates/channel_statistics.html` before designing.
Preserve its recognizable compact channel table and dark neutral/teal visual
language, rather than replacing it with a generic wall of oversized cards.
Use English for dashboard labels by default, matching the owner's UI preference
and native channel-stats; keep chat replies in the user's language. An explicit
UI language choice overrides that default. A useful starting layout is:

- Header: Channel Analytics, last successful update, reporting coverage, privacy
  toggle and **Refresh**. Keep secondary explanations in a short expandable note.
- Toolbar: search channel name/internal name, saved category/group filter when
  such data exists, and period selector. Use 30 days initially; retain user choices.
- Small summary strip: assigned/visible channels, current subscribers, selected
  period views and watch hours. Show what is covered rather than fake totals.
- Main sortable table: internal name if available, avatar/name/handle, subscribers,
  videos, **24h\*** and **48h\*** views, selected-period views, watch hours and
  trend sparkline/detail action. The short-period columns follow
  [latest reported days](data-contract.md#latest-reported-day-and-two-day-columns),
  with reporting dates and a compact visible note that they are not realtime.
  Available earnings are secondary; use a clear unavailable label when access is
  missing. Current worker status may be shown only when a native source exists.
- Channel detail panel/dialog: larger daily chart, date/metric selector, exact
  coverage, period totals and meaningful comparison where available. Keep channel
  identity visible when switching charts. Optional video breakdown should use real
  supported queries when requested, not fabricated starter data.

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

Keep Google calls and credential refresh in the trusted backend. Send only the
assigned channels' necessary data to the artifact. Store the last successful
dated snapshot privately, so opening Library is fast and does not repeat every
Google API query. Filters/sorting/chart selection should use cached data when
possible; preserve selection and scroll position while refreshing.

Wire **Refresh** to a supported backend or agent action that fetches the APIs,
updates durable data, and updates the existing artifact. Disable duplicate
concurrent refreshes; show progress, success time and per-channel failures. Do
not label a button Refresh if it merely reloads unchanged embedded JSON. If the
host supports only agent-driven refresh, label the real action **Ask Muse to
update** and make that handoff work in the dedicated chat. Explicitly distinguish
an interactive snapshot from a live updating app until the full refresh path is
verified. Never add automatic periodic refresh merely to make the UI seem live.

Avoid re-querying 730 days on every click. Fetch a bounded useful initial range,
cache/report its coverage, and extend on demand. Preserve the last valid snapshot
when a later request fails. Store operational errors privately; the frontend needs
a short actionable state, not raw OAuth responses, filesystem paths or secrets.

## Verify the delivered result

Use the actual Muse artifact viewer to check:

1. The artifact opens from its saved Library location with real assigned-channel
   data, accurate dates and no credential material in the frontend/data payload.
2. Search/filter and sorting work; opening a channel chart and changing periods
   shows the corresponding series and correct totals. Unknown values remain
   unknown. Verify a real total against the backend response. Check 24h\*/48h\*
   against their dated daily rows, independently of the selected chart period;
   include them in the dashboard's existing privacy behavior.
3. The documented Refresh/Ask Muse action really updates the same artifact and
   records a new successful API retrieval time. A refreshed viewer alone is not
   evidence of a new API request.
4. Reopening keeps the artifact, saved preferences and last valid snapshot, and
   the separate Analytics side chat or actual route to it is accessible.

Use temporary non-user fixtures only for states that cannot be safely observed;
keep fixture coverage distinct from live proof. Do not attach a public demo
containing private channel data. Report the stable entry point, connected count,
data cutoff and any feature not yet verified. The maintainer owns reusable skill
changes; Muse may implement the private dashboard and report lessons, without
rewriting this shared skill package on its own.
