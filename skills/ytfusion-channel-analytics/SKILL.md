---
name: ytfusion-channel-analytics
description: Read connected YouTube channel statistics, video catalogs and publishing schedules, and build or update a private Muse dashboard following current YtFusion channel-stats and bundled visual references. Use for channel comparisons, video performance, views, watch time, revenue, charts and publication cadence; schedule edits require a separate assigned action.
---

# YtFusion Channel Analytics

Respond in the user's language. Read connected channels using the existing
instance assignment and credentials. Build the requested report or dashboard;
do not repeat account setup when a valid connection already exists.

## Choose the surface

For dashboard setup or development, follow [the development principles](references/development-principles.md)
and the assigned source's `docs/CHANNEL_STATISTICS_PRODUCT_PRINCIPLES.md`.
Adding metrics must preserve manual collection boundaries and cached navigation.

- For a quick question, return the requested figures, dates and a short
  explanation. Do not create an app for every statistics question.
- For a reusable UI, read [dashboard](references/dashboard.md) and open the
  [visual references](references/ui-reference.md) before briefing the builder.
  Follow [source CSS reuse](references/ui-reference.md#reuse-the-current-native-css):
  use the assigned checkout's actual styles as artifact build inputs, with
  matching component classes. Screenshots verify the result.
  On Muse, prefer one private interactive artifact in Library, linked from the
  user's chosen chat.
  Keep coordination in the main chat unless the user requests a separate thread.
  Reuse that artifact on later requests rather than creating another dashboard.
- For data collection in either case, read [data contract](references/data-contract.md)
  and the assigned source's `src/templates/channel_statistics.html`, its included
  partials/assets and handlers. Statistics uses `src/channel_analytics.py`;
  Publishing uses `src/channel_publishing.py` and
  [publishing](references/publishing.md). Inspect the relevant current source
  even when a saved screenshot or previous dashboard already exists.

## Work from the assigned connections

1. Reconcile the saved assignment with actual connected channel IDs. Report only
   channels assigned to this instance or explicitly selected by the user. Resolve
   duplicate display names by ID privately. A new connected channel must appear
   after refreshing discovery without rewriting the skill or hardcoding accounts.
2. If the native app is running, use its authenticated statistics/cache endpoints
   after inspecting their current contract. For a Muse API executor, use existing
   channel credentials in the VM backend and read Data/Analytics APIs directly.
   A running YtFusion server, public domain, or connected Mac is not required for
   an executor that already has valid credentials and network access.
3. Refresh within the task scope, keep the last successful snapshot per channel,
   and isolate channel failures. A connected account is not proof that Analytics
   or revenue permissions are available. Distinguish absent data from zero.
   Optional Demographics, Viewing habits, Top videos and Average video length stay cache-only
   until their own Load/Refresh is requested; a general refresh must not expand
   into all optional reports. Follow the data contract and bundled UI references.
4. If a required connection/API/grant is actually missing, explain that precise
   blocker. When installed, reuse `ytfusion-operations` for account/project setup;
   do not create clients, broaden grants or reauthenticate merely to build a UI.

## Deliver and maintain

For a dashboard, deliver its stable reopenable location and verify it in the
user-facing viewer, including a channel selection, date change and refresh.
State whether refresh really fetches new API data or only reloads a snapshot.
Persist the artifact identity, channel selection and data-source mapping in
private instance context so future chats update the same dashboard. Changing the
preferred chat changes delivery/context, not the artifact identity or running job.
Record the source/skill revisions used to implement the dashboard. After an
assigned update, compare the changed page, included assets and data contracts
with the existing artifact, then update that artifact within the assigned scope.
Pulling a repo or reinstalling a skill alone does not migrate a Muse dashboard.

Read-only reporting and cache updates do not authorize uploads, channel/video
edits, public sharing, new account access, or recurring tasks. When the user asks
for scheduled refresh, use the host's supported scheduler and verify the task;
an open artifact or chat is not a background scheduler.

Report data coverage, last successful retrieval, unavailable metrics and any
remaining blocker. A screenshot or mockup does not prove a working API-backed
dashboard. Keep tokens, client secrets, source credentials and private runtime
ledgers out of frontend bundles, exports, chat and this shared skill repository.
