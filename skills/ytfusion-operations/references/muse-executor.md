# Muse as a scheduled upload executor

Use this mode when the user assigns Muse to fetch final videos and upload them
through available connectors/APIs, with YtFusion as the workflow reference.
This is distinct from operating the native YtFusion dashboard. Preserve an
existing native installation, credentials, and queues; do not reset or migrate
them merely to evaluate this mode.

## Choose the execution mode from actual capabilities

Read the instance assignment and inspect the host's available tools. Record
`execution_mode: native_app` or `execution_mode: agent_executor` in private agent
context once chosen. This field is not a YtFusion application setting.

- **Native app:** use the installed YtFusion queues/UI/API and the other workflow
  references. Its native queue owns job state and scheduling.
- **Agent executor:** use supported Drive access, a resumable YouTube uploader,
  a private durable job ledger, and Muse's scheduler when authorized. The ledger
  owns these separate jobs. Do not claim they appear in YtFusion's native queue.

For an agent-executor assignment, obtain the appropriate app source and study
only relevant package/metadata, channel mapping, scheduling and recovery logic.
Do not import `src/app.py` as a library, copy Private engines into the skill repo,
or require a continuously running dashboard just to read the implementation.
Reuse suitable dependencies already installed, normally the app's virtualenv.
Source access does not establish that an independent executor is implemented.

## Capability evidence and first proof

One Muse instance inspected on 20 November 2026 had a Drive connector, Python
upload libraries in the app venv, and a native recurring-task facility. A later
authorized Drive test wrote actual MP4 bytes directly to VM staging without Mac
control or rclone, but stopped with a partial file after a reported runtime
interruption; complete download, checksum, and upload were not verified. The
exact interruption cause was not established. A public Google API request timed
out after approval; the cloud browser reached Google's sign-in page but rejected
a VM loopback URL. These are bounded observations, not host-wide guarantees.

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
assigned upload. Only after the transfer legs work should the recurring workflow
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
requests them. Follow [Google project setup](google-project.md) when clients or
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
or media download works. Diagnose one concrete failed leg at a time.

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

When implementation is requested, the executor needs a durable ledger keyed by
Drive file ID plus version/fingerprint, destination channel, and intended job
identity. Track download status, local file identity, upload state, resulting
video ID, publication intent/timezone, and retry/review state. Keep account tokens
in supported credential storage. Treat resumable session URIs as sensitive:
persist them only in protected private state, never in chat, public ledgers or logs.

Use the resumable session protocol to query the server's accepted bytes after an
interruption and validate the same source before continuing. A library accepting
`resumable=True` does not prove restart recovery has been implemented. Session
expiration and ambiguous final outcomes need explicit handling. Reconcile saved
video IDs and session results before a new insert; unknown outcome is a review
state, not permission to insert another video. Persist success before optional
thumbnail/playlist work so repairs do not re-upload the video.

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
