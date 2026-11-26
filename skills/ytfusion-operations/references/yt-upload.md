# YT Upload: final videos and Drive packages

This reference operates native YtFusion queues. For a user-assigned Muse executor
using connectors/APIs without the dashboard, read [Muse executor](muse-executor.md).
Do not force its connector to use the app's rclone connection or package format.

Both modes must preserve the [upload workflow contract](upload-workflow.md).
Read it before the first upload: AI/audience/category defaults, thumbnail and
playlist finishing, recognized Drive history and selected cleanup are part of
the workflow, not just title/description/tags plus an MP4 transfer.

Open `/fitur_tambahan/yt_upload`. Read the installed
`docs/yt-upload-channel-queue-plan.md` for current queues/timing/controls,
`docs/HDS_UPLOAD_FORMAT_MIGRATION.md` for the current Drive package contract and
`docs/YT_UPLOAD_QUEUE_RECOVERY_AUDIT.md` for scheduling and recovery behavior.
Those documents describe a dated implementation; confirm relevant behavior in
`src/app.py`, `src/templates/yt_upload.html`, and the referenced queue/Drive helpers
when the installed version differs. Do not treat historical audit steps as new
work to repeat.

## Establish the input and destination

Read the instance assignment and inspect the existing channel queues, connection,
Drive Inbox, and upload history. Match the intended YouTube channel by channel ID
and the source by Drive identity. Drive Inbox routing and an account's channel
display name are not proof of destination authorization.

For a current manual Drive package, the app documents this form:

```text
YTFusion Upload/
  Channel/
    Batch/
      Batch name/
        Videos/Final video.mp4
        Metadata/Final video.json
        Metadata/Final video.jpg
```

```json
{
  "videoFile": "Final video.mp4",
  "title": "The full YouTube title",
  "description": "The approved description.",
  "tags": ["example"],
  "thumbnailFile": "Final video.jpg"
}
```

The thumbnail is optional; omit `thumbnailFile` if absent. `videoFile` must match
the video filename. Native HDS output can carry richer package identities. A
bare final MP4 in an arbitrary Drive folder is not automatically a YT Upload
package. Use the installed supported import/preparation path and the user's
metadata; do not invent project ownership or force HDS generation/Master setup
to upload a completed video.

