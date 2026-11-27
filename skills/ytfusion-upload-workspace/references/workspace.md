# Drive Inbox, Upload Queue and History in Muse

## Authority and first useful proof

Keep the existing `native_app` / `agent_executor` choice. In agent mode, the native
source defines behavior and UI references; its authenticated `/api/hds/yt_upload`
routes require a running native backend and are not a standalone API library.
Do not import `src/app.py`, copy Private engines into a skill, fabricate native
projects, or start the native service merely to reproduce the UI.

Use the actual supported Space storage/actions and worker invocation facilities.
Inspect their current documentation before selecting a bridge. A Space can
persist interactive data; this does not by itself establish that the worker VM
can read it or that a Space action can launch a long-running transfer. Conversely,
an older artifact's manual chat refresh is not evidence of a platform-wide limit.
No public tunnel or new grant is part of workspace setup.

The initial proof is read/preparation only: list assigned Drive packages, save an
explicitly selected real package as a draft/held job, reload the viewer, read it
through the executor's supported dry-run path and confirm matching IDs/settings.
The dry-run does not download video contents, insert/update a YouTube video,
write Drive history, delete files, set `execution_authorized`, or create a
recurring schedule. It does not consume or mark the job complete. Use existing
disposable fixture rows for mutation failure checks; keep live selections held.

If no direct worker bridge is available, retain the useful Inbox and persistent
held queue. Implement a bounded, explicit agent-mediated reconciliation from
the durable store if the host supports it, then show its actual acknowledgement
and time. Explain the concrete missing automated leg. Do not call manual transfer
automatic, silently mirror jobs to unrelated files, or require the user to copy
tokens/technical JSON. A script that loads a private export is only an export
reader until actual supported retrieval and round-trip identity are verified.

## Drive Inbox

Read the connected Drive workspace using its existing connector/API. Inspect the
binding/root and include only assigned sources. Read package metadata, declared
thumbnail and receipt history; listing is not a reason to download large videos
or run media generation. Preserve measured duration when present and leave it
unknown otherwise. Source profile/batch labels do not identify the destination
YouTube channel.

Retain stable Drive file IDs plus version/fingerprint, workspace/package identity,
manifest/video/thumbnail references, source folder/profile/batch, title, size,
duration choice/measurement and upload history evidence. Keep credential-bearing
download URLs backend-only; render safe host-served thumbnail previews or an
honest placeholder. A short-lived thumbnail URL can expire independently of the
source; do not convert its failure into a missing-video state.

Follow native facets: **All**, **Ready**, **In queue**, **Uploaded**, **Needs action**;
search title/source/profile/batch; source folder/profile/batch filters; sort and
selection count. Filtering changes the visible list, never actual queue order.
Open the Inbox on **Newest in Drive**. Sort by the creation time of the
metadata file when the index has it, with the manifest's recorded creation time
as fallback. Show the same date in the **Drive added** column (native
**Masuk Drive**), with a labeled row on mobile. The column header switches between
newest and oldest. Put undated packages after dated results. Editing a title,
thumbnail, or upload status does not give a package a new arrival date. In the
Status cell for a queued video, show its assigned worker and YouTube channel
from the queue or the package-scoped device report. Display **Upload start** and
**Scheduled publish** separately when recorded. Use the assignment's timezone
and display it. Identify stale worker reports as last known.
Native Inbox renders 50 rows per page from the cached inventory. Browsing and
sorting that inventory require no additional Drive calls. Keep
search, filters, sort, and status totals scoped to the complete inventory. Store
selection by package identity across pages, show selections outside the page or
filters in the count, and apply bulk select to all matching eligible packages. Uploaded/conflicting/missing/unknown-source items must not silently become
ready. One source's failure does not erase the last successful Inbox snapshot.
Keep retrieval time and partial/failed status separate from successful empty data.

