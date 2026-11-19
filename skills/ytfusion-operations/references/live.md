# Live operations

First choose the workflow the user assigned. Read current native status before
starting a stream; do not create a new broadcast or encoder on each status check.

| Workflow | Entry point | Account requirement |
| --- | --- | --- |
| Live with API | `/live_dashboard` | Connected channel with required YouTube authorization and Live access |
| Live without API | `/live_without_api` | Broadcast configured in YouTube Studio and its private stream key |

Inspect the corresponding controls in `src/app.py` and their worker. For encoder-only
Live, read `src/direct_live.py` and `src/direct_media.py` when media or runtime
behavior needs checking. Do not apply encoder-only assumptions to API Live.

## Prepare the assigned source

Confirm channel/broadcast identity, final video or selected media pipeline,
start/end or duration, loop behavior, and the requested action. Reuse saved
assignment choices. Let the user enter a stream key through the app's intended
secret field; keep it out of shell arguments typed by the agent, logs and reports.

Use the native media library/import workflow for Drive downloads. A file listed
as downloading, checking, interrupted, or paused is not a ready input. Use the
native retry action; it can download again rather than resume at the same byte.
Never mark an unfinished download complete by editing its state file.

Current encoder-only Live validates H.264 video and AAC audio with FFprobe and
sends through FFmpeg stream copy to YouTube RTMPS on port 443. Use native validation
before starting; an MP4 extension alone does not establish compatible codecs.
Do not transcode a user's finished source or change quality unless that work is
authorized. API Live can have a different media-processing pipeline.

## Live with API

Inspect the connected channel, native schedule, existing broadcast/stream IDs,
and worker state. Confirm that YouTube permits Live for the account. Native
creation/binding/transition controls should own the broadcast lifecycle. If a
request times out, reconcile returned IDs and YouTube/native state before
creating another resource. A connected upload channel does not establish Live
eligibility or an active broadcast.

Start only the assigned pipeline. Observe source preparation, encoder progress,
ingest health, and broadcast transition where the installed interface exposes
them. Distinguish a future broadcast, an encoder connection, and a live broadcast.

## Live without API

Use an existing authorized broadcast/key from YouTube Studio; this workflow does
not create or manage broadcasts through the YouTube Data API. Save/select the
intended native stream and use its Start/Stop controls. The current manager guards
against concurrent use of a key inside this installation; that is not a lock
across independent Muse instances or VPSs. Allocate distinct active keys or
coordinate explicitly.

A running FFmpeg PID is not proof YouTube is broadcasting. Check native sending
progress/reconnect/error status and, when available, the user's YouTube Studio
ingest/live state. Report only the state observed. After restart, inspect native
interrupted state; do not promise automatic restoration or start a second sender.

## Stop and report

Stopping the encoder and ending the YouTube broadcast are distinct actions.
Follow the requested scope and available native controls, preserving the source
and any scheduled future work. Do not delete a broadcast or rotate a key merely
to stop sending.

Report the stream/broadcast ID, observed encoder and broadcast state, and the next
specific action if attention is needed. Sustained throughput, network permission,
and process lifetime must be tested on the actual host before promising unattended
Live; shell access and a successful video upload do not establish them.
