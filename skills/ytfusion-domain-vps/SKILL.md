---
name: ytfusion-domain-vps
description: Configure or migrate YtFusion YouTube API Setup on local devices and VPSs, including Firebase or owned-domain branding, Desktop/Web OAuth clients, setup profiles, DNS/HTTPS and Server Transfer connections.
---

# YtFusion Domain and VPS

Use the installed YtFusion workflow and respond in the user's language. Open
**YouTube API Setup** (`/domain-setup`) on the user's management device. If the
installation files are available, read `docs/setup/DOMAIN_CLOUDFLARE.md` from that
installation and check which actions its wizard actually offers.

On a remote VPS, the default page shows the installed configuration for the
current dashboard hostname: managed public site, Web project, callback and saved
channel count. Setup profiles and drafts belong to the management installation.
An empty wizard catalog on a VPS does not establish that its client is missing.
Use the overview's installed state first. The explicit **Wizard domain & HTTPS**
action opens management; Google client import/install stays on localhost. The
HTTPS label describes the current connection, while domain and Google review
checks remain separate operations.

## Setup profiles

Profiles are installation-local setup notes. Automatic names follow the selected
server/domain; **Ubah nama** and **Hapus** are beneath the profile selector.
Legacy generic labels can be derived from the saved context, so identify a
profile by its target and profile ID rather than assuming duplicate labels mean
duplicate servers. Delete a profile only within the requested scope: its
confirmation removes the setup note, while saved projects, credentials and VPS
configuration remain. Empty drafts do not create saved profiles. Preserve a
meaningful unsaved draft when switching profiles or returning after a reload.

## Identify the target and check its state

- Reuse the user's saved **Server Transfer** connection for the intended VPS.
  Match the target IP and the SSH account to that connection. Server Transfer
  uses its configured identity and port. Test with those settings before
  diagnosing a Server Transfer authentication failure.
- In **HTTPS VPS**, use the VPS status check. It can report an already working
  public dashboard without contacting the SSH helper. When SSH or helper access
  is the question, check the saved connection and the helper's status directly
  through the installed workflow. With shell access, inspect the installed
  Server Transfer configuration and use the same saved identity, verified host
  key, and read-only helper status operation. Keep key contents and passwords out
  of output, chat, and published files.
- Report DNS resolution, public HTTPS, and remote setup access separately. A
  certificate check on the VPS is evidence about the origin, while public
  readiness requires reaching the hostname from the management device. A request
  to inspect or discuss ends after the checks and explanation.
- For application installation/update or GitHub access repair, use
  [Operations maintenance](../ytfusion-operations/references/maintenance.md).
  Reusing a saved SSH connection does not establish GitHub access from that VPS.

## Install or migrate when requested

1. Establish the runtime target, login location and public branding hosting
   independently. Current setup profiles support local or VPS runtime, Desktop
   login on the management computer or direct Web login on a VPS, and Firebase
   Hosting or an owned domain for branding. Follow the installed UI; older
   profiles retain their owned-domain/Web configuration. For an owned domain,
   use separate dashboard hostnames or one hostname with homepage `/`, dashboard
   `/dashboard`, and callback `/oauth2callback`. One shared hostname can target
   only one VPS. A dashboard-only migration can keep the existing public site.
   Before using the shared hostname layout, update/activate YtFusion on that VPS
   so `/dashboard` exists, and update its helper when requested.
   For Desktop login, continue with Google clients below; the DNS/HTTPS steps
   here apply when configuring a public VPS dashboard.
2. Use the wizard's DNS records and apply the relevant changes in the user's DNS
   provider, normally Cloudflare. Verify the new hostname points to the target
   before starting HTTPS setup. Preserve unrelated DNS records. If a web login,
   second factor, or sudo password is required, let the user enter it directly
   in the appropriate UI.
3. Use **HTTPS VPS** to install through the matching Server Transfer connection.
   Activate or update the helper only when the installed workflow requires it.
   Confirm affected VPS jobs are idle before operations that can restart YtFusion.
   If the saved connection or remote helper is unavailable, follow the installed
   manual ZIP flow with authorized admin access. After a timeout, inspect VPS
   status before retrying because the remote installer may still be running.
