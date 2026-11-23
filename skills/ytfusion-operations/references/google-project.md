# Prepare Google Cloud, branding, and OAuth clients

Use this reference when the requested setup includes preparing an own Google
project, APIs, public branding pages, publishing, or OAuth clients. Perform the
authorized setup, install the clients, and inspect the results. A list of console
links or instructions for the user is not completion. User login/2FA, required
consent, unavailable access, and Google's review are genuine handoff boundaries;
finish other independent authorized steps while waiting.

## Identify the application and account

Read the private instance assignment and installed client metadata first. Reuse
an assigned working project. For a new project, resolve the owning Google account,
application name, support/developer contact, and intended channel/Drive accounts.
Use the user's naming choice or a clear name based on the assignment. Record the
actual project ID separately from its editable display name.

When a new project is within the setup request, select/create it in the correct
account and check the selected project before each API/client operation. Preserve
unrelated projects and clients. For a new Muse instance follow
[Muse onboarding](muse-onboarding.md): prepare a distinct project unless the user
assigns an existing one. Existing instances reuse their assigned project.
Another project is not a workaround for quota or authorization errors.
Do not attach billing or buy a domain/hosting plan without the corresponding task.

Choose the audience for the real authorizing accounts. **External** supports
separate personal Google accounts; **Internal** requires the appropriate Workspace
organization. If the current console offers **Personal mode**, do not select it
for a multi-account setup: it permits only the creator account and cannot later
be converted to External/Internal. Check current
[Google Auth Platform guidance](https://support.google.com/cloud/answer/15544987?hl=en)
rather than assuming a historical console layout.

## Enable APIs and declare the actual scopes

In the selected project, enable the APIs needed by the installed application:

| Assigned feature | API |
| --- | --- |
| YouTube channel connection, upload, API Live | YouTube Data API v3 |
| Installed channel statistics / analytics grant | YouTube Analytics API |
| Google Drive connection and transfer | Google Drive API |

Record the actual service names `youtube.googleapis.com`,
`youtubeanalytics.googleapis.com`, and `drive.googleapis.com` with their verified
ENABLED/DISABLED states. Activate missing required APIs within the setup scope;
do not ask again for routine configuration already authorized. Stop for actual
new terms, security grants or billing under the host's rules. Enabling an API
does not grant access to an account. A working Muse Drive connector can use its
own project, so it does not prove Drive API is enabled in this project.

After activation, test a relevant read endpoint with the actual grant. Distinguish
`accessNotConfigured` (service disabled), insufficient scope/account access, and
`liveStreamingNotEnabled` (channel eligibility). Data API covers Live resources;
turning it on does not activate Live on a channel. Do not enable unrelated APIs
or promise revenue access from a non-monetary Analytics grant.

For native login, inspect `SCOPES` in `src/app.py`, Drive authorization in
`src/google_oauth_routes.py`, and the configured native Drive client flow. Declare
the scopes actually requested in **Google Auth Platform → Data Access** and save.
Current channel login requests `openid`, `userinfo.email`, `youtube.force-ssl`,
`youtubepartner`, and `yt-analytics.readonly`; current Web Drive requests full
`drive` plus identity scopes. Optional **Enable earnings** also requests
`https://www.googleapis.com/auth/yt-analytics-monetary.readonly` through the same
YouTube Analytics API; include it in Data Access when that feature is assigned.
Existing channel tokens need one-time additional consent for monetary access,
not a new project/client JSON. Preserve the working connection until consent
succeeds; API activation and In production alone do not grant the scope.
Re-check these on the installed version. Do not
silently remove a required grant or add unrelated scopes copied from a generic
rclone example. If broad scopes need review, record the requirement honestly.
For an independent executor, choose scopes for its actual features and supported
login route. If later using native Add Channel, reconcile and consent to the
actual native request; its broader scopes are not limited by the earlier upload-
only declaration. Keep this distinction in the assignment.

The official [rclone own-client guide](https://rclone.org/drive/#making-your-own-client-id)
is useful for Drive project/client setup, including publish prerequisites and
GitHub Pages as a hosting option. YtFusion's Web/YouTube flows require their own
matching configuration; do not copy rclone's Desktop setup for every server.

## Choose public hosting that can actually be used

Prepare the public pages before attempting branding publication. Use existing
working pages when suitable; do not impose GitHub Pages on every installation.
For a **new Muse branding site**, the preferred first route is **Firebase Hosting
Spark** in the assigned Google account/project, as demonstrated by the pilot.
Attempt that supported no-billing route before asking the user to choose another
provider. Preserve an explicitly assigned site; fall back when Firebase cannot
satisfy a concrete access, plan, ownership or deployment requirement.

| Available access | Preferred action |
| --- | --- |
| Existing app site or public VPS site under the user's control | Inspect and reuse/update its homepage, privacy, and terms through the supported site workflow |
| Google owner login and suitable same-project Firebase Hosting access | First choice for a new Muse branding site: deploy on Spark, verify the current no-billing plan/terms and public pages |
| Cloudflare access and an assigned domain | Deploy a small static site to Cloudflare Pages and bind the assigned domain/subdomain |
| GitHub access and a suitable Pages site | Deploy a separate static Pages site; use its accepted/verifiable URL or an assigned custom domain |
| Neither usable hosting nor access | Prepare the site files privately, request the missing access/hosting choice, and continue independent project setup |

These are examples, not a closed provider list. Minimize user logins and manual
work while choosing a supported solution. The pilot used Firebase Hosting Spark
for public branding and reached In production without GitHub Pages or billing.
Static Firebase Hosting does not itself execute a Python OAuth callback or store
refresh tokens for a VM. Backend additions such as Functions/Cloud Run have
different requirements and can require billing; check current
[Firebase hosting guidance](https://firebase.google.com/docs/hosting/functions)
before proposing them. Do not turn on billing to unblock a setup silently.

With Cloudflare Pages, use its current
[Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/)
or supported Git deployment route. For a custom hostname, register it in Pages
**Custom domains** as well as configuring DNS; a CNAME alone is insufficient.
Follow [Cloudflare's custom-domain instructions](https://developers.cloudflare.com/pages/configuration/custom-domains/)
and preserve unrelated DNS records. With
[GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages),
publish only the intended static public files. Never make the Private app repo
public or include OAuth downloads, tokens, channel data, or private ledgers in a
public site/repo. Inspect plan/access limitations rather than buying an upgrade.

Create coherent pages with the chosen app name and real contact details:

- Homepage: what this YtFusion deployment does, its operator/contact, and links
  to privacy and terms. The content must match the OAuth application.
- Privacy: the actual Google data accessed, purposes, storage/sharing, retention,
  and how the user can revoke access or request deletion. Describe the installed
  agent/hosting workflow truthfully; do not copy claims such as data never leaving
  a device when the agent, server, Drive, or YouTube receives it.
  Name the actual processing services as appropriate; avoid guarantees about
  third parties' advertising, analytics or retention that the operator cannot
  make. Describe retained verification records and deletion requests accurately.
- Terms: the actual service/use terms for this deployment, consistent with the
  requested private or public use. Do not invent an organization or certification.

Open each final HTTPS URL without login, check the rendered content and links,
and confirm deployment success. Remove private-draft notices from the published
pages; do not publish credentials or the private instance/account mapping.
Files written locally, a pending build, a preview
with authentication, or a URL returning an error is not a published branding site.

## Configure Branding and verify ownership when required

Fill **Branding** with the correct name, monitored support/developer contacts,
homepage, privacy and terms URLs, and actual authorized domains. Google's
[brand requirements](https://developers.google.com/identity/protocols/oauth2/production-readiness/brand-verification)
require publicly accessible relevant pages and proof of authorized-domain ownership
for brand verification. A hostname merely resolving does not establish ownership.

Use [Search Console](https://support.google.com/webmasters/answer/9008080?hl=en)
with the relevant project Owner/Editor account. For an owned custom domain,
use its Domain property and the supplied DNS verification record. When using a
hosted URL, use an available ownership method and verify that the property/domain
is accepted for the actual OAuth application. Do not claim ownership of the
shared parent `github.io`, `pages.dev` or `web.app`. If the hosted address cannot satisfy
the required check, use an assigned custom domain or existing verified site.
Preserve successful verification records/tags and other owners' tokens.

Changing draft Branding is not necessarily publishing it. Inspect **Verify
Branding / Publish branding / Verification Center** as actually offered. Complete
the requested available action and record whether the result is verified,
published, pending review, or blocked by a specific requirement. Never substitute
a screenshot of saved fields for verified/published status.

## Create the appropriate OAuth clients and install them

| Needed login | Client and destination |
| --- | --- |
| Direct login through a working HTTPS YtFusion server dashboard | Web application; register the exact callback shown by that installed app |
| Supported local login and later auth/Drive connection transfer | Desktop app; use the native local login/import route |
| Both assigned paths | Create or reuse both types in the same selected project |

Get the real callback from the running app, normally ending in `/oauth2callback`;
match scheme, hostname, port, and path exactly. Do not assume the public homepage
is the callback. Static branding pages on GitHub Pages or Cloudflare Pages do not
run YtFusion's Python callback. If Muse lacks a usable HTTPS app endpoint, prepare
the supported local-login/auth-import path in [Channels and Drive](accounts.md),
or report the concrete endpoint requirement. Do not register a static landing
page as a pretend callback. Native YtFusion's Linux server gates do not establish
that every independent executor has identical login capabilities; evaluate the
actual receiver/browser and Google's client-type requirements. See
[Muse onboarding](muse-onboarding.md) for the proven local-login/transfer route
and criteria for researching alternatives.

Download the original client JSON privately when creating it, check its actual
`web`/`installed` type and project ID without exposing the secret, then use the
installed management/import workflow. Follow the sibling
[domain/VPS skill](../../ytfusion-domain-vps/SKILL.md) for managed snapshots and
original private archives. Install and inspect the selected project binding on
the target; downloaded JSON alone does not configure the app. Preserve existing
client secrets, channel grants, and Drive connections during ordinary additions.

## Publish the audience and finish real connections

For the requested long-running External setup, use **Audience → Publish app**
and inspect **In production** afterward. If unavailable, inspect the actual
Branding/Verification Center requirements, fix the authorized missing items and
recheck. Do not leave it in Testing and report completion. Testing grants with
YouTube/Drive scopes normally have a seven-day refresh-token lifetime;
[Google's refresh-token rules](https://developers.google.com/identity/protocols/oauth2#expiration)
also allow revocation/expiration for other reasons. In production is not a
promise that tokens never expire. Reauthorize through native controls if an
existing grant needs renewal; preserve working connections until replacement.

Audience publishing, published/verified branding, domain ownership, scope review,
and channel/Drive consent are separate results. Follow the actual
[scope-review requirements and applicable exceptions](https://developers.google.com/identity/protocols/oauth2/production-readiness/restricted-scope-verification).
Prepare truthful supporting material and submit review when that is within the
requested scope and access permits it. A pending Google decision remains pending;
do not invent approval or hide an unresolved requirement by removing app scopes.

Finish the actual channel and Drive connections using [accounts](accounts.md),
then verify source access. Record project/account metadata, enabled APIs, actual
scope declarations, public URLs/deployment, ownership verification, publishing and
review states, client types/callbacks, private credential references, and native
connection results in the instance assignment/progress. Never store secret values
there. Report concrete completed results and the smallest genuinely pending step.
