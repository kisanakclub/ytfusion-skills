# Statistics and Muse dashboard development principles

When extending the dashboard or setting up a new Muse instance, read the assigned
source's `docs/CHANNEL_STATISTICS_PRODUCT_PRINCIPLES.md` as the product baseline.
It is linked by source AGENTS.md. If the source is unavailable, preserve these
essential rules together with the bundled data/dashboard/UI references:

- Display/cache reads and Google collection are separate operations. Optional
  cards and Content groups start with Load data, then their own Refresh. Opening
  tabs, changing dates, filtering, sorting and revisiting saved selections must
  not trigger optional Google requests or a full catalog scan.
- Keep main overview, optional detail groups, Content Catalog, Content Performance,
  Content Earnings and Reach independently refreshable and timestamped. No
  Refresh all details cascade, automatic polling or setup-time catalog scan.
- Batch compatible metrics and video IDs. Catalog reads one page of at most 50
  uploads plus its metadata batch. Performance uses one multi-video Analytics
  query for that page/period. Earnings stays optional; combine it with Performance
  when both requested and granted, keeping separate states. An access/metric
  rejection allows one basic fallback, not retries on quota/disabled API/5xx.
  Read impressions/CTR from the same saved Reach imports.
- Show dates, missing/partial/bounded coverage, actual per-API usage and stale
  success honestly. Unknown is not zero; a permissions failure is not non-YPP.
  Use the matched project/client and keep credentials in the private backend.
- Views and Engaged views are two simultaneous chart lines, not a mode picker.
  Subscriber totals and gained/lost/net are different metrics. Original runtime,
  average viewing duration and average viewed percentage are different metrics.
- Content can eventually browse all available uploads through explicit older-page
  loads; loaded-page search/sort must not pretend to cover unloaded videos.
  Do not request one Analytics report per row, fetch money with every refresh,
  or initialize Reporting just because an impressions column is visible.
- Default Content to Available (bounded up to 730 days), independently from other
  topics' 30d period/custom dates. Cache Google's exact period aggregate; daily
  sum/reweighting can differ from that aggregate and adds pagination requests.
- Preserve connection/period/video-selection cache ownership, old successful
  reports on failure and late-result guards. Cache-only reads cannot renew an
  expired credential or silently refresh expired resource metadata.
- Build a compact responsive English UI from the current synthetic references.
  Reuse the assigned source's actual CSS/inline theme in artifact build inputs,
  preserving native type, theme, dimensions and cascade. Generated style assets
  are refreshed from the app on an assigned update, not maintained as another
  skill stylesheet. Follow the UI reference's source CSS procedure and verify
  same-size screenshots/computed styles as well as functionality.
  Lead Overview with Views, Engaged views, Watch time and subscriber change, then
  the chart; averages/runtime/Reach sit below. Keep counts inline and secondary
  definitions/retrieval dates in tooltips, without duplicate large footer cards.
  Topic tabs are Overview/Content/Reach/Traffic/Audience/Revenue; graph metrics
  stay within their topic. Earnings/RPM belong to Revenue, Impressions/CTR to
  Reach, and country/demographics/viewing groups to Audience.
  Keep Privacy in open tables/charts, links and money. Metadata/comments and
  period performance have different dates; preserve that distinction.

For source-maintenance work, update the relevant skill contract/captures in the
same change. For a new instance, implement these controls in its actual backend
and viewer, not just in a planning document. For an existing instance, preserve
its artifact identity, assignment, credentials and jobs; a repo pull or a revised
skill does not migrate the executor/dashboard. Deployment requires the assigned
update task. Keep fixture, live API, Shared export and host deployment evidence
separate. Routine Muse operations do not gain permission to push skill source.
