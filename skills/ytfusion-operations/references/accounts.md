# Connect YouTube channels and Google Drive

Use this reference when an installation starts empty, an assigned channel or
Drive connection is missing, or the user requests another channel or re-login.
Connect only what the assigned workflow needs. Installed OAuth clients and
authorized channel/Drive accounts are separate things.
For Muse onboarding, use [Muse onboarding](muse-onboarding.md) to choose from
actual host capabilities. The native routes below are a proven option, not a
requirement to run the dashboard on every Muse VM.

## Learn the installed connection flow

Before the first connection on this version, inspect the actual pages and read
the matching portions of these files when available:

| Connection | Installed implementation to inspect |
| --- | --- |
| Channel Manager / Add Channel | `src/templates/channel_manager.html`, `src/templates/add_channel.html`; `/add_channel`, `_google_client_for_login`, and `oauth2_callback_route` in `src/app.py` |
| Drive login/import/status | `src/templates/gdrive_downloader.html`, `src/static/js/gdrive_connection.js`, `src/google_oauth_routes.py`, and relevant `src/gdrive_downloader.py` methods |

Follow the form fields, selected method, project selector, status checks, and
callback handling actually offered by this installation. Read only the relevant
handlers, not the entire application. Use native UI or inspected authenticated
APIs; do not invent a shell OAuth utility or manually construct credential files.

Inspect existing channels and Drive status first. Ask together for unresolved
account/channel choices and Drive source, then prepare every step that does not
depend on user login. The GCP owner, YouTube account, and Drive account need not
be the same Gmail. Do not ask again for choices already saved in the assignment.

## Add a YouTube channel

1. Open **Channel Manager → Add Channel** (`/channel_manager` → `/add_channel`).
   Reuse an existing matching channel. The app's local channel key/name and the
   real YouTube channel identity are distinct; typing a name does not select the
   corresponding Google or Brand Account.
2. Choose the supported connection method:

   | Current environment | Native method |
   | --- | --- |
   | Configured HTTPS server dashboard | **Google login → VPS dashboard**; select its installed Web project, enter the app's channel name, then **Hubungkan YouTube** |
   | Supported local Desktop flow | **Google login → Local device**; select a saved Desktop project or import its Desktop JSON once when requested by the form, then connect |
   | Existing authorization from a trusted installation | Use **Token files**, **Channel folder**, or the installed channel-transfer workflow as appropriate to the requested migration; preserve the matching client/token pair |

   Native YtFusion currently treats Linux as a server and also checks the
   request hostname; inspect installation_device and google_oauth context on
   the assigned version. This native gate is distinct from an independent
   executor's Google-supported Desktop receiver. A browser on a host alone
   does not establish that it can reach that receiver.
   If Web login lacks a configured project,
   HTTPS address, or registered callback, follow [setup](setup.md) and the sibling
   [domain/VPS skill](../../ytfusion-domain-vps/SKILL.md). Reuse an assigned client
   or supported existing authorization. When preparing a project is part of the
   setup request, execute [Google project setup](google-project.md); do not create
   a new project merely because another account login is being added.
   A configured Web dashboard does not require JSON upload for each new channel.
3. Start the native login and preserve its application/browser session. Direct
   the user to choose the intended Google account and YouTube/Brand channel and
   complete consent/2FA through the supported UI handoff. Never request passwords,
   OTPs, token contents, or an OAuth callback code in chat. Do not finish the
   callback in an unrelated browser profile or bypass its state/session checks.
4. After the callback/import completes, inspect the actual result in Channel
   Manager and available auth information. Confirm the resolved YouTube identity
   and selected project rather than the typed label alone. Record the app channel
   key and the YouTube channel ID when available. Cached auth metadata is useful
   identification, not proof of a fresh API request or successful video upload.

If consent is cancelled or incomplete, inspect the native error and retry that
login only after its cause is addressed. Preserve working credentials and data.
For an existing channel requiring a new grant, use native re-authentication or
project-switch controls rather than deleting/recreating the channel. Connecting
a channel does not start Studio, upload a trial video, or establish Live access.

For a Muse executor using local authorization, transfer only the selected
channel's matching token/client pair through supported private host transfer or
the native export/import path. Keep the original connection intact. Verify
`channels.list(mine=true)` from the **VM** matches the assigned YouTube channel
ID and record actual scopes/refresh capability without exposing tokens. A Mac
success banner alone does not prove VM access. If no private transfer is
available, request the smallest supported handoff, never tokens in chat.

## Connect Google Drive

1. Open **Google Drive** (`/gdrive-downloader`) and inspect **Koneksi Google Drive**.
   Check rclone availability, saved own client, token validity, and the displayed
   account identity. A stored token or installed rclone binary alone is not a
   usable connection. Reuse a valid connection that can access the assigned source.
2. Choose the native route available on this host:

   | Route | Action |
   | --- | --- |
   | Configured HTTPS server dashboard | **Login Google**, select the installed Web project, then **Hubungkan Google Drive**; complete the separate Drive consent |
   | Supported local Desktop flow | **Login Google** using the saved own client or Desktop JSON selected in the connection wizard, then **Login ke Google Drive** |
   | Existing connection backup | **Impor koneksi → Pilih cadangan JSON**, or its **Tempel koneksi** option, then **Hubungkan** |

   A Drive connection backup from **Detail koneksi → Unduh cadangan JSON** or
   **Salin untuk VPS** includes account access and its matching own client. It is
   not the OAuth client JSON downloaded from GCP. Import through the intended
   private UI; do not print it, paste it in chat, or put it in the skill repo.
3. Let the user complete account login and Drive consent if needed. A successful
   YouTube login does not authorize Drive, even when both use the same Web client.
   Conversely, a connected Drive account does not add a YouTube channel.
4. Refresh native status after login/import. Distinguish **Koneksi tersimpan** from
   a verified account identity. Confirm the assigned folder/file is accessible
   through the native browser/Inbox and record its stable identity privately.
   If the account cannot access a source, resolve the source/account choice or
   sharing permission; do not repeatedly replace the OAuth client.

The current Drive workflow uses the configured `gdrive` rclone connection across
the installation. Do not connect a different Drive account for each channel and
silently replace it for existing jobs. Inspect active transfers and migration
state before an authorized account/client change and honor the app's guards.
Multiple assigned source folders must be accessible to the configured connection.

For YT Upload, connection readiness and workspace registration are separate.
For an independent Muse connector, inspect the actual connector's account and
binary read/write capabilities rather than forcing the native rclone import.
Writing upload history requires a supported write operation on the assigned
Drive workspace; download access alone does not establish that permission.
Follow [YT Upload](yt-upload.md) for native workspace join/migration and package
format. For Regular/Live, use their native downloader/media-library path instead
of assuming every Drive file is an HDS package.

## Finish initial onboarding

Save only resolved account identifiers, source references, and connection choices
in the private instance assignment described in [setup](setup.md). Native app
stores retain credentials. Report each state separately: client prepared,
channel connected, Drive connected, source accessible, workspace ready if needed,
and any user login still pending. Stop only the dependent step while waiting for
required login/input; finish other authorized setup that can proceed independently.

Adding another channel later follows the same native flow, reusing installed
clients and preserving existing channels, queues, and Drive connections. Do not
repeat full installation or all account setup because the assignment expands.
