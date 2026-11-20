# YT Upload: final videos and Drive packages

This reference operates native YtFusion queues. For a user-assigned Muse executor
using connectors/APIs without the dashboard, read [Muse executor](muse-executor.md).
Do not force its connector to use the app's rclone connection or package format.

Both modes must preserve the [upload workflow contract](upload-workflow.md).
Read it before the first upload: AI/audience/category defaults, thumbnail and
playlist finishing, recognized Drive history and selected cleanup are part of
the workflow, not just title/description/tags plus an MP4 transfer.

Open `/fitur_tambahan/yt_upload`. Read the installed
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

For manual packages, current identity derives from workspace root and JSON path.
After uploading, renaming/moving that JSON can create a different package identity.
Use stable paths, distinct batches for duplicate names, and native review for
identity conflicts. Do not infer sameness from title alone.

The app manages the Drive workspace binding. When a device needs migration/join,
use **Google Drive → Migrasi / Hubungkan perangkat** and inspect its preview.
Do not move the workspace manually, delete its registration, or assume another
host's successful migration registered this one. Coordinate writers before an
authorized migration. `_Workspace.json` and `_Upload Results` are operational data.

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
