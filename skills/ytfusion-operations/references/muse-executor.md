# Muse as a scheduled upload executor

Use this mode when the user assigns Muse to fetch final videos and upload them
through available connectors/APIs, with YtFusion as the workflow reference.
This is distinct from operating the native YtFusion dashboard. Preserve an
existing native installation, credentials, and queues; do not reset or migrate
them merely to evaluate this mode.

For first setup, use [Muse onboarding](muse-onboarding.md). Select methods from
actual capabilities and the user's goal, not a fixed host/provider recipe.

## Choose the execution mode from actual capabilities

Read the instance assignment and inspect the host's available tools. Record
`execution_mode: native_app` or `execution_mode: agent_executor` in private agent
context once chosen. This field is not a YtFusion application setting.

- **Native app:** use the installed YtFusion queues/UI/API and the other workflow
  references. Its native queue owns job state and scheduling.
- **Agent executor:** use supported Drive access, a resumable YouTube uploader,
  a private durable job ledger, and Muse's scheduler when authorized. The ledger
  owns these separate jobs. Do not claim they appear in YtFusion's native queue.

For an agent-executor assignment, obtain the appropriate app source and follow
the [upload workflow contract](upload-workflow.md): package import, job/UI
defaults, payload, finishing, Drive history, cleanup and recovery. Reading only
metadata text or a low-level upload helper is insufficient.
Do not import `src/app.py` as a library, copy Private engines into the skill repo,
or require a continuously running dashboard just to read the implementation.
Reuse suitable dependencies already installed, normally the app's virtualenv.
Source access does not establish that an independent executor is implemented.

When the user requests a visual Drive Inbox/queue, use
[Upload Workspace](../../ytfusion-upload-workspace/SKILL.md). Establish the host's
actual Space-to-worker bridge, persist stable held jobs and verify a read-only
worker round trip before exposing execution controls. An existing one-off pilot
script does not become a queue executor merely because a Space was added.

Keep an explicit `agent_executor` decision across continuations. A connector or
receipt failure is a leg to repair, not a reason to start the native backend,
configure its Drive connection, or repeat GCP onboarding. Preserve any existing
native installation; stop a separate trial only when requested and after checking
its actual active jobs. Do not carry a trial's restrictions or pending approvals
over as authorization for new executor work.

Validate the assigned package/export using the installed pure format/identity
helpers where applicable and retain its real source identities. An independent
executor does not require a native HDS project catalog. Do not strip export
markers, invent project folders or forge native import state to make a final
video uploadable. Use those original identities in the shared receipt.

## Capability evidence and first proof

The 20 November 2026 pilot demonstrated direct binary Drive download to VM staging
through the built-in connector, full size/hash/media validation, and an authorized
private resumable upload from that VM. Initial download interruption was traced
to a VM reboot; a bounded full retry completed. Native local Desktop authorization
and private transfer of the matching channel token/client pair enabled successful
VM channel reads. After API activation, non-monetary Analytics reads succeeded.

The first upload omitted finishing. The same video was repaired without re-upload:
explicit not-for-kids declaration, package thumbnail and existing playlist were
verified; Studio confirmed AI disclosure even though the read API omitted it.
Data transfer success alone therefore did not establish workflow parity. Shared
Drive upload-history synchronization and post-success staging deletion were not
proven in that pilot. Recurring publication, restart-resume of an in-flight upload,
Regular Studio/render, sustained Live and revenue reporting remain separate tests.
These are observations from one instance, not host-wide guarantees.

Inspect the current account before prescribing setup:

| Capability | Establish before relying on it |
| --- | --- |
| Drive connector | Actually present, connected to the intended account, and able to download binary contents to the worker, not merely search metadata |
| YouTube executor | Available library/tool, intended channel authorization, required scopes, and usable upload transport |
| Browser | Which machine it controls and which URLs it can reach; cloud, local computer control, and an optional Chrome extension are different facilities |
| Scheduler | Supported creation/list/status controls, timezone, persistence contract, invocation lifetime, and observed run behavior |
| Persistent state | Private writable location retained across tasks/restarts, separate from both repositories and public web content |

Start with the smallest requested proof: connect Drive through its supported
account flow, download one assigned video, and verify length and checksum when
Drive provides one. Otherwise verify file identity/version, length, and a stable
local checksum without claiming an unavailable remote-hash comparison. Do not
create YouTube credentials or publish a video merely to test Drive access.

Next, when authorized, prepare the intended YouTube OAuth grant and test one
assigned upload including the [finishing/history/cleanup contract](upload-workflow.md).
Only after the required workflow stages work should the recurring workflow
be enabled. Preserve the user's explicit publication/privacy choice. A successful
private upload does not prove scheduled/public publication or sustained Live.

