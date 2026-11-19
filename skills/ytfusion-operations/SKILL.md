---
name: ytfusion-operations
description: Prepare YtFusion and its Google project/accounts, operate final-video workflows through YT Upload, Regular Studio, or Live, or evaluate an assigned Muse connector/API executor with recurring tasks. Use for Muse onboarding, first account connections, Drive-to-YouTube uploads, assigned queues, scheduled publication, and API or encoder-only live streams. Reuse the instance assignment and installed application instead of repeating setup.
---

# YtFusion Operations

Respond in the user's language. Normally operate the installed YtFusion. This skill
covers installation and final-media operations on Muse, a VPS, or a local device.
Use `hds-home-production` for HDS generation. Reuse `ytfusion-domain-vps` in this
repository for domain/HTTPS deployment and managed Google-client installation.

## Start with the assignment

1. Find the existing installation and the agent's saved instance assignment.
   Establish whether the assigned mode is the native app or a Muse connector/API
   executor. For the latter, read [Muse executor](references/muse-executor.md)
   before installing a server or prescribing native account-import flows.
   Read its `AGENTS.md` and inspect the relevant native connection, channel, queue,
   and worker status. Do not start a second installation or worker to find status.
2. For a new host, missing connection, or installation/update request, read
   [setup](references/setup.md). The app repository is
   `https://github.com/kisanakclub/Yt_FusionX`; this skill repository does not
   contain the application or an automatic installer.
3. Read only the reference for the assigned workflow, then the matching installed
   documentation and implementation when details are needed:

   | Task | Reference | Native entry point |
   | --- | --- | --- |
   | Muse connector/API execution, capability proof, recurring upload tasks | [Muse executor](references/muse-executor.md) | Available host connectors, uploader, and scheduler |
   | Own GCP project, APIs, public branding pages, publishing, or clients | [Google project](references/google-project.md) | Google Cloud / site hosting / native client import |
   | First channel/Drive connection, additional account, or re-login | [Channels and Drive](references/accounts.md) | `/channel_manager`, `/add_channel`, `/gdrive-downloader` |
   | Upload final video packages from Drive or local output | [YT Upload](references/yt-upload.md) | `/fitur_tambahan/yt_upload` |
   | Operate a channel's Regular pipeline | [Regular Studio](references/regular-studio.md) | `/studio_dashboard` |
   | Live with YouTube API or encoder-only Live | [Live](references/live.md) | `/live_dashboard` or `/live_without_api` |

4. When the requested setup needs a Google project/client or public branding,
   execute [Google project](references/google-project.md); choose usable hosting,
   complete authorized publishing/verification steps, and install the clients.
   When the installation is empty or a required connection is missing, follow
   [Channels and Drive](references/accounts.md) before proceeding to the assigned
   workflow. Study the relevant installed UI and handlers; do not merely tell the
   user to add accounts. Prepare the connection and guide any necessary user login.
   Fill only missing information and save resolved choices privately so future
   tasks do not repeat onboarding. Connect only accounts needed by the task;
   encoder-only Live with a local source need not add a YouTube OAuth channel.

The assignment is agent context, not a configuration format that YtFusion loads.
In native mode, app settings, grants, queues, and receipts remain owned by the app.
An authorized independent executor has separate jobs and private durable state. Reconcile
the assignment against actual installed state before acting; a saved note cannot
establish that a channel is connected or a video was uploaded.

## Follow the user's scope

- An installation/setup request ends at the requested readiness. Upload, publish,
  or start Live when the current instruction or saved assignment authorizes that
  action. Record the scope of an ongoing assignment, including channels, sources,
  schedule, privacy, and cleanup. Do not ask again for routine steps already
  authorized; ask when a missing or conflicting choice materially changes work.
- Preserve existing app settings and credentials. For a new assignment, start
  with one upload at a time, no automatic source deletion, no inferred publication
  schedule, and reports for completion or a failure needing attention. The user
  can customize these defaults; they do not override an existing installation.
- Bind channel IDs and Drive file/folder identities, not just display names.
  Multiple hosts must have distinct assigned inputs or use an actual shared
  coordination mechanism. Separate local queues do not provide a distributed lock.
- In native mode, use UI or authenticated APIs whose current request/response contract has
  been inspected. Preserve session, origin, and CSRF checks. Never guess a payload,
  forge connection status, directly edit queue databases, or import `src/app.py`
  into a diagnostic script to discover behavior.
- Use the selected executor's supported Start, Pause, Resume, Stop, Retry, and
  review actions; native-app controls apply to native jobs. Re-read state
  after timeouts. Reconcile an uncertain YouTube result before retrying upload;
  do not create a second video or broadcast just because a response was lost.
- Keep Google downloads, refresh tokens, stream keys, app passwords, and GitHub
  credentials out of chat, this repo, screenshots, and command output. Reuse the
  supported account connection instead of creating a project for every task.

## Continue and report

On continuation, reconcile the saved assignment with the selected executor's jobs and receipts,
then perform the next authorized action. Keep stable job, package, file, channel,
video, or broadcast IDs in private progress notes only as needed. In native mode,
YtFusion owns durable scheduling. In agent-executor mode, use the authorized host
scheduler and durable ledger. An open chat is not a job supervisor.

For recurring monitoring requested by the user, use the host's supported task
mechanism and the same saved assignment. Do not promise a permanent shell process,
public endpoint, or restart recovery until verified on that host.

Report the useful outcome: which assigned work completed, its video/broadcast ID
or link, publication time and timezone where relevant, and any concrete blocker.
Distinguish downloaded, queued, uploaded, scheduled, published, encoder sending,
and confirmed live. Documentation checks or fixture tests do not establish actual
Muse installation, successful Google authorization, uploads, or live uptime.
