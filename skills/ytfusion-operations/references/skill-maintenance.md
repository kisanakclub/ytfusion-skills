# Keep operating skills aligned with application changes

Use this when assigned to maintain YtFusion source, skills or their onboarding
instructions. Routine uploads/reports use the existing guides and assignment;
they do not require editing repositories.

## Choose the affected guide

| Source change | Guides to review |
| --- | --- |
| YT Upload queue/modes, timing, cancellation, retry | [YT Upload](yt-upload.md), [Muse executor](muse-executor.md); current docs/yt-upload-channel-queue-plan.md and dispatch/reschedule handlers |
| Payload/defaults, Original/Extend, receipt, history or cleanup | [Upload workflow](upload-workflow.md); package, uploader, receipt and completion helpers |
| Channel Statistics, Publishing, chart or metrics | [Analytics skill](../../ytfusion-channel-analytics/SKILL.md), its data/dashboard/Publishing references and [visual source map](../../ytfusion-channel-analytics/references/ui-reference.md) |
| Google project/API/scopes, OAuth, branding, domain setup | [Google project](google-project.md), [Accounts](accounts.md), [Domain/VPS](../../ytfusion-domain-vps/SKILL.md), [Muse onboarding](muse-onboarding.md) |
| Agent Setup instructions, install/update/discovery | [Setup](setup.md), [Maintenance](maintenance.md), [Muse onboarding](muse-onboarding.md), package README and the app's src/static/js/agent_setup.js |
| HDS workflow exposed to an operating agent | Relevant [HDS guide](../../hds-home-production/SKILL.md) and the installed app's product/feature guidance |

Read only the changed behavior and its direct consumers. Distinguish HDS's Muse
media provider from Muse operating as an upload/Analytics executor; a change to
one does not require rewriting the other's instructions.

## Close the same change

1. Establish the app and skill revisions and preserve existing dirty work.
   Compare the assigned source diff with the relevant guide, including linked
   helpers/partials and actual request/response fields. Reuse an existing skill
   checkout; a clone alone is not proof that its installed copy is current.
2. Update instructions when an agent's decisions, defaults, fields, controls,
   recovery or completion evidence change. Keep native_app and agent_executor
   routes distinct. An internal refactor can leave guidance unchanged; state
   briefly why it remains valid. Do not turn a pilot account or one user's job
   into a default for every instance.
3. For a UI change, update the source map and reviewed synthetic screenshots
   when their baseline changes. Inspect the source and images before briefing
   a builder; the user should not need to supply screenshots for normal setup.
   Preserve real-data/permission/privacy requirements regardless of the fixture.
   For prompt changes, align the app entry point, README and onboarding reference.
4. Validate changed manifests, relative links and examples. Execute a changed
   helper on disposable data; visually inspect refreshed images. Use existing
   focused app checks for changed code, not a broad unrelated suite. A documented
   procedure or fixture is not live Google/Muse/production evidence.
5. Report the skill files updated, or why no skill change was needed, with the
   relevant verification. When publication is assigned, publish each repo through
   its own workflow and verify Publish Shared for an app source push as required
   by the installed runbook. Preserve other work and never publish credentials.

Record installed copies and discovery separately from repository revisions.
When instance updates are assigned, inspect work in flight, synchronize supported
skill metadata without replacing host policy, then adapt the existing executor
or artifact to the relevant contract changes and verify it on that host.
Keep its identity, grants, ledger, snapshots and jobs. Updating a repo does not
change a running worker, an installed skill copy or a generated Muse dashboard.
