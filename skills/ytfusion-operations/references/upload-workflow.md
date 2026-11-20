# Preserve the YT Upload workflow

Use this contract for native YT Upload and independent Muse execution. It defines
observable behavior, not a second native queue or a prebuilt standalone uploader.
For native jobs use [YT Upload](yt-upload.md). For an independent executor, read
the matching installed implementation before its first upload or a relevant
version change; retain the resolved policy so later jobs do not rediscover it.

## Read the actual chain

| Stage | Source to inspect |
| --- | --- |
| Package normalization and stable identity | `src/hds_drive_format.py`, `src/hds_drive_upload_bridge.py`, relevant package I/O |
| Import job/defaults | `yuAddStagedToQueue` in `src/static/js/yt_drive_jobs.js`; `yuJobFillFromProject`, `yuBulkAdd`, `yuLoadMeta`, `yuDefaultPlaylist` and cleanup controls in `src/templates/yt_upload.html`; queue overrides in `src/static/js/yt_channel_queue.js` |
| Transfer, status payload and finishing | `upload_video`, `list_playlists`, metadata repair in `src/hds_youtube_upload.py`; `src/youtube_thumbnail_policy.py` |
| Accepted result/history/Drive sync | journal callbacks, `_hds_record_upload_receipt` and `_hds_merge_drive_receipt` in `src/app.py` (read targeted definitions, never import the app); `make_receipt`, `save_receipt`, `sync_receipts` in the bridge |
| History identity/location and cleanup | `src/hds_upload_collection.py`, `src/hds_upload_state.py`, `src/hds_drive_system.py`, `src/hds_upload_cleanup.py`, `UploadQueue._finalize_video_cleanup` |

Preserve this order: user assignment and explicit per-job choices override the
applicable package/channel defaults; missing values get the installed workflow's
defaults, not arbitrary Python truthiness. An explicit `false`, empty playlist
selection or thumbnail removal is not “missing.” Do not apply HDS defaults to
unrelated Regular/Live content without checking its workflow and assignment.

## Resolve settings before transfer

| Setting | Current YT Upload behavior to preserve |
| --- | --- |
| Title, description, tags | Read the exact selected export/package; keep its approved text and identity, not a truncated connector filename |
| Category | Explicit selection/package value, otherwise **People & Blogs, `22`** |
| AI disclosure | HDS UI defaults to true; Drive import uses `containsSyntheticMedia !== false`, so an absent field defaults true and explicit false remains false. Send `status.containsSyntheticMedia` explicitly after resolving the job |
| Audience | Resolve package/user choice; current HDS/import default is not made for kids. Send **`status.selfDeclaredMadeForKids: false`** for that choice. `madeForKids` is YouTube's resulting status, not the writable declaration |
| Thumbnail | Use the selected project image or the package's validated `thumbnailFile` when available. Preserve explicit removal/custom selection. Upload it as a finishing operation, not as a `videos.insert` field |
| Playlist | Keep explicit ID/name/none. Otherwise current UI selects the first existing playlist returned for the destination channel. No playlists means none; do not invent/create one just to satisfy a default. Resolve actual full IDs and ownership |
| Privacy/publication | Follow the assignment. A private test stays private with no `publishAt`; never copy a source's public/scheduled setting over that instruction. Native scheduled mode needs a valid publication choice before Start; backend fallback is not a substitute for scheduling validation |
| Cleanup | Resolve final local/VM, final Drive, and footage policies separately. Preserve saved choices and obtain actual deletion authorization where required; see below |

Keep a private resolved job with the settings and their source (assignment,
explicit override, manifest or workflow default), destination channel ID, source
file/version/hash, and thumbnail identity. Do not silently substitute an image or
another channel when a declared resource is missing. Have the agent resolve and
save this; do not make the user complete a technical checklist for every video.

## Transfer and finish one video

1. Reconcile the ledger, native/Drive receipts and existing YouTube result before
   claiming the source. Bind package/file identity and version, channel and job.
   Verify downloaded length/hash and media readability before upload.
2. Use the authorized resumable transfer. Persist accepted bytes/session state
   privately if restart recovery is implemented. Never repeat `videos.insert`
   after an uncertain final response without reconciling the original attempt.
3. Save the returned video ID and accepted upload fact durably **before** thumbnail
   or playlist requests. “Video exists” and “workflow complete” are different.
