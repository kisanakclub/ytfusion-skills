# Channel statistics and Analytics data contract

## Native source and endpoints

Inspect the installed version before relying on field names. The reference
implementation has these entry points:

| Entry point | Purpose |
| --- | --- |
| `/channel-stats` | `src/templates/channel_statistics.html`: cached channel table, search/category filter, privacy toggle, sortable metrics and chart detail |
| `GET /api/channel-statistics` | Cache payload: `success`, `channels`, `last_updated`; no cache is an empty list, not proof of no connected channels |
| `POST /api/channel-statistics/refresh` | Fetch connected native channels, write cache, return channel results; per-channel errors may coexist with top-level success |
| `GET /api/status`, `GET /api/categories` | Native worker/category context used by the page; optional when the executor does not run native workers |
| `fetch_channel_statistics`, `fetch_channel_analytics` in `src/app.py`; `src/channel_analytics.py` | Channel credentials, Data API identity/status/totals, dated independent Analytics reports and calendar aggregation |

Use an existing authenticated session, preserve origin/CSRF checks and never import
`src/app.py` into a helper just to call it. Inspect responses for per-channel
and per-metric errors. Native refresh can fetch more channels than assigned: keep
unassigned records out of the artifact's server response and exported data.

For an independent executor, inventory actual assigned connections instead of
assuming native folders exist. Keep credential loading/refresh in the trusted
backend. Use `channels.list(mine=true)` to reconcile channel identity when needed;
cache it rather than requesting identity on every filter click. Read reports from
`https://youtubeanalytics.googleapis.com/v2/reports` with the matching channel's
credentials. Bind the credential to the resolved channel ID, not its display name.

## Metrics and honest labels

| Data | Meaning and presentation |
| --- | --- |
| Data API `subscriberCount`, `viewCount`, `videoCount` | Current reported channel totals, not growth within the selected period. Honor hidden subscriber status; do not imply exact subscriber precision. |
| Analytics `views`, dimension `day` | Daily views within explicit start/end dates; sort and join by ISO date. This is not Studio's rolling realtime 48-hour report. |
| `estimatedMinutesWatched` | Divide by 60 for hours; preserve precision before formatting. Show the exact period. This alone does not establish YPP-eligible public watch hours. |
| Native-style Watch Hrs (365d) | Query the actual 365-day period with the existing grant, record its dates/availability and convert minutes to hours. Do not relabel a 30/57-day sum as a 365-day query. Failure is unavailable, not zero. Do not copy a Ready/YPP-eligible badge from a simple hours/subscriber threshold. |
| `subscribersGained`, `subscribersLost` | Optional period metrics; net growth is gained minus lost for the same period. Keep separate from current subscriber total. |
| `averageViewDuration` | Optional average in seconds. Query the aggregate for the selected period or weight compatible components correctly; do not average daily averages unweighted. |
| Data API `status.isChannelMonetizationEnabled` | Use the explicit Boolean, when returned by `channels.list(part=snippet,statistics,status,mine=true)`. `true` = **Monetized**, `false` = **Not monetized**; absent = **Unknown**. Show these in a dedicated Monetization column. Do not infer membership from revenue, ad presence or hours/subscriber thresholds. |
| `estimatedRevenue` | Optional estimate, with currency and coverage. Requires the granted `yt-analytics-monetary.readonly` scope and YPP access. Failure/absence is not proof of no monetization and not revenue zero. Valid returned zero stays zero. It is not finalized AdSense payments. |

Use supported metric/dimension combinations from the current channel-report
documentation. Keep optional monetary queries separate so an access failure or
slower revenue availability does not discard newer views/watch-time data. Do not
attempt every possible Analytics dimension for a simple dashboard.

### Dates, gaps and comparisons

- Analytics reporting days use Pacific time (`America/Los_Angeles`, including
  daylight saving), not the VM or user's local calendar. Display retrieval times
  in the user's timezone, separately from the reporting-day timezone.
- Default to a 30-day calendar selection ending yesterday in reporting time unless
  a saved/user-selected period exists. Show requested start/end and actual latest
  returned report date. The API can lag: a successful request made today does not
  imply data through today or yesterday. Revenue can have a different cutoff.
- Filter by calendar boundaries, not the last N returned rows. Preserve ISO dates
  including the year in stored/chart data. Join views and revenue by date rather
  than array index. Gaps remain unknown unless the response contract establishes
  zero; never fill unavailable recent days with zero or draw them as a crash.
- Use 7/14/30/90/180-day and custom selections as useful controls, not separate
  queries on every click when the cached dated series already covers them.
  Fetch additional coverage only when necessary. Label bounded history by its
  range; reserve Lifetime for genuinely complete history or Data API totals.
- Compare equal calendar spans with the same filters and coverage. Identify
  partial comparisons; do not announce growth from mismatched cutoffs. A zero
  prior value needs a new/no-baseline label, not an infinite percentage.
- Across channels, show selected count and valid reporting count. Do not sum
  unknowns as zero, mix currencies, or silently combine different report dates.

### Latest reported day and two-day columns

For channel-stats-style short summaries, expose sortable **24h\*** and **48h\***
views columns. Keep a compact visible note: **Latest reported day / two days ·
not realtime**, and show actual per-channel reporting dates in subtext or tooltips.
These are compatibility labels for daily reports, not rolling hour windows.

- Derive each channel's latest date from its full dated daily series, independently
  of the chart's selected 7/14/30-day window. 24h\* is that day's views.
- For 48h\*, require that latest date and the immediately preceding calendar date
  in reporting time. Sum those two available daily values, preserving valid zeros.
  A missing preceding date means unavailable or explicitly partial coverage, not
  zero; do not silently combine nonconsecutive rows. If no report exists, both
  summaries are unavailable with the channel's data state.
