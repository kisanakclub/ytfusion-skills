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

A read-only inspection of one Muse instance on 20 November 2026 found a Drive
connector with documented binary download, Python upload libraries in the app
venv, and a native recurring-task facility. Drive was not connected and actual
download/upload was not tested. A public Google API request timed out after
approval. The cloud browser reached Google's sign-in page but rejected a VM
loopback URL. These are bounded observations, not guarantees for other instances.

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