4. For a migration with an overlap period, use **Add** (`Tambahkan`) so both
   hostnames can serve while the new one is tested. The wizard's replace action
   can retire a managed dashboard as soon as the origin passes its check, before
   browser or Google login verification. Retire the old hostname only when it
   is within the requested scope and the required checks have passed. The wizard
   protects the public website from this dashboard replacement action.
5. When the dashboard uses direct Google OAuth, register the exact new callback
   shown by the installed app. Reuse the configured Web client for a migration,
   or use the wizard's GCP step for a first setup. Keep the old callback during
   overlap and verify sign-in on the new HTTPS hostname. Update Google Branding
   links if the public site used there is moving. Verify the new dashboard and
   any moved public pages from the browser before reporting success.


## Google OAuth clients and private archives

For a first Google project, API activation, public branding pages (including
existing hosting, Cloudflare Pages, or GitHub Pages), publishing and client
creation, follow [Google project setup](../ytfusion-operations/references/google-project.md).
Execute the authorized setup and record the actual publishing/review state;
reuse an assigned existing project rather than creating one per connection.

Use **Target → Branding → GCP → Akun** for Desktop login. Direct Web login adds
DNS and HTTPS before GCP. Select the target/project and import the matching
Google download. **Pasang untuk localhost** binds a Desktop client on the
management computer without SSH; connect YouTube and Drive there, then transfer
connections to the VPS if selected. The management computer need not stay on.
Direct Web login uses the existing SSH client installer. Follow the installed
UI when older versions have different controls.

The GCP stage groups **Branding & website**, **API & publikasi**, and the matching
**OAuth Desktop/Web client** in collapsible panels. Project identity stays above
them; file references and review notes are under **Catatan & verifikasi lanjutan**.
The project selector's **+ Project baru** adds a setup note; it does not create
a Google Cloud project. API/Production checkboxes record observed Console state,
not activation. Import the matching primary JSON, then use **Simpan JSON** and
the install action; the other client type is optional. Prepared clients and
completed account grants remain separate states.

For Firebase branding, the GCP step can download a public website ZIP containing
homepage/privacy/terms, Hosting configuration and deployment instructions.
Downloading is preparation, not publication. Review the pages, use the assigned
project's Spark plan without billing, deploy **Live**, and check all public URLs.
Do not deploy a preview channel as the permanent branding site. Static Hosting
does not run YtFusion or provide its Python OAuth callback. A Web login still
needs a separate HTTPS application endpoint. Record actual Audience and review
states rather than treating a live site as Google verification.

- A Web application client serves both Add Channel and Google Drive on the VPS.
  Register the exact HTTPS callback shown by the wizard. The YouTube and Drive
  grants are separate account logins even when they share the Web client.
- A Desktop client serves localhost logins for both YouTube and Drive on the
  management Mac. Preserve each client's actual Google type regardless of its
  downloaded filename. Creating or replacing credentials is a separate action
  from importing an existing download.
- Current localhost imports automatically archive original JSON bytes beneath
  `secrets/gcp_client_archive/<target-label>/<project-id>/`, named
  `oauth-web.json` and `oauth-desktop.json`. The label is the dashboard hostname,
  `localhost`, or the profile/server identity for a VPS using local login.
  Keep archives private and out
  of Git. They can be copied or moved for personal backup.
- Setup and installed dashboards use managed snapshots under
  `secrets/google_oauth/` with `index.json` and hash-named JSON files. Preserve
  this active store. Older installations may still reference original files
  through `global_config/domain_setup_profiles.json`; check the saved paths
  before moving an old archive. Import through the current wizard to create
  managed copies.
- Existing channels retain their client and login token in
  `channels/<channel>/data_internal/auth/`. Installing a default project selects
  the client for new logins. Reauthorizing or switching an existing channel is
  a separate operation. Keep Drive's existing connection backups and channel
  upload queues intact during ordinary setup.
- Original downloads may also be kept privately on a VPS when requested. VPS
  installation creates the active client snapshots; automatic original-file
  archiving described above belongs to the localhost import step. Check the
  actual files before reporting an original-download backup on a VPS.

Verify the project's Audience publishing status separately from branding and
scope verification. Record each actual result, and distinguish prepared clients
from completed channel/Drive account authorization. Archive changes alone need
no service restart. Source updates that require activation must wait for affected
media/upload work to be idle.

Report which hostname was checked or changed, what was verified at the origin
and from the browser, and any step still pending. Scope changes to the requested
hostnames and integrations.