4. Apply the requested thumbnail; resolve the assigned/default playlist and add
   membership once. Check existing membership before retries. Preserve an
   explicit none. Creating a named new playlist is a separate assigned action;
   do not accidentally inherit a helper's public-playlist creation behavior.
5. Read back channel ID, title/category, private/public/scheduled state and all
   requested status fields. Verify the explicit audience declaration separately
   from `madeForKids`. Check custom thumbnail identity and playlist membership.
   A 200 response alone does not establish all requested settings were retained.
6. Treat absent fields as **unknown**, not false or success. In the pilot, an AI
   update returned true while `videos.list` omitted it; Studio confirmed the
   saved **AI use: Yes** with no pending changes. If needed, inspect the actual
   Studio setting through authorized controls rather than declaring the API
   unsupported or blindly uploading/updating again. Record the evidence source.
7. Record and sync the recognized upload history, then perform selected cleanup.
   Keep explicit pending/failed outcomes for each unfinished leg. YouTube media
   processing, upload acceptance and publication are separate states.

## Mark “previously uploaded” on Drive

A private agent ledger alone will not mark a package uploaded in YtFusion's
Drive Inbox. Preserve the installed **receipt contract** and source identity.
Current bridge receipts use `ytfusion-upload-receipt/v1`, a deterministic
`receiptId`, `projectRef`, `draftName`, and an entry with actual video/channel,
time and applicable collection/project/export identity and result details.
Read the actual builder/validator; do not invent a boolean in the editable JSON.

Use native recording/sync for native jobs. For a standalone executor, reuse the
pure receipt builder/validation when available, or implement the inspected
contract faithfully with the same stable identity. Deliver the append-only
receipt through the connected Drive transport. Rclone is the native sync
transport, not a requirement for a supported Muse connector implementation.
Never import `src/app.py` to obtain its recording hook or fabricate a collection,
project reference, upload time or successful finishing result.

Resolve the workspace's real system-data parent. Older workspaces keep
`_Upload Results` at the root; newer ones may use
`_YtFusion System/_Upload Results`. Inspect `hds_drive_system` and the existing
workspace marker; do not create a competing history folder or another workspace.
Keep editable source metadata, original source video and immutable upload facts
distinct. Metadata fields such as `sourceUploadHistory` are projections, not an
excuse to overwrite the source or lose older receipts.

Read the receipt back, validate identity and facts, and verify the native
history/Inbox resolves the source as previously uploaded where native access is
available. If only receipt readback/validation is available, state that evidence
limit. Conflicting receipts require review; retain both evidence and media.
If writing/sync fails, preserve the video ID and report **uploaded; history
pending**. Retry the receipt operation, not the upload.

## Clean the assigned local copy after recording

Native UI has separate local/VPS and Drive cleanup settings, restored from saved
choices. Current UI can default these to delete; legacy backend jobs missing an
option can mean keep. Neither is permission to apply every destructive default
to a new executor or silently replace an existing keep policy.

For a Muse assignment that requests disposal after success, capture that policy
for **owned VM staging only**. Once the upload and selected finishing are verified,
the durable local receipt is saved and the required Drive history is confirmed,
remove the exact assigned staged MP4 and eligible job-owned temporary copies.
Check its recorded file identity and that no other pending/running job uses it.
Do not delete a replacement file, follow a symlink, or recursively remove a
shared staging directory. Missing files can be recorded as already absent.

Preserve token/client stores, assignment, scripts, receipts, hashes and recovery
evidence needed for history. Keep original Drive video, metadata and thumbnail
unless an independent **Drive-source** cleanup policy was explicitly authorized.
A request to clear the VM copy does not authorize Drive deletion. Honor any
host-required deletion confirmation at the actual action.

On failed/ambiguous upload, pending finishing/history, changed/shared file or
conflicting cleanup intent, retain media and record the blocker. Retry cleanup
independently; cleanup failure must never create another video or erase its
uploaded marker. Report bytes actually reclaimed, retained items and reasons.

Completion reporting should distinguish: accepted/processed video; resolved
settings; thumbnail; playlist; local receipt; Drive history; local cleanup; any
separately assigned Drive cleanup. Required history/cleanup cannot be omitted
from an “all done” claim merely because playback works.
