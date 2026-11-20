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
2. Inspect actual connectors, cloud browser, local computer control, execution,
   persistent storage, networking and job facilities. Choose native application
   operation or an independent executor with [Muse executor](muse-executor.md).
   For final-video work, source plus needed dependencies can suffice; a running
   YtFusion server and a full HDS generation install are not prerequisites.
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
Data API for channel/upload/API Live, Analytics API for reports, Drive API when
the own project will serve Drive. A working built-in Drive connector may use a
different project; do not replace it merely to make the project list uniform.

Research usable hosting rather than presenting a closed menu or requiring a
GitHub login. Existing hosting or Firebase Hosting Spark in the same Google
account may reduce logins; Cloudflare/GitHub or another supported provider may
fit better. Prepare a concrete solution within available access and cost. Do not
add billing or buy services as an incidental setup step. Static branding pages
and a working OAuth callback are different capabilities.

Publish truthful homepage/privacy/terms pages, free of private mappings, tokens
and draft-only notices. Describe Google and Muse/hosting processing accurately;
do not promise control over third-party advertising, analytics or retention.
Verify live pages without login, saved Branding/authorized domains, and the
actual **In production** Audience state. Record domain ownership, brand review,
scope review and any unverified-app warning separately. Publishing removes the
External Testing token condition, not all possible token expiration/revocation.

## Connect Drive and YouTube with the available route

Use a working built-in Drive connector if it can deliver binary bytes to this
VM. Rclone, a Mac connector and the native Drive UI are alternatives, not universal
requirements. Verify the assigned account can access the exact file/folder.
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

Before asking the user to focus a window, copy a file or repeat login, inspect
supported computer/file-transfer controls and use them when allowed. Confirm
the right browser profile/window is visible; repeatedly waiting on an occluded
or wrong window is not evidence the page failed. Do not convert a local control
failure into a claim that all Muse instances lack that capability.

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