- Preserve exact dates alongside values when refreshing. Different channels may
  have different cutoffs; neither sorting nor changing the chart period should
  change which dates these columns summarize. Do not infer hourly bars from them.

### Native version 2 contract

After updating source, inspect `src/channel_analytics.py` and the actual payload.
Native `analytics.report_version == 2` includes:

- `reports.views`, `reports.earnings`, `reports.watch_time`, each with its own
  `status`, `error`, ISO `dates`/`values`, `requested_start`, `requested_end`,
  `latest_reported_day`, `reported_days`, `available_total` and calendar `totals`.
- Failure states distinguish `permission_required`, `api_disabled`, `unauthorized`,
  `forbidden`, `quota_exceeded`, `unavailable` and legitimate `no_data`. A generic
  403 does not prove non-YPP. A watch-time failure remains null, not zero.
- Latest-day `views_24h`/`earnings_24h`, consecutive-day `*_48h`, and 7/14/30/90/180
  calendar totals. A total with missing days is null. A graph may sum reported
  days only if partial coverage is clearly labeled; do not describe it as a
  complete calendar total.
- `reports.earnings.periods.this_month` / `last_month`: Pacific calendar boundaries,
  `value` (sum of reported daily API revenue), requested dates, latest reporting
  day, `reported_days` / `expected_days`, `complete` and status. Flat fields
  `earnings_this_month` / `earnings_last_month` mirror these values. They are not
  rolling 30-day windows; missing reports/grants remain null. A valid zero remains
  zero. On the first Pacific day of a month there may be no completed day yet.
- `reports.rpm` / `rpm_engaged`: derived Estimated RPM using Views / Engaged views
  respectively. A separate joint daily query requests
  `estimatedRevenue,views,engagedViews`, so its numerators and denominators have
  matching reporting dates/filter/currency. Its failure must not discard the
  independent earnings history/month totals. Each report keeps `dates`, `values`,
  `revenue_values`, `denominator_values`, basis, cutoff and status. Missing or zero
  denominators yield null. Revenue zero with a positive denominator yields zero.
  For a selected period, compute **sum(matched revenue) / sum(matched denominator)
  × 1000**; never average/sum daily RPM values. Keep the basis explicit. Shorts
  use Engaged views; a mixed channel estimate is not guaranteed to match Studio's
  RPM. Do not substitute CPM or claim RPM is returned directly by the API.
- `views_available` / `earnings_available` are bounded returned-data sums, up to
  730 days. Views use `chart_labels`/`chart_values`; revenue uses independent
  `earnings_chart_labels`/`earnings_chart_values`. Never align these by array index.
- Channel-level `is_monetized` comes only from the Data API status field and is
  nullable. It does not come from `analytics.is_monetized` or revenue access.

The status field is exposed by Google's Discovery schema and generated Python
client documentation; it may be absent from responses or narrative REST docs.
Keep absence unknown and re-check current schema if support changes. It does not
state payment eligibility, ad serving on a particular video, or payout amounts.

Older native caches may contain `views_all_time` for only ~730 days, short labels
without years, inferred `analytics.is_monetized=false`, or watch-time errors as
zero. Do not reuse those guesses. Refresh the native cache after updating, or
retrieve a dated series in the executor without starting native YtFusion. Updating
this skill alone does not authorize native source edits, restarts or new grants.

## Access and recovery

Verify YouTube Data API and YouTube Analytics API are enabled in the actual
credential's project, and inspect granted scopes plus real API results. Normal
Analytics uses `yt-analytics.readonly` (the monetary scope also covers user-activity
reports). Estimated channel revenue requires the exact
`https://www.googleapis.com/auth/yt-analytics-monetary.readonly` grant. The same
YouTube Analytics API serves it: no additional GCP API/library, client JSON or
AdSense API is required for this metric. Enabling an API or declaring a consent
scope does not expand an old token's actual grant. Verify the actual failure
before prescribing another login.

When the user requests earnings and the grant is missing, explain one-time
reauthorization with the existing client/channel; preserve working credentials
until it succeeds. Native v2 exposes **Enable earnings** in channel-stats and uses
`/re-authenticate/<internal-name>?earnings=true`. Ordinary Add Channel does not
require monetary access; regular reauthentication preserves an already granted
monetary scope. An executor must use its own supported reconnection/handoff and
reimport the authorized connection when needed; a native relative URL in a Muse
artifact would point to the wrong host. Do not auto-grant Google access or promise
revenue on a channel that is not eligible. Keep upload/normal statistics usable
without the optional monetary grant.

Classify disabled API, insufficient scope, expired/revoked credentials, wrong
channel, network error, and legitimate empty data separately. Keep unaffected
channels and valid old snapshots visible with their timestamps. Use bounded
retry/backoff for transient network/429/5xx responses, then show the error and
last successful data; avoid repeated login loops or a dashboard that spins forever.

## Authoritative references

- [Reports query, available dates and currency](https://developers.google.com/youtube/analytics/reference/reports/query)
- [Reporting dimensions and Pacific days](https://developers.google.com/youtube/analytics/dimensions)
- [Metrics and their units](https://developers.google.com/youtube/analytics/metrics)
- [Supported channel reports](https://developers.google.com/youtube/analytics/channel_reports)
- [Authorization](https://developers.google.com/youtube/reporting/guides/authorization)

- [Data API generated channel status schema](https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.channels.html)
- [Current YouTube Discovery schema](https://www.googleapis.com/discovery/v1/apis/youtube/v3/rest)

- [YouTube RPM definition and view bases](https://support.google.com/youtube/answer/9314357?hl=en)
