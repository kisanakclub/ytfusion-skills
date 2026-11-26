# Publishing overview and schedule actions

Read this for the Publishing tab or questions about actual publication patterns
and scheduled YouTube videos. Follow the assigned source's
docs/channel-publishing.md, src/channel_publishing.py, matching src/app.py routes,
and the page's Publishing partial/CSS/JS. View the bundled
[UI references](ui-reference.md) for composition.

## Display and dates

Keep Statistics and Publishing as two tabs in one persistent private artifact,
sharing category/search and Privacy while preserving their separate data,
refresh state and last-successful check time. Opening a tab, expanding cached
details, filtering or inspecting a chart must not trigger a Google refresh.

The Publishing summary follows native column order:

Channel | Last published | Typical interval | Typical time · WIB |
Next publish | Scheduled | Last scheduled | supported Action.

Use channel avatars/name/internal name, with privacy masking. Zero scheduled
videos is a real zero and can still expand private/unlisted details; missing
data is unavailable. Expand to Scheduled and Private / unlisted lists, with
titles, dates, Studio links, reviewed-upload coverage and an explicit Older
uploads action. Failed refreshes retain the previous result and its check time.
Do not present counts as the whole channel when only some pages were reviewed.

- Last published is the latest publication timestamp among reviewed public
  videos. Queued jobs not yet uploaded to YouTube do not appear here.
- Scheduled means a private video with a future publishAt. Next/last schedule
  are the earliest/latest such timestamps. A passed schedule is not proof of
  successful publication; a fresh status read establishes that.
- Typical interval describes observed public history, not a target queue setting.
  Reuse up to 10 newest reviewed public videos; require at least six videos.
  Native shows the middle 50% of intervals and median, with mean/full range and
  sample size in a tooltip. Fewer samples show Not enough data.
- Typical time uses those public timestamps in Asia/Jakarta, with the same
  minimum sample. Reuse the native circular-clock calculation: a cluster around
  midnight must stay around midnight. Show the typical window, overnight cue,
  median and sample size, rather than averaging 23:00 and 01:00 into noon.
- Publishing dates/editor times use WIB (UTC+7), regardless of browser/VM
  timezone. Statistics daily reports and earnings months remain Pacific dates.

## Reads and refresh

Native endpoints are GET /api/channel-publishing and
POST /api/channel-publishing/refresh with a channel and optional more flag.
Use an existing authenticated native session when assigned native operation.
In agent_executor mode, use existing assigned credentials through the trusted
backend and the native algorithm as a reference; do not start YtFusion or
forward native relative URLs into the artifact.

Use YouTube Data API, not Analytics reports, for this overview. Reuse the
uploads playlist ID; otherwise resolve it with channels.list. Read
playlistItems.list(maxResults=50) then batch videos.list for those IDs. Continue
only until a page contains a public video or no next page remains. Repeated
page tokens must stop safely. Older uploads explicitly adds one page. A normal
refresh starts again at the newest page. Preserve per-channel partial coverage,
failures and assigned-channel isolation; use bounded concurrency and coalesce
duplicate refreshes. Merely enabling the Data API does not prove account access.

Use the dashboard's supported real refresh path or verified chosen-chat handoff.
Maintain separate Statistics and Publishing snapshots/timestamps in durable
storage. A new check time requires a successful upstream read, not a tab click.
Inspect the current route/response before relying on the endpoint names above.

## Editing a schedule is a separate operation

Reading Publishing data or building the dashboard does not authorize changing
YouTube. A reporting-only artifact can provide a supported Studio link; leave
schedule editing unavailable until an actual edit is assigned and implemented.
Do not copy an Upload link that points to an absent native app.

When schedule editing is assigned, follow the native safeguards: fresh-read the
video with the matching channel credential, verify ownership, private status
and expected existing schedule, then require the new timestamp at least one
minute ahead. Preserve other writable status fields. Native uses
POST /api/channel-publishing/schedule; retain its login/origin checks. An executor
needs its own trusted backend action with the same checks and a supported grant,
not a frontend credential or a fake success state.

Reject stale/conflicting edits, refresh the relevant saved row after success and
keep the same artifact. Editing an uploaded video's YouTube schedule does not
reschedule local/VPS jobs awaiting upload. Setup does not authorize enabling a
write scope, reauthentication, an upload, publication or a recurring schedule.
