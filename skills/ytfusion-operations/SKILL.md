---
name: ytfusion-operations
description: Install or prepare YtFusion on a new agent host and operate existing final-video workflows through YT Upload, Regular Studio, or Live. Use for Muse onboarding, Drive-to-YouTube uploads, assigned channel queues, scheduled publication, and API or encoder-only live streams. Reuse the instance assignment and installed application instead of repeating setup.
---

# YtFusion Operations

Operate the installed YtFusion and respond in the user's language. This skill
covers installation and final-media operations on Muse, a VPS, or a local device.
HDS generation belongs to `hds-home-production`; domains and managed Google
clients belong to `ytfusion-domain-vps` in this repository.

## Start with the assignment

1. Find the existing installation and the agent's saved instance assignment.
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
   | Upload final video packages from Drive or local output | [YT Upload](references/yt-upload.md) | `/fitur_tambahan/yt_upload` |
   | Operate a channel's Regular pipeline | [Regular Studio](references/regular-studio.md) | `/studio_dashboard` |
   | Live with YouTube API or encoder-only Live | [Live](references/live.md) | `/live_dashboard` or `/live_without_api` |

4. Fill only missing information that prevents the requested work. Let the user
   complete login, consent, and secret entry through the intended secure UI.
   Save resolved choices privately so future tasks do not repeat onboarding.

The assignment is agent context, not a configuration format that YtFusion loads.
App settings, account grants, queues, and receipts remain owned by the app. Reconcile
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
- Use native UI or authenticated APIs whose current request/response contract has
  been inspected. Preserve session, origin, and CSRF checks. Never guess a payload,
  forge connection status, directly edit queue databases, or import `src/app.py`
  into a diagnostic script to discover behavior.
- Use native Start, Pause, Resume, Stop, Retry, and review actions. Re-read state
  after timeouts. Reconcile an uncertain YouTube result before retrying upload;
  do not create a second video or broadcast just because a response was lost.
- Keep Google downloads, refresh tokens, stream keys, app passwords, and GitHub
  credentials out of chat, this repo, screenshots, and command output. Reuse the
  supported account connection instead of creating a project for every task.

## Continue and report

On continuation, reconcile the saved assignment with native jobs and receipts,
then perform the next authorized action. Keep stable job, package, file, channel,
video, or broadcast IDs in private progress notes only as needed. YtFusion owns
durable job scheduling; an agent note or open chat is not a job supervisor.

For recurring monitoring requested by the user, use the host's supported task
mechanism and the same saved assignment. Do not promise a permanent shell process,
public endpoint, or restart recovery until verified on that host.

Report the useful outcome: which assigned work completed, its video/broadcast ID
or link, publication time and timezone where relevant, and any concrete blocker.
Distinguish downloaded, queued, uploaded, scheduled, published, encoder sending,
and confirmed live. Documentation checks or fixture tests do not establish actual
Muse installation, successful Google authorization, uploads, or live uptime.
