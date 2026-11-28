---
name: ytfusion-upload-workspace
description: Build or update a private Muse YT Upload Space with a real Drive Inbox, durable Upload Queue and upload History, following current YtFusion source and bundled visual references. Use for browsing available Drive packages, selecting videos and inspecting or preparing executor jobs; actual transfers require the instance's upload authorization.
---

# YtFusion Upload Workspace

Respond in the user's language; keep the workspace UI in English. Reuse the
instance's assigned Drive, channels, existing executor and private state. This
skill builds the operator's visual workspace; use
[Operations](../ytfusion-operations/SKILL.md) for Google onboarding and actual
transfer/finishing/receipt/cleanup procedures.

## Build from actual capabilities

1. Inspect the saved assignment and any existing upload Space before creating
   anything. Reopen/update that Space on later requests. Keep Channel Analytics
   separate. A new channel, Drive folder or account is assignment data, never a
   hardcoded skill edit.
2. Read [workspace contract](references/workspace.md), open the
   [native visual references](references/ui-reference.md), and inspect their
   relevant current source. Give the builder the images and data/action brief;
   the user should not need to supply screenshots.
   Use [native CSS as build input](references/ui-reference.md#reuse-the-current-native-css),
   including current inline/theme rules and matching component classes. Verify
   visual parity as well as working data/actions. Keep the assigned app checkout
   authoritative rather than maintaining a second CSS source in the skill.
3. Establish which host-supported Space actions, persistent storage and worker
   read/write routes actually work. Prefer direct UI actions when supported.
   Do not assume a snapshot-only limit from an older artifact or promise that
   arbitrary VM processes are reachable from the frontend. No tokens, resumable
   session URLs or private machine paths belong in the frontend.
4. Build one private **YT Upload** Space with **Drive Inbox**, **Upload Queue**
   and **History**. Use real assigned metadata and receipts; preserve stable
   source/job identities, last-successful data and honest partial/error states.
   Implement the smallest useful end-to-end path before exposing more controls.
5. Verify in the real viewer: filtering, video detail/thumbnail, select → save
   draft/held queue → reload → worker dry-run reads that same job. Retrying the
   same action must not create another job. Inspect desktop and narrow layouts.
   This proof must not perform an upload, download full media, modify Drive or
   activate a recurring task. Keep authorization flags unchanged.

## Keep operation and evidence consistent

Use one authoritative durable job store or an explicitly versioned bridge with
acknowledgements. Space cards, worker output and chat notes must not become three
independent queues. Show saved, held, eligible, running, accepted and complete as
their actual states. Saving a draft or date does not authorize execution.

Expose Start, schedule, Pause, Cancel, Retry or cleanup only when the assigned
executor implements their semantics and the action's authorization is resolved.
A held queue and implemented read-only worker contract are useful completion
milestones; report missing execution legs honestly instead of adding decorative
controls or switching to native YtFusion. Retain existing native installations
and queues without starting them for an `agent_executor` assignment.

Deliver the stable Space link/card in the chosen chat, record its identity and
source/skill revisions privately, and distinguish viewer storage, worker access,
real Drive reads and live transfer verification. Repository sync alone does not
update a Space or implement a worker.
