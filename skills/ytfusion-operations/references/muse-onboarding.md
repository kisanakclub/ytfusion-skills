# Set up a Muse operations instance

Read this for a new Muse, a changed assignment, or missing onboarding. Continue
from the private assignment and actual state; do not reinstall on every chat.
The outcome is an instance that can perform its assigned workflow with minimal
user intervention. Setup alone does not authorize an upload, publication or Live.

## Discover once, save the decisions

1. Obtain the skill package and the assigned YtFusion source following
   [setup](setup.md). Install/register the required skill folders using Muse's
   supported mechanism and verify discovery. Record the source and installed
   skill revisions; updating a checkout alone does not update an installed copy.
   Also inspect host-generated discovery metadata when search still shows old
   capabilities. Refresh it through the supported registration mechanism, or
   synchronize supported descriptive fields from `SKILL.md` while preserving
   host policy/dependency fields. Matching source hashes alone does not update
   a separate host catalog such as a generated `skill.yaml`.
   Include [Upload Workspace](../../ytfusion-upload-workspace/SKILL.md) in
   discovery during setup. When a visual Drive Inbox, Upload Queue or History is
   assigned, open its bundled captures and reuse the existing private Space for
   that assignment when possible. Verify the Space-to-worker connection with a
   held job before enabling execution controls.
2. Inspect actual connectors, cloud browser, local computer control, execution,
   persistent storage, networking and job facilities. Follow an existing mode
   choice. For a new Muse final-video uploader, prefer `agent_executor` when its
   supported connectors/APIs meet the workflow; use native operation when assigned.
   See [Muse executor](muse-executor.md). Source plus needed dependencies can
   suffice; a running YtFusion server, native Drive onboarding and a full HDS
   generation install are not prerequisites for an independent executor.
3. Resolve only missing choices: instance role, GCP owner/browser profile,
   channel and account, Drive account/source, branding/contact, and task scope.
   GCP, channel and Drive accounts may differ. A profile name, Gmail tab or typed
   channel label is a lead; verify the account at consent and channel ID by API.
4. For a **new Muse instance**, prepare a **new project** unless the user assigns
   an existing one. Offer a distinct role-based name such as `<owner>-muse` and
   save the actual ID. Never reuse the project currently selected in a browser
   without checking the assignment. Later tasks on this instance reuse its
   assigned project; this is not a way to multiply quota for the same service.
5. Save resolved identifiers, credential references, chosen execution/login
   route, public URLs and readiness evidence outside both repos and public web
   roots. Follow the private assignment in [setup](setup.md). Have the agent
   create/update it; do not ask the user to compose JSON or repeat known inputs.

## Google project, branding and publication

Execute [Google project setup](google-project.md), including the API readiness
table and actual account connections. Verify APIs before declaring completion:
Data API for channel/upload/API Live, Analytics API for reports, Reporting API for thumbnail impressions/CTR and traffic reach, Drive API when
the own project will serve Drive. A working built-in Drive connector may use a
different project; do not replace it merely to make the project list uniform.