Combine valid source/package receipts with the same executor ledger. If history
access is incomplete, status is unknown, not confirmed Ready. Titles and display
names can help review but cannot establish duplicate identity. For matching source
IDs/versions already assigned to a non-cancelled job, return that job rather than
creating a second one. Do not invent a native receipt for arbitrary raw files.
Follow [upload workflow](../../ytfusion-operations/references/upload-workflow.md)
for supported package normalization and recognized history.

## Upload Queue

One queue belongs to a destination channel ID and publication mode. Reuse that
queue by default; separately named queues are an explicit option. Keep distinct
source labels. Initially keep jobs **Draft / Held · Not started** until execution
is assigned and implemented. A private default for a new draft is acceptable;
never infer Public from an empty field or native screenshot. Preserve explicit
choices and existing schedule/authorization data.

Persist enough data for the same worker to validate the reviewed job:

| Data | Required meaning |
| --- | --- |
| Identity/version | Stable queue/job IDs, source file/version and package/export identity, destination channel ID, schema revision and action/request ID |
| Reviewed settings | Title/description/tags, category, audience/AI choices, privacy/publication mode, declared thumbnail, explicit/default/none playlist |
| Timing | Timezone, earliest transfer vs YouTube publish time, fixed/random pattern and already sampled dates; null means unset, not immediately due |
| State | Draft/held/eligible/running/accepted/finishing/complete/error/review/cancelled, revision, last worker acknowledgement and error |
| Result | Accepted video ID, finishing evidence, receipt/history sync and selected cleanup outcomes; never credential/session secrets |

Treat this as a semantic contract, not a requirement to adopt invented field
names over an existing working ledger. Keep edits transactional/versioned and
reject stale revisions rather than clobbering a newly claimed or changed job.
Retried UI requests must be idempotent. A UI acknowledgement says **Saved** only
after durable storage succeeds; a worker acknowledgement records the exact same
job/version. Browser localStorage alone cannot own operational jobs.

For full controls, follow
[native queue semantics](../../ytfusion-operations/references/yt-upload.md#queue-and-schedule-contract)
and [executor recovery](../../ytfusion-operations/references/muse-executor.md#recurring-tasks-and-durable-upload-state).
Separate transfer start from scheduled YouTube publication. Random dates are
drawn once and persist across refresh/retry. Pause stops future claims while the
active video finishes; removing a draft/cancelling a waiting job does not delete
Drive/YouTube files. Unknown upload outcomes require reconciliation before Retry.
Do not expose unsupported destructive/running-job actions as working controls.

## Progress and History

Show genuine worker stages and heartbeat/update time. Render byte percentage,
speed or ETA only when measured. A missed heartbeat means stale status, not an
assumed failure or permission to create another upload. Opening/closing a Space
must not start/stop workers. Scheduler persistence and surviving an in-flight
VM restart are separate capabilities requiring evidence.

History includes accepted upload facts even when thumbnail, playlist, receipt or
cleanup is pending. Label that work **Needs action / Finishing pending**. A video
ID alone is not completion. Sync native-compatible Drive history before declaring
the package Uploaded across devices; show pending sync explicitly. Never rewrite
metadata to claim success. Hide completed cards only after the required workflow
is resolved, while retaining identity/receipt/recovery evidence. Staging cleanup
follows assigned ownership/policy; clearing a card does not delete any media.

## Verification and handoff

- Use real assigned metadata for the delivered Inbox; synthetic references remain
  fixtures and never seed live queues or History.
- Verify a selection and its held job survive reload, repeated Add returns the
  same identity, worker dry-run reads the same revision without claiming it, and
  a changed/unknown source is blocked or explicitly held for review.
- Verify empty/search/filter states, thumbnail/detail, selection scope and clear
  removal of only a disposable held draft. No transfer is needed for these checks.
- Inspect desktop/narrow viewers; keep a compact native-like list and useful
  controls. UI copy stays short; secondary explanation belongs in tooltips/detail.
- Record source/skill revisions, Space identity, authoritative store and actual
  bridge. Report what is implemented, what is held and what was not live-tested.
  Update the same Space on future changes and preserve jobs/grants/preferences.