Preserve an explicit Original/Extend choice and actual source-duration metadata;
read [media preparation](upload-workflow.md#original-extend-and-measured-duration)
before transferring a package that requires extension. The target duration and
an upload-time estimate are not the measured duration of the original file.

For manual packages, current identity derives from workspace root and JSON path.
After uploading, renaming/moving that JSON can create a different package identity.
Use stable paths, distinct batches for duplicate names, and native review for
identity conflicts. Do not infer sameness from title alone.

The app manages the Drive workspace binding. When a device needs migration/join,
use **Google Drive → Migrasi / Hubungkan perangkat** and inspect its preview.
Do not move the workspace manually, delete its registration, or assume another
host's successful migration registered this one. Coordinate writers before an
authorized migration. `_Workspace.json` and `_Upload Results` are operational data.

## Queue and schedule contract

Native queues belong to one channel and one publication mode. Reuse that queue
by default; create a separate named queue when assigned. New queue creation or
browser drafts do not start a transfer. Admission commits reviewed dates and jobs
together. Server queues persist; unsent drafts remain browser-local. Independent
Muse jobs use their private ledger, not invented native queue rows.

| Mode | Meaning |
| --- | --- |
| Publish on upload | Public after upload/processing; the pattern governs earliest upload start, not an exact publication deadline |
| Private / Unlisted | Earliest upload start and the explicit visibility; no inferred YouTube publishAt |
| Schedule on YouTube | A future publishAt; transfer starts when capacity is available, without a second user-defined upload schedule |

Days and clocks are separate choices. Current native server controls support
fixed day gaps or inclusive random whole-day ranges from 1 to 365; equal bounds
give a fixed gap. Random clock ranges apply to public/scheduled queues;
private/unlisted retain their fixed clock. Local YouTube/Drive scheduling uses
publication metadata and also supports random day ranges; legacy fractional
fixed intervals on that local panel remain valid. Inspect the chosen mode and
installed validation rather than imposing an OS-based scheduling restriction.

Draw each gap/clock once for a reviewed plan. Save the exact timestamps and
per-job interval_days as well as the chosen day_interval pattern for future
additions. Polling, retries, restart or reopen must not redraw accepted dates.
Append after the existing tail, preserve explicit per-video choices, and reject
stale previews instead of overwriting an updated queue.

The standard native host shares one download/upload/cleanup worker across queues;
Pause/Resume belongs to the chosen queue and Pause lets the current video finish.
Capacity reservations are advisory, not guaranteed completion times or a lock
across independent hosts. Read [Muse scheduling](muse-executor.md#recurring-tasks-and-durable-upload-state)
for implementing equivalent assignment behavior in a standalone executor.

After a delay, use the current recovery path and preserve the chosen mode.
Automatic native public patterns can move missed calendar-day slots together
while retaining clock times, order and sampled gaps; a delay within the intended
day alone does not skip that day. Private/unlisted interval queues preserve
spacing after a late start. Scheduled publication has its own journal/recovery
checks; do not convert a missed publication into immediate public upload.
Keep manual overrides and uncertain prior attempts under their existing guards.

## Queue through the native workflow

1. Select only assigned packages and resolve any native Review requirement.
   Confirm destination channel, title/description/tags, optional thumbnail and
   playlist, privacy, and schedule from the saved task. Preserve confirmed values.
2. Use the native transfer/import and channel queue controls. Let the app stage
   files and allocate transfer slots. Keep the package/file IDs and returned job
   ID for reconciliation; do not start a parallel downloader/uploader for the same
   item. Multiple hosts must have non-overlapping assigned inputs unless actual
   cross-host coordination has been established.
3. Inspect the current scheduling mode. **Publish on upload** describes the upload
   start pattern; **Schedule on YouTube** uploads before a separate publication
   time. Read the UI's timezone explicitly (the documented queue uses WIB) and
   translate user times if necessary. Do not assume the VM's OS timezone matches.
4. Start/continue only authorized work. Observe native queue Activity, transfer,
   and upload status. Editing queued schedules should use the app's preview/Save
   transaction; do not rewrite active/completed jobs or regenerate a random
   schedule on each poll. If state changed during editing, reload before retrying.

## Continue without duplicate uploads

Use the app's journal, receipts, YouTube video ID and Review Uploads before
retrying an interrupted/ambiguous result. A missing response is not proof the
upload failed. Once a video exists, repair thumbnail, playlist or metadata through
supported actions rather than inserting the same video again.

The documented uploader can retry the same resumable session while its process
lives. Do not promise persistence of that session/byte offset across process
restart: recovery uses journal and result review. Use the installed implementation
as authority if this behavior changes.

Pause normally holds following jobs; Stop requests cancellation of active work.
Wait for native stopping/recovery status rather than killing a process. A saved
`videoId` remains a real upload even if Stop skips remaining metadata steps.

**Cancel** removes a waiting job without recreating a browser draft.
**Cancel N** affects waiting jobs in that queue, leaving active work to finish;
use **Pause after current** to prevent later work from starting.
**Withdraw & edit** is the route for returning a non-running item to editing.
Check the current journal result first when an earlier upload is uncertain.
Cancellation does not delete Drive media or an existing YouTube upload.

**Clear Completed** dismisses only selected clean results from the visible list.
Use the current completion helper, not state=done alone: warnings, uncertain
remote state, pending/failed metadata sync or cleanup need follow-up. Preserve
the durable job/video/receipt and duplicate-prevention evidence. Clearing cards
is separate from physical file cleanup. Deleting an empty queue only removes its
definition; a queue with live jobs or completed history is not empty, including
when those completed cards are hidden.

Clean up only through the configured native lifecycle and the user's assignment,
after the app establishes the outcome. Preserve receipts and unresolved attempts.
Do not delete original Drive media or local recovery files because a task merely
disappeared from the active list.

Report the final native job/video ID and any pending metadata action. An uploaded
video also needs its durable receipt and assigned Drive history sync; a private
agent ledger alone does not create the native “previously uploaded” marker.
Report pending recording/cleanup separately and repair those steps without
another video insertion. An uploaded
video scheduled for tomorrow is upload-complete, not published today. Distinguish
YouTube processing/publication from transfer completion and an accepted schedule.