Resolve runtime, branding host and login receiver independently using the
[Google setup routes](google-project.md#resolve-runtime-branding-and-login-independently).
Use the actual project/grants for upload, Publishing and Analytics readiness;
saved setup checkboxes or client archives alone are not connection evidence.

For a new Muse branding site, use **Firebase Hosting on Spark as the first
choice**, preferably in the assigned Google project/account, following the
successful pilot. Check the current no-billing plan, access and terms, then
prepare and deploy homepage/privacy/terms and verify their public HTTPS URLs.
Do not make the user select from a hosting menu or research every provider first.
Preserve an explicitly assigned working site. If Firebase is unavailable or
cannot meet an actual requirement, diagnose that constraint and choose suitable
existing hosting, Cloudflare, GitHub or another supported alternative. Do not
add billing or buy services as an incidental setup step, or enable Google
Analytics merely to host the pages. Static branding pages and a working OAuth
callback are different capabilities; this preference does not choose a login route.

Publish truthful homepage/privacy/terms pages, free of private mappings, tokens
and draft-only notices. Describe Google and Muse/hosting processing accurately;
do not promise control over third-party advertising, analytics or retention.
Verify live pages without login, saved Branding/authorized domains, and the
actual **In production** Audience state. Record domain ownership, brand review,
scope review and any unverified-app warning separately. Publishing removes the
External Testing token condition, not all possible token expiration/revocation.

## Connect Drive and YouTube with the available route

Use a working built-in Drive connector if it can deliver binary bytes to this
VM. For upload assignments, also inspect its supported JSON receipt create/read
operations and access to the existing workspace's history folder; download alone
does not establish post-upload recording capability. Do not write a fake receipt
as a probe. Rclone, a Mac connector and the native Drive UI are alternatives, not
universal requirements. Verify access to the exact assigned file/folder.
Enabling an API, installing client JSON and granting account access are separate.

For YouTube, establish a supported complete route, then use the matching client:

| Available capability | Route to evaluate |
| --- | --- |
| Existing valid channel grant assigned to this executor | Preserve and use its matching token/client pair; verify from this VM |
| Reachable configured HTTPS application/backend | Web flow with its exact registered callback |
| Local browser and supported receiver on the same machine | Desktop flow, including native YtFusion Add Channel when available, followed by private transfer to the VM |
| Other host capability | Research and demonstrate a supported route; do not assume it is absent or force the options above |

The pilot's proven route was local YtFusion Add Channel followed by private
transfer and a successful `channels.list(mine=true)` from the VM. It is a usable
fallback, not a requirement to install the same Mac/profile for every instance.
Native connection details are in [accounts](accounts.md). Inspect its actual
scope request: native YtFusion can request broader access than an independent
upload-only client. Do not silently change scopes or assume the consent-screen
declaration limits what the application requests.

Desktop loopback requires a real receiver reachable by the authorizing browser.
Do not copy a code from a failed loopback URL or revive deprecated OOB login.
Evaluate device flow against current Google app-type requirements and allowed
scopes, not just whether an API accepts a request. The pilot did not establish a
supported device-flow deployment; do not install a TV client as the default for
every server or promise full Analytics/revenue access through it.

Keep original client downloads when creating them: a later download may not
recover the same secret. Use supported private file/credential transfer with
owner-only permissions. Match client/project/channel before and after transfer;
never request tokens, passwords or auth codes in chat. Preserve existing grants.
For a CLI login, inspect the installed version's actual handoff/state contract
rather than assuming its process must remain alive; a URL or exited process
alone proves neither success nor failure. Exchange short-lived codes promptly.

## Continue autonomously within authorization

Navigate, read source, stage files, verify identities, and complete ordinary
confirmations whose facts you have verified. Once the user authorizes work,
continue until its outcome or a real blocker; do not wait for another “continue”
after each step. Group unresolved choices and prepare reviewable requests.
Legal terms, new credentials/grants, security warnings and host approval cards
follow the host's actual rules; a skill never grants or bypasses permission.

Collect known setup inputs in one short batch: role, account/profile mapping,
source/destination, branding contacts, privacy/timezone/cadence when assigned,
and separate local/Drive cleanup. Save answers and use reasonable app defaults
for routine choices. Prepare concrete approvals together when they are ready;
do not demand blanket consent to grants/terms whose scope is not yet known.
Explain available reusable host permission modes and their actual scope if the
user wants fewer prompts, but never change approval settings or blocked apps
as a side effect of onboarding. Reusable permission does not add tool abilities.

Before asking the user to focus a window, copy a file or repeat login, inspect
supported computer/file-transfer controls and use them when allowed. Confirm
the right browser profile/window is visible; repeatedly waiting on an occluded
or wrong window is not evidence the page failed. Do not convert a local control
failure into a claim that all Muse instances lack that capability.

In the pilot Mac tool, `open_app` could launch Chrome, but the documented browser
control targeted existing windows without a profile selector and did not bring
apps to the foreground. Do not assume another agent's window-raising API exists
in Muse. When no supported profile-opening/focus route is available, ask once
for the intended profile/window to be prepared for login; do other preparation
first. This is a bounded initial handoff, not a requirement to keep the Mac in
front for VM uploads. Verify current tools before carrying this limitation to
another host/version; a locked/asleep Mac or blocked app is a separate condition.

## Channel dashboard during full first-run setup

When the assigned first-run setup includes Channel Analytics, install/register
the sibling ytfusion-channel-analytics skill and verify discovery. Read its
SKILL.md, dashboard/data references, bundled UI screenshots and Publishing
reference. Supply the images to the artifact builder; the user should not need
to capture the native app. Compare with the assigned current source and its
included assets before building the same private Library artifact.

Full channel-stats-style setup includes Statistics and the read-only Publishing
overview, English labels by default, filters, charts, available earnings/RPM,
Privacy, separate refresh timestamps and the user's chosen Analytics chat.
Record source/skill revisions and verify the delivered viewer. Missing revenue
permission stays explicit; do not initiate a new grant just to fill a screenshot.
An uploader-only assignment does not require creating this dashboard.

On an assigned update, reconcile source/skill changes with the existing artifact;
updating the repo or installed skill does not update the artifact automatically.
Preserve its identity, snapshots, connections and chat preference. Schedule
editing/upload actions remain separate from read-only dashboard setup.

## Finish with evidence, not a readiness promise

Read the [upload workflow contract](upload-workflow.md) **before** implementing
the first uploader. Source metadata alone does not include every YT Upload default
or finishing operation. Check actual source, scopes, API activation and channel
eligibility; fix the relevant missing leg without repeating all onboarding.

When authorized, prove download identity/size/hash, then one assigned upload and
its settings, thumbnail, playlist, recognized Drive history and selected cleanup.
Report each stage separately. A missing history receipt or retained cleanup is
pending work, not an excuse to upload again. Before recurring operation, resolve
cadence/timezone, publication intent, overlap control and durable recovery using
[Muse executor](muse-executor.md). Do not infer these from a successful private
upload. Regular Studio, render and sustained Live need their own assigned proof.

Maintain private operational evidence and assignment state. Skill authorship and
repo publication belong to the maintainer unless the user explicitly delegates
them; running this skill does not authorize Muse to rewrite its shared guidance.

For full Analytics onboarding, also follow the current Channel Analytics data
contract for Reporting activation, a reused Reach Combined job, pending/history
coverage, manual cache refresh, and API/project identity. Collect the dynamic
project manager/channel/Drive assignment once; no pilot Gmail or project is a
default. Use the bundled native screenshots (including Traffic, Browse and API
info) plus current source when briefing an artifact builder. Verify the actual
executor/backend refresh action and the same existing private artifact; pulling
the skill repo or swapping images alone does not implement these behaviors.

Check the assigned VM's network transport before diagnosing Google setup from a
timeout. Some VM tools use an approved proxy path that an SDK does not pick up
automatically. Preserve TLS verification and use bounded requests; keep network
approval, API activation, OAuth grants and report availability distinct. A Reach
connection failure does not block other reports or the cached dashboard. Resume
from durable checkpoints after a host response failure rather than repeating
account setup, completed fetches or artifact creation.
