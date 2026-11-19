# Set up an operations instance

## Find or install YtFusion

Inspect the host, existing checkout, app service, and saved assignment before
installing. Read the selected checkout's `AGENTS.md`. Preserve dirty work,
credentials, channel data, queues, and the configured Private/Shared edition.
Resolve paths on this host rather than copying another device's absolute paths.

For a new owner instance, obtain these two repositories in a persistent workspace:

```sh
git clone https://github.com/kisanakclub/ytfusion-skills.git
git clone https://github.com/kisanakclub/Yt_FusionX.git
```

These are clone commands, not installation commands. Reuse an existing checkout
instead of repeating them. The application is private: use the account assigned
repository access, normally Read for an operations host. Let the user complete
GitHub's normal browser/device login when needed; never request a token in chat
or embed one in the clone URL. Read `docs/setup/GITHUB_ACCESS.md` once available.
Use a Shared repository only when the user actually assigns that edition; do not
change editions to work around access or dependency failures.

Read this skill and make it available through the host agent's supported skill
mechanism, if provided. Reading `SKILL.md` explicitly can supply the procedure for
the current task; cloning alone does not prove future automatic skill discovery.
Do not invent a Muse skills-directory path based on Codex or another product.

Determine OS/version, Python availability, install permissions, persistent disk,
available space, process supervision, browser access, and network capabilities.
Inspect installer scripts before choosing a supported route:

| Host | Installed app guidance |
| --- | --- |
| Debian 13 | `vps-debian13/README.md`, `vps-debian13/SETUP_GUIDE.md`, `vps-debian13/setup.sh` |
| Ubuntu 22.04 | `vps/2_SETUP_GUIDE.md` and its referenced installer |
| Existing install | Its configured updater and maintenance guidance; do not rerun initial setup |
| Other environment | Read current platform instructions and dependencies; establish compatibility first |

The current Debian installer uses a non-root application user with sudo, Python
3.12 and a virtualenv, apt, systemd, and web-server setup. Root access inside a
container does not prove host-level privileges or systemd support. Minimal is the
documented upload/Live profile; check the assigned YT Upload page and dependencies
actually work before declaring readiness. Full is needed only for assigned features
that require it. Do not install every generation provider by default.

Muse's official [runtime description](https://muse.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)
describes a dedicated Linux environment and controlled network access. Establish
the actual account's disk persistence, service lifetime, usable dashboard URL and
proxy behavior, and required outbound connections. Google HTTPS uploads and Drive
downloads differ from sustained RTMPS Live egress. Do not infer arbitrary inbound
ports, a permanent public IP, or unattended 24/7 streaming from shell access.
If the supported installer cannot operate on this host, report the concrete
missing capability and the smallest next step; do not alter app authentication
or silently substitute a different hosting scheme.

## Connect the existing application

Open the actual running dashboard and use its normal login. Verify the assigned
workflow page and runtime tools: FFmpeg/FFprobe for media work, and the installed
Drive/rclone connection for Drive sources. Keep credentials and account consent
in their intended UI. Reuse existing app connections before requesting setup.

For Google setup, read the sibling [domain/VPS skill](../../ytfusion-domain-vps/SKILL.md)
and `docs/setup/DOMAIN_CLOUDFLARE.md` from the app. Current behavior matters:

- Linux is identified as a server by `installation_device()` in `src/app.py`.
  A browser inside Muse or a URL containing localhost does not automatically
  make its OAuth flow the Mac Desktop flow.
- A configured HTTPS dashboard uses its installed Web client for Add Channel
  and Drive, with separate user grants. Local management imports/installations
  and Desktop OAuth have different eligibility checks. Inspect
  `src/google_oauth_routes.py` when host/proxy behavior is uncertain. A Muse
  browser's availability does not establish a registered Google callback.
- Desktop JSON is appropriate for supported local Desktop flows, not a substitute
  for a server Web callback. Original JSON archives and active managed snapshots
  are distinct. Preserve `secrets/google_oauth/`, channel auth, and Drive's saved
  client/token pair; follow the domain skill for their lifecycle.
- Existing Google projects and connected accounts can be reused as assigned.
  Client installation is not account authorization; publishing status is not
  branding or scope verification. Do not promise Google acceptance or create
  extra projects to work around quotas.

Ask only for unresolved task inputs: repository/app access, the intended Google
project/client if missing, channel identity and account login, Drive source,
operation mode, privacy/schedule/timezone, or the stream key for encoder-only
Live. The GCP owner, channel account, and Drive account can be different. Do not
make the user repeat facts already available in the assignment or app.

## Keep a private instance assignment

Create the assignment through the agent once choices are known; the user need
not write JSON. Keep it outside both Git checkouts and any directory served by
the web app. Use the host's persistent private state location, for example:

```text
~/.local/state/ytfusion-operations/<instance-id>/
  assignment.json
  progress.json
```

Use an absolute `$XDG_STATE_HOME` instead of `~/.local/state` when configured.
Restrict directory/file permissions to the owner (0700/0600 where supported).
Choose a stable instance ID and record how to find the profile using the agent's
supported persistent memory/instructions. Reopen it on later tasks instead of
creating a new profile per chat. If no persistent discovery mechanism is available,
give the user a short continuation prompt containing its location.

Example shape for a newly prepared, not yet assigned instance:

```json
{
  "schema": 1,
  "instance_id": "uploader-one",
  "app_root": "<resolved installation directory>",
  "dashboard_url": "<verified dashboard URL>",
  "workflows": ["yt_upload"],
  "channels": [],
  "drive_sources": [],
  "timezone": null,
  "schedule": null,
  "upload_concurrency": 1,
  "cleanup": "preserve_sources",
  "reporting": ["completion", "failure_needing_attention"],
  "execution_authorized": false
}
```

Resolve IDs and timezone from confirmed app/user choices. When an ongoing task is
authorized, record its actual scope and boundaries, then reuse them. Keep credential
references here, never secret values. The app does not read this example format:
native configuration must still be changed through native controls, and an agent's
`execution_authorized` note is not an application security setting.

Update only the relevant assignment fields when the user changes the task. Reuse
connected accounts and native settings. Start with one upload at a time on a new
assignment unless directed otherwise; do not reduce existing parallelism silently.
Cleanup remains at the app's saved behavior on an existing workflow, within the
user's authorized scope. Do not enable Drive deletion merely to free disk.

## Readiness, updates, and continuation

Record what was actually checked: installed app and revision/edition, running
dashboard, workflow/tools available, connection and account status, accessible
assigned source, and any required user login. Missing account consent means
prepared for login, not ready to upload. An installation request alone does not
authorize a trial publication or stream. Test media only when within the task.

Before an update/restart, inspect active render, transfer, upload, Live, and
migration operations. Follow the installed updater and allowed Stop/Resume flow;
wait for affected work to be idle. A future queued publication does not require
waiting until its date, but preserve the queue and recovery state. Never reset
`user_data`, channel auth, journals, or settings to complete an ordinary update.
Verify the service and saved jobs afterward. Restarting a host does not prove
byte-level upload resume or automatic restoration of a live encoder.

On each continuation, read assignment → inspect native state → reconcile stable
IDs and pending outcomes → perform the next authorized action → report a useful
result. Schedule recurring checks only when requested and supported by the host;
keep the durable upload queue in YtFusion.