## Automatic download recovery

Completing an authorized download includes ordinary recovery from transient
failures. Do not stop merely to ask whether to retry the same file. Keep the same
account, source/version, destination, and purpose; host approval cards and a
user's explicit pause or retry limit still apply.

- Before retrying, inspect the actual process and staging file so a surviving
  transfer is not duplicated. Preserve the Drive file ID, version/fingerprint,
  expected length/hash, local path, attempt count, and latest error privately.
  Persist the attempt count across tasks/restarts rather than resetting it on
  every invocation.
  Track the actual downloader PID/task and exit result: a broad `pgrep -f` can
  match the checking shell or monitor itself. Full file size alone does not
  prove the writer exited or checksum/media verification passed.
- Prefer the transport's documented resume mechanism. Drive supports partial
  blob downloads with `Range`, but the selected connector must actually expose
  that operation. Validate the same source/version, returned range and length
  before appending; never append a full response to a partial file. A connector
  without a resume flag is not evidence that all Drive transports lack resume.
- If resume is unavailable, a full retry of the same authorized download is
  allowed. Check free space, write to a distinct partial path, and preserve the
  existing partial file until the replacement is verified or authorized cleanup
  applies. Do not relabel a partial file as complete or pass it to upload.
- Follow the saved retry policy. If none exists, allow up to two additional
  automatic attempts for a transient failure, with increasing delay and any
  server-specified wait. Record the next eligible attempt time. Use a supported
  continuation or an already authorized recurring task when necessary; saving
  a retry note does not itself schedule another run.
- Stop at the retry limit, or earlier for revoked/insufficient access, a changed
  source, a denied approval, or evidence the same execution limit will recur.
  Diagnose the concrete limit instead of endlessly restarting a large transfer.
  Report only the user action actually needed. A new transport, credential,
  schedule, or broader permission still needs its own applicable authorization.
- After completion, compare length and the available Drive checksum, then check
  media readability. Report success only after validation. Distinguish process
  exit, tool-runtime restart, VM reboot, and timeout from actual evidence; an
  empty log alone establishes none of their causes.

These instructions guide the agent's retries; they do not install a supervisor
or make a killed process resume by itself. For uploads, use the reconciliation
and resumable-session rules below rather than blindly repeating `videos.insert`.

## Google access without rclone or a dashboard

Use the built-in Drive connector when it supports the required operation. Inspect
its current documentation and connected state rather than inventing command names.
If it cannot fetch the required media, evaluate an authorized direct Drive API
transport. Rclone is optional in this execution mode. A Google client JSON alone
is not an account grant, and a native YtFusion Drive backup is not automatically
an accepted credential format for a Muse connector.

For YouTube, use an available supported upload tool or an authorized standalone
uploader using the official API/library. Choose scopes for the actual features.
`videos.insert` accepts alternative grants including `youtube.upload` and
`youtube.force-ssl`; do not require both if an existing grant already suffices.
Do not inherit unrelated partner/analytics scopes solely because the full app
requests them. If the chosen native login actually asks for broader scopes, show
that concrete request and obtain the required consent; do not describe it as an
upload-only grant. Follow [Google project setup](google-project.md) when clients or
branding are needed, adapting it to the selected login route rather than imposing
a server Web callback on an executor without a reachable dashboard.

The host's approval system still applies. Inspect the exact destination, action,
and scope and obtain the required real approval. Chat assent does not replace a
pending permission card. Prefer the required bounded grant rather than asking
for unrestricted network access. Use documented connector/proxy mechanisms.
Do not weaken isolation or add a tunnel to evade a denied request.

Record timeout, DNS/TLS failure, HTTP response, and explicit policy rejection
separately. HTTP 000 or a timeout does not establish a permanent policy block.
Public discovery access does not prove authenticated upload, large-file transfer,
or media download works. Diagnose one concrete failed leg at a time. The pilot
reached authenticated Data API calls via `youtube.googleapis.com` with the host's
trusted system CA bundle while another Google hostname timed out. Inspect the
actual proxy/transport and officially supported endpoint; do not disable TLS
verification, strip approvals or hardcode that observation for every host.
Runtime public egress may differ from the VM interface address. A dedicated VM
does not establish a stable/exclusive public IP, and IP-check probes do not prove
the source IP seen by YouTube or sharing across accounts.

## Recurring tasks and durable upload state

Create a schedule when the user requests recurring work and the required source,
channel, timezone, cadence and authorization are resolved. Inspect existing tasks
first to avoid duplicates, use the supported scheduler, and record its returned
task ID privately. A saved schedule and an observed successful invocation are
different evidence. Do not use an agent note as a substitute for an actual task.

