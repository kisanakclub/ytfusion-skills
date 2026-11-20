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
| `fetch_channel_statistics`, `fetch_channel_analytics` in `src/app.py` | Channel credentials, Data API identity/totals, Analytics reports and aggregation |

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
| `subscribersGained`, `subscribersLost` | Optional period metrics; net growth is gained minus lost for the same period. Keep separate from current subscriber total. |
| `averageViewDuration` | Optional average in seconds. Query the aggregate for the selected period or weight compatible components correctly; do not average daily averages unweighted. |
| `estimatedRevenue` | Optional estimate, with currency and coverage. Requires appropriate granted access; failure/absence is not proof of no monetization and not revenue zero. |

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

### Native compatibility caveats

The inspected native code requests roughly 730 days, calls that sum
`views_all_time`, and derives `views_24h`/`views_48h` from the last one/two
returned daily rows. Its formatted chart labels omit the year. It also folds
several revenue failures into `is_monetized=false` and watch-time failures into
zero. These fields are compatibility inputs, not trustworthy semantics for a
new dashboard. Label them as bounded/latest reported-day data where provable;
request a dated series when exact period calculations are needed. Do not guess
missing years or silently relabel them as realtime/lifetime. Treat ambiguous
revenue, watch-time failures and incomplete provenance as unavailable. This skill
does not authorize patching or restarting the native app to fix those caveats.

## Access and recovery

Verify YouTube Data API and YouTube Analytics API are enabled in the actual
credential's project, and inspect granted scopes plus real API results. Normal
Analytics commonly uses `yt-analytics.readonly`; monetary reports need appropriate
monetary access such as `yt-analytics-monetary.readonly`. Current Google docs list
additional authorization nuances: verify the actual failure before prescribing
another login. Enabling an API does not expand an existing token's grant.

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
