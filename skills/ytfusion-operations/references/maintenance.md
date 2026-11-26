# Update and maintain an existing installation

Use this reference for local-device/VPS updates and GitHub access repair. Reuse
the installed app, its edition and dependency profile. For a new installation,
start with [setup](setup.md); for DNS/HTTPS and Google clients use the sibling
[domain/VPS skill](../../ytfusion-domain-vps/SKILL.md).

## Find the target

Read the installation's `AGENTS.md`, `docs/RELEASE_ACCESS_RUNBOOK.md`, platform
updater and relevant maintenance guide. A development checkout can also be the
running Private installation. Preserve dirty work; do not reset it to update.

For a remote host, use the management installation's saved Server Transfer /
Remote Nodes connection, including application path, user, port and identity.
With shell access these are in `global_config/remote_nodes.json`; resolve the
configured key through that installation's private `secrets` store. Verify the
SSH host key and preserve the target selection. Do not embed the owner's host
list, IPs, keys or account names in a reusable skill.

## Prove independent update access

Access from the management computer to the VPS does not grant that VPS access
to a private GitHub repository. A transferred clone or Git bundle proves code
delivery, not future independent maintenance.

1. Use the application user, not root or another user's GitHub session. Check
   the installed edition, branch and repository before configuring access.
   Source Private uses `kisanakclub/Yt_FusionX`; Shared uses its assigned snapshot
   repository. Keep both the saved origin and updater channel consistent.
2. Read `docs/setup/GITHUB_ACCESS.md` from the application. Retain working access.
   An assigned GitHub CLI login is suitable for an interactive/development host.
   A production VPS needing one repository can use a unique read-only deploy key:
   its private half stays on the VPS and only its public half is registered with
   that repository by an authorized administrator. Preserve other identities.
   Owner GitHub tokens and the management SSH private key stay on their device.
3. Persist the selected access under the application user. For a deploy key,
   follow the app guide's repository-local SSH command and exact URL rewrites;
   the updater fetches a canonical HTTPS URL even when the origin uses SSH.
   A host alias or a rewrite for only a differently cased URL can leave the
   updater unable to fetch. Keep repository/edition validation enabled. Verify
   GitHub's host key against its official published fingerprint.
4. Open a fresh SSH connection with agent forwarding disabled (`ssh -a`, or the
   equivalent supported connection option). Do not inject management tokens,
   `GIT_CONFIG_*`, a temporary bundle rewrite, or an agent socket for this test.
   On that host, run `git ls-remote --exit-code origin refs/heads/main` and repeat
   for the canonical repository URL used by its updater. Require exit zero and
   a real branch SHA. A successful `gh auth status` alone is insufficient.
5. With affected jobs idle, run the actual platform updater below from that fresh
   login. Compare the installed commit with the fetched branch. If already
   current, record a successful no-op; do not claim a new deployment. If login or
   repository approval needs the user, finish other preparation and identify the
   exact remaining step. Do not call self-service updates ready before this proof.

An application login, a Google OAuth grant and GitHub access are separate. Repair
only the connection that failed. Keep one-time login codes and secrets in their
intended private UI; do not print token stores, private keys or process environments.

## Run the installed updater

Inspect active HDS/Studio/render, upload, transfer, Live and migration work before
changing a running installation. Auto-reload can activate Python edits before an
explicit restart. Wait for idle or use the user's authorized Stop/Resume flow.
Preserve future queued jobs and journals; their scheduled date is not a reason
to wait until the queue is empty. Avoid starting an update across an imminent job.

Run as the application owner from the actual installation root:

| Host | Normal command | Saved dependency profile |
| --- | --- | --- |
| Mac | `bash mac/update.sh` | Full or VM (`venv/.ytfusion_profile`) |
| Ubuntu VPS | `bash vps/update.sh` | Full or Minimal (`venv/.ytfusion_requirements`) |
| Debian 13 VPS | `bash vps-debian13/update.sh` | Full or Minimal (same marker) |
| Windows | Follow the installed Windows guidance; the checked helper is `venv\Scripts\python.exe scripts\release_update.py` | Do not assume a legacy wrapper uses the checked helper |

If a legacy installation lacks a profile, choose the assigned profile explicitly:
Mac `--full` / `--vm`, Linux `--full` / `--minimal`. These are dependency profiles,
not Private/Shared editions. Do not rerun initial setup on an existing service.
Use the installed runbook's explicit migration route for an old repository or
snapshot; do not change origin or edition merely to work around authentication.

The checked updater protects local data/configuration, validates its source or
release manifest, and fast-forwards ordinary updates. Respect its dirty source,
local-ahead, collision and channel errors. Inspect the actual failure rather than
substituting `git reset --hard`, deleting files, or bypassing validation. Recovery
backups outside the checkout are intentional and are not full media/venv backups.

If code advanced but dependency installation failed, resolve that step before
activation. On Linux, install the recorded requirements explicitly when needed;
a retry at the same commit may no longer see the original requirements delta.

## Activate and verify

Restart for backend/dependency changes after affected work is idle. Documentation
alone needs no application restart. Reload the page for changed browser assets.
For extension changes follow the app's build/update coordinator; a built package
does not establish that the browser has activated it.

For the standard VPS service, use the account's permitted restart operation:
`sudo systemctl restart ytfusionx`, or the installed domain helper's `restart`
operation where authorized. That helper accepts only JSON
`{"confirmed_idle":true}` on stdin after idle has actually been checked. Inspect
its installed contract before use. Failure of generic `sudo -n true` does not
establish that a narrowly allowed helper operation is unavailable.

After a restart timeout, inspect service state, PID and readiness before retrying;
systemd may still be finishing the original request. Do not submit duplicate
restarts. Verify the installed commit, service state, a new process when restart
was needed, and the expected app/assets over local and public HTTPS paths.
Check saved queues and credential-file metadata without printing credential
contents or modifying queue databases. An unauthenticated Login response proves
HTTP readiness only; actual uploads and authenticated workflows need their own
evidence. Never forge a session to manufacture a readiness check.

For source publication, verify the automatic Publish Shared result and remote
manifest source commit as required by the installed runbook. Report source push,
Shared publication, installed revision and runtime activation separately.

## Access failures and temporary bundle delivery

Separate GitHub authentication, network/host-key failure, repository policy and
local changes. For CLI access inspect normal auth status; for a deploy key verify
its registration, read permission, fingerprint and repository-specific transport.
Do not replace working access on another host because one server failed.

When direct GitHub access is unavailable and delivery is authorized, a verified
Git bundle sent over the saved SSH connection can be a bounded fallback. Bind it
to the reviewed commit, verify transfer checksum and Git bundle prerequisites on
the target, and retain the checked updater's repository/edition/data checks. A
temporary exact URL rewrite can let that updater fetch the verified local bundle;
scope it to that invocation, not persistent Git configuration. Restore normal
transport afterward. Record this as SSH-assisted delivery; it does not satisfy
independent-update readiness. Resume direct access setup rather than making the
management device an undocumented permanent requirement.
