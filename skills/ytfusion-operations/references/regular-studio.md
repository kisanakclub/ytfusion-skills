# Regular Studio operations

Use `/studio_dashboard` and the channel's installed Studio settings. Read the
relevant parts of `src/worker_studio.py`, its native controls in `src/app.py`, and
the matching template if the selected mode is unclear. Do not infer behavior
from the dashboard name or copy an HDS upload API payload into Studio.

## Match the task to the channel pipeline

Read the saved assignment and current worker/queue status. Match the channel ID,
its Studio operation type, media folders, mode, title/description/tag rules,
thumbnail/playlist, privacy and publication schedule. A channel configured for
Live is not automatically the same Regular worker configuration.

For Drive-sourced final videos, use the installed Google Drive downloader or
asset-import workflow to place finished downloads in the intended native media
library. Inspect download completion and selected file identity before starting
Studio. Do not move partial downloads into input folders or assume the HDS Drive
Inbox and Regular media library share one import contract.

Current Studio supports modes including `video_only`, `audio_visual`, and
`narasi_backsound_visual`. **Video Only does not promise upload without processing**:
the current worker selects media and can prepare/render it with FFmpeg. Read the
actual selected pipeline, duration, ordering, rotation, and used-file rules.

If the user's request is to upload an unchanged finished MP4, first establish
whether that installed Studio configuration supports the intended result. When
it requires assembly or processing outside the assignment, explain the specific
choice and use an authorized supported final-video upload path instead. Do not
silently generate new media, change duration, or claim byte-for-byte passthrough.

## Run and follow the existing worker

1. Preserve the channel's saved pipeline. Fill only missing inputs that block the
   task; do not reset rotation, metadata, schedules, or cleanup on every run.
2. Apply only authorized configuration changes through native settings. Use the
   actual UI/API contract for this version, including session/origin protections.
3. Use native Start/Resume for the assigned channel. Check an existing worker
   before starting another. Let YtFusion own preparation, render, transfer slots,
   upload, metadata, and the next-item lifecycle.
4. Track native status and logs without displaying credentials. Separate media
   preparation/render failure from transfer, OAuth, quota, and YouTube processing
   failures so the next action targets the actual problem.
5. After an uncertain upload outcome, inspect native history and the destination
   account before retrying. Reuse an established video ID for metadata repairs
   where the installed workflow offers that action. Do not assume every Studio
   mode has the same recovery implementation as YT Upload.

Use native Stop/Pause controls when requested and preserve unfinished work and
used-media state. A paused native worker is different from a killed application.
Do not restart the whole host or clean its media folders to clear one job.

Report the selected workflow, resulting video ID/link and publication status or
time. Record the observed result in private progress notes. Successful YT Upload
on a host does not prove Regular's render dependencies or account setup work;
actual Studio execution remains a separate validation.