Each invocation should read the assignment, reconcile existing jobs, claim only
assigned due work, execute a bounded amount, and persist results. Keep scheduling
choices stable across runs. Distinguish worker start time from YouTube publication
time. Observe the host's actual run budget; do not hardcode a budget seen in one
account as a product guarantee. Prevent overlapping claims with a supported lock
or transactional mechanism; a local lock does not coordinate separate hosts.

Follow the [queue and schedule contract](yt-upload.md#queue-and-schedule-contract)
when matching YT Upload behavior. Group jobs by assigned channel and publication
mode, keep pause state per queue/group, and share the assigned transfer capacity
(one at a time by default) across this instance. Native queue buttons/SQLite are
not prerequisites for an executor; preserve these decisions in its own ledger.

Resolve fixed/random day gaps and clock choices from the assignment. Persist
the reviewed per-job timestamps and sampled gaps plus the pattern for later
additions; do not redraw them on polling, retry, a new chat or VM restart.
For public/private/unlisted work, distinguish earliest transfer time from actual
publication; for scheduled YouTube work, persist publishAt and upload ahead when
capacity permits. Estimates are not a publication deadline guarantee.

Record the missed-run policy before recurring work. When following the native
pattern, preserve clocks/gaps/order after a missed public calendar day and retain
spacing for delayed interval jobs; do not drain all overdue jobs in one invocation.
A same-day transfer delay alone is not a reason to skip the day. Resolve
uncertain upload attempts before moving a group. A passed YouTube publishAt
requires the assigned recovery/review decision, not changing visibility to public
or silently discarding the publication intent. Save any reviewed replacement
dates atomically and retain manual overrides.

When implementation is requested, the executor needs a durable ledger keyed by
Drive file ID plus version/fingerprint, destination channel, and intended job
identity. Track download status, local file identity, upload state, resulting
video ID, publication intent/timezone, finishing results, native-compatible Drive
receipt/sync state, selected local/Drive cleanup and retry/review state. Keep account tokens
in supported credential storage. Treat resumable session URIs as sensitive:
persist them only in protected private state, never in chat, public ledgers or logs.

Handle cancellation against durable job identity/state: cancel waiting jobs
without deleting Drive/YouTube media; pausing stops later claims while the active
job finishes. Stopping an in-flight operation needs its supported cancellation
and outcome reconciliation, not merely removing a scheduler entry. A saved
video ID remains accepted work and finishing/history can still be pending.

If the executor offers a completed list, dismiss only fully resolved results and
retain its receipts, file/version-to-video mapping and recovery evidence.
Pending warnings, history/metadata sync, unknown upload outcomes and assigned
cleanup remain visible for follow-up. Removing a card does not mean deleting
staging, cancelling a live job or making a video eligible for another upload.

Use the resumable session protocol to query the server's accepted bytes after an
interruption and validate the same source before continuing. A library accepting
`resumable=True` does not prove restart recovery has been implemented. Session
expiration and ambiguous final outcomes need explicit handling. Reconcile saved
video IDs and session results before a new insert; unknown outcome is a review
state, not permission to insert another video. Persist acceptance before
thumbnail/playlist work so repairs do not re-upload the video. Follow the
[workflow contract](upload-workflow.md) for recognized Drive history and cleanup;
do not stop at a private agent ledger or retain disposable staging indefinitely
when its post-success cleanup was assigned.

Inspect the current connector's create-file, readback, upload-path and approval
contract before relying on shared history. Some require an absolute worker-home
path rather than `/tmp`. Use the workflow contract's one-file-per-receipt delivery
and per-leg continuation; no append API is required. Do not request a new OAuth
grant or native rclone setup merely because an already connected writer needs
its normal per-action approval.

A persistent schedule does not make an in-flight process survive VM/container
restart. A subsequent invocation must recover from durable state. Keep completed
receipts when cleaning staging files, and preserve sources according to the task.
Notify for requested milestones or failures needing attention, not every poll.

This reference specifies the candidate workflow; it ships no standalone uploader,
connector integration, checkpoint implementation, or pre-created recurring job.
Report prepared, implemented, connected, and actually tested states separately.

Primary references: [Muse runtime and approvals](https://muse.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse),
[Drive file download](https://developers.google.com/workspace/drive/api/guides/manage-downloads),
[YouTube upload scopes](https://developers.google.com/youtube/v3/docs/videos/insert),
[YouTube resumable protocol](https://developers.google.com/youtube/v3/guides/using_resumable_upload_protocol).
