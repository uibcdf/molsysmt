<!--
SYNCHRONIZED MOLSYSSUITE GUIDE — DO NOT EDIT COMPONENT COPIES.
Canonical source: https://github.com/uibcdf/molsyssuite/blob/main/MOLSYSSUITE_GUIDE.md
Propose changes in: https://github.com/uibcdf/molsyssuite/issues
-->

# MolSysSuite component guide

This file is the local ambassador of `uibcdf/molsyssuite` in every component. It gives
contributors the operational rules needed during ordinary development and routes them
to the complete, authoritative governance documents. Component copies are synchronized
from the canonical file above; changes belong in the MolSysSuite repository.

## Where suite governance lives

Use [the MolSysSuite repository](https://github.com/uibcdf/molsyssuite) for MolSysSuite-specific compatibility contracts, member governance, domain extensions, common suite tooling, cross-component proposals, coordinated rollouts, and decisions affecting two or more suite members. Its `suite.toml` is the
machine-readable registry of members, classification fields, initiatives, and accepted
policies. Its `devguide/` contains the full normative texts and decision history.

The component repository remains authoritative for its implementation, tests, product
API, scientific evidence, releases, and local development tools. Local rules may be
stricter, but they must not silently contradict a common policy. A deviation needs a
tracked exception with its reason and expiration condition.

MolSysSuite is a first-class MOLI component with delegated internal governance. MOLI governs the suite's platform boundary. MolSysSuite owns normative engineering and modeling rules, rollout and enforcement for its registered members.

A member follows **MolSysSuite member governance + repository-local rules**. MolSysSuite as a unit remains accountable for its MOLI platform contracts.

The current central member-policy release is MolSysSuite `policy-v1.5.4`, as
recorded in `suite.toml`. Each member's effective automated policy is the
release pinned by its workflow; older compatible releases remain visible in
the adoption inventory. The MOLI commit recorded in `suite.toml` identifies
platform-contract context for the suite; it is not a source of member
engineering values.

The wider platform architecture belongs to [MOLI Architecture 1.0](https://github.com/uibcdf/moli/blob/main/architecture_1.0/README.md). MolSysSuite is a first-class MOLI component with delegated internal governance. MOLI describes MolSysSuite as
the molecular modeling ecosystem alongside Scientific Context and optional
MOLI Agent reasoning.

Start with these central documents:

- [repository ownership contract](https://github.com/uibcdf/molsyssuite/blob/main/devguide/repository_contract.md);
- [issue and developer-guide reporting protocol](https://github.com/uibcdf/molsyssuite/blob/main/devguide/reporting_protocol.md);
- [cross-component feedback policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/cross_component_feedback.md);
- [MolSysSuite Python support policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_policy.md);
- [MolSysSuite CI policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_ci_policy.md) and [quality tooling policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_tooling_policy.md);
- [MolSysSuite support-library and developer-tool policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_ecosystem_policy.md);
- [MolSysSuite release-version policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/release_version_policy.md);
- [MolSysSuite distribution policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_distribution_policy.md);
- [GH Run Receptor dogfooding policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/gh_run_receptor_policy.md).

MOLI's conceptual architecture does not admit repositories to MolSysSuite.
`suite.toml` alone records governed members; its `role`, `membership`,
`maturity`, `development-mode`, and `capabilities` fields classify real
repositories rather than platform concepts.

Consult MOLI governance when changing MolSysSuite's platform obligations or a contract with another MOLI component. Consult MolSysSuite governance before changing a member engineering rule, suite-member contract, dependency boundary, reusable workflow, vendored integration guide, or behavior expected across members.

Canonical-guide publication and versioned policy adoption are independent. A guide-only
change does not require a policy caller bump, and a caller bump does not prove that guide
copies were synchronized. Use the central `devtools/scripts/adoption_status.py` inventory
and `devguide/adoption_lifecycle.md` procedure to find the responsible consumer, observed
state and next action for each relationship.

## Durable working instructions

Follow the [durable working-instruction policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/working_instructions_policy.md).
Keep technical findings in owning issues, fixes, tests and maintained technical
guidance. When normal review accepts a lasting contributor or agent action,
place repository-wide instructions in root `AGENTS.md` and directory-specific
actions in the relevant nested file. Include the accepted action with its
decision, or track distinct adoption work with an owned issue; a defect does
not automatically require another instruction or issue.

For work in `devguide/`, read `devguide/AGENTS.md`, the root instructions and
the local reporting protocol. Start with current guidance and relevant active
queues; use archive indexes for orientation and open historical records for a
stated question. Preserve local queue layouts and commands. Propose working
rules useful to other members in `uibcdf/molsyssuite` with local evidence;
cross-MOLI contracts belong in `uibcdf/moli`. Upstream changes require explicit
suite adoption. Mechanical checks verify active routes, not prose quality;
bounded exceptions and member adoption are recorded by the policy. Future
human-facing reporting integration remains uibcdf/molsyssuite#65.

## Cross-repository working state

Before work spanning components, use the MolSysSuite checkout to refresh and inspect every
registered component:

```bash
python devtools/scripts/suite_status.py
```

The command puts current initiative priorities first, then follows registry order from
`suite.toml`, fetches remotes, and
reports dirty, ahead, behind, missing, or upstream-less checkouts. It does not modify a
component worktree, merge, rebase, stash, commit, or push. Resolve or explicitly preserve
every reported item before a coordinated change. Use `--no-fetch` only for an explicitly
offline snapshot and repeatable `--repository` selectors for a bounded inspection.

## Reporting bugs and proposals

Everyone who uses, develops, maintains or operates a suite component or UIBCDF support
tool must report actionable bugs, missing capabilities, improvements and new feature
proposals in the owning repository. Open an issue or add evidence to an existing one;
if you cannot file it, ask a maintainer to record it. Do not leave the finding only
in a chat, workaround or downstream issue. Reporting does not promise immediate
implementation. Use private reporting first for exploitable or confidential findings.
This adopts [MOLI's universal issue-feedback commitment](https://github.com/uibcdf/moli/blob/8056b7861ce9238d75a3b957322d839ccb6c7ca6/devguide/governance/reporting_protocol.md#universal-issue-feedback-commitment).

Decide ownership before filing:

- one-component behavior is tracked in that component;
- a shared rule or coordinated change is tracked in `uibcdf/molsyssuite`;
- a central decision may link concrete implementation issues in affected components.

For work that needs durable analysis, open the owning GitHub issue first and then create
the component's `pending_bugs` or `pending_proposals` record. The issue is its stable
identity; the document holds measurements, alternatives, reasoning, and acceptance
criteria. Every queued document has an issue, although not every incoming issue needs a
document.

Use the common statuses `open`, `active`, `blocked`, `partial`, `resolved`, `withdrawn`,
and `superseded`. On closure, cite a durable test or normative rule, synchronize the
issue, regenerate local indexes, and archive the document. Archive, never delete.

When an issue owned by one repository has a concrete relationship with another registered
component, add `component:<name>` for every related component and explain the relationship
in the issue body. For example, MolSysMT work requested by DockingMT uses
`component:dockingmt`. These labels are created on demand through the central
`component_issue_labels.py` tool; do not invent unregistered suffixes or use a component's
own label in its repository. The central reporting protocol defines the full procedure.

For defects resolved on or after 2026-09-20, a `guard` must be mechanically addressable
by the repository's documented runner. In the default Python profile use one safe pytest
module, function, or class-method selector under `tests/` or `devtools/tests/`; nonexistent
nodes, globs, parameter IDs, comma-separated targets, and shell commands are rejected.
Automation proves addressability, not relevance: the resolution must explain why the
selected assertion protects the reported failure mechanism. Non-pytest repositories or
targets require a bounded local selector profile as defined by the central reporting
protocol.

## Shared stewardship across components

Every component is a UIBCDF team development. When developing one component reveals a
missing, limiting, unsafe, or expensive capability in another, report it in the provider
repository with the consumer's reproduction, measurement, integration context, and
impact. Cross-link any consumer-side workaround or blocked work.

For example, a MolSysViewer contributor limited by SMonitor opens or updates a SMonitor
issue; the limitation must not remain hidden only in MolSysViewer. Provider maintainers
own triage and priority, while the discovering contributor owns a clear evidence handoff.
A local workaround may unblock work, but it must name the provider issue and its removal
condition. Do not silently fork sibling functionality.

For a fix in another owner's repository, use its issue for a nonurgent need
without a ready fix, or submit a concrete fix as a linked pull request for owner
review. For urgent work by or directly supervised by Diego (`dprada`) or Liliana
(`LMMV`), ask which route to use; direct commit and push require their explicit
authorization. Authorization already given for the same work remains valid
within its scope; do not request it again for every commit. Other contributors
do not inherit it. Owner-local development and the accepted internal-maintainer
direct-push/CI routes retain their own rules. Follow the
[cross-repository contribution route](https://github.com/uibcdf/molsyssuite/blob/main/devguide/cross_component_feedback.md#contributing-a-fix-to-another-repository)
for applicability and bounded exceptions.

When changing any shared auxiliary library, reusable workflow, development/publication
action or canonical guide with plausible consumer impact, open or update a linked
MolSysSuite impact issue. Give notice before publication or rollout when foreseeable,
and promptly after a later discovery. Identify affected/candidate consumers from the
registered guide, dependency and publisher inventories; include exact old/new versions
or commits, observable effects, migration/fallback, evidence, unknowns and follow-up
owners. Deliver the handoff to affected members' owner issues and record notices,
adoption commits and tested/public artifacts separately. Reuse the issue for the same
theme. Provider implementation and release ownership, internal direct pushes and the
accepted CI lanes follow their existing policies.

Use the [shared-provider impact rule](https://github.com/uibcdf/molsyssuite/blob/main/devguide/cross_component_feedback.md#shared-provider-changes-and-consumer-impact)
for applicability, timing and bounded exceptions. Cross-link MOLI when its direct
components or platform contracts are affected. One-consumer findings stay local until
wider impact becomes plausible; confidential findings use private reporting first.

## UIBCDF development support

MOLI [catalogs four UIBCDF-owned support resources](https://github.com/uibcdf/moli/blob/8056b7861ce9238d75a3b957322d839ccb6c7ca6/devguide/governance/support_infrastructure.md):
[Pytest Receptor](https://github.com/uibcdf/pytest-receptor) for Python test reporting,
[GH Run Receptor](https://github.com/uibcdf/gh-run-receptor) for Actions inspection,
[the Conda build/upload action](https://github.com/uibcdf/action-build-and-upload-conda-packages)
for applicable Conda releases, and
[the Sphinx-to-Pages action](https://github.com/uibcdf/action-sphinx-docs-to-gh-pages)
for applicable Sphinx documentation publication. Use the applicable resource and report
tool defects or improvements in its own issue board. MolSysSuite governs member
use and adoption; MOLI owns direct-component usage and suite-level platform
obligations. The receptors remain suite auxiliary members.

## Physical quantities and units

A quantity must retain its value, unit and scientific meaning across computations,
storage and component boundaries. Serialized values carry their negotiated unit in
the same object; readers verify the record and explicitly name the expected field and
unit or dimension. Never infer a unit from a bare number, field name or session default.
Use an explicit target unit for boundary conversions and test under a non-default
session policy. A wrong but internally consistent source also needs domain checks.
The [published MOLI quantity integrity policy](https://github.com/uibcdf/moli/blob/8056b7861ce9238d75a3b957322d839ccb6c7ca6/devguide/policies/quantity_integrity_policy.md)
defines the target contract; member adoption is tracked below and is not established
by this guide alone.

PyUnitWizard owns the [serialization design](https://github.com/uibcdf/pyunitwizard/issues/83)
and [QuantityRecord codec](https://github.com/uibcdf/pyunitwizard/issues/82); take
format questions there. [MolSysSuite #46](https://github.com/uibcdf/molsyssuite/issues/46)
tracks member adoption and migrations. A member's engineering policy remains the
MolSysSuite release pinned by its workflow until that member adopts another release.
The MOLI commit in `suite.toml` records platform-contract context for the suite.

## Common development baseline

MolSysSuite owns member Python support, CI, Ruff, support-library,
developer-tool, distribution and public-release rules. `suite.toml` and the
called suite policy release supply their machine-readable values. Follow the
[Python policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_policy.md),
[CI policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_ci_policy.md),
[tooling policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_tooling_policy.md),
[ecosystem policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_ecosystem_policy.md),
[distribution policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_distribution_policy.md)
and [release policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/release_version_policy.md)
for adoption, evidence and historical exceptions. Type checking and scientific
or UI gates remain repository-local.

The new support-library and developer-tool policies require member-specific review.
Their publication does not establish adoption by a member. `suite.toml` records
each Python member's separate review states, and
`devtools/scripts/python_ecosystem_status.py` displays them.

Every registered Python package must adopt Python 3.11–3.14 support
(`>=3.11,<3.15`) in its metadata, environments, recipes, required full CI and
installed-package gates. Routine local development and push/PR tests use Python
3.14. The full matrix still covers every supported minor. This
requirement applies to incubating and auxiliary components too; joining an
initial transition cohort is not a prerequisite. Track incomplete adoption in
the owning component and the central rollout `uibcdf/molsyssuite#51`; a
temporary deviation needs a reason, owner and expiry/removal condition.

The common requirement does not certify an untested interpreter or a public
release. `suite.toml` records component-specific qualification; only components
marked `admitted` may advertise delivered 3.14 support. Preserve truthful
release/badge evidence while completing the required migration. Follow the
existing internal direct-push and deferred-test routes; this range change does
not require a full suite after every internal push.

Every root integration guide synchronized from another repository is generated, read-only content. List its exact path in Ruff `extend-exclude`; propose changes at the canonical source and resynchronize the exact copy. The suite checks the exclusion and byte-level drift.

## Modular reusable tools

Before implementing a new or changed capability, inspect existing tools and identify
the owning domain/module or MolSysSuite provider. Reuse supported operations. Implement
or extend missing independently useful operations as documented general tools in that
owner, with their own contracts and tests, and have consumers call them. Keep feature
selection, interpretation, rendering and orchestration in the consumer; implementation
helpers remain private behind supported tools.

Apply the [modular reusable tools policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/modular_reusable_tools.md)
to every registered component, including support libraries, scientific components,
developer tools and specialist subsystems. Every root `AGENTS.md` must explicitly route
this requirement through this section. New Python members receive it from the starter
kit. Existing public APIs, scientific definitions, units/index mappings, dependency
direction and special environments retain their owning component contracts.

Report missing sibling capabilities to the provider with linked consumer evidence.
The provider chooses its supported backend and justifies performance changes from
measurements. Apply the existing CI/recovery and release policies. This rule governs
relevant new or changed work; discovered historical duplication receives an owned
migration decision. Scientific defects remain with component development teams.

A temporary duplication or workaround records the affected operation/rule, provider and
consumer issues, rationale, responsible owner, interim impact, review/expiry date and
removal condition. Keep the instruction visible during an implementation exception.
Guide and instruction checks verify delivery/routing only. Architectural review must
inspect the standalone tool contract and actual consumer call, distinguishing source
inspection from executed compatibility evidence. Adoption is tracked in
[MolSysSuite #61](https://github.com/uibcdf/molsyssuite/issues/61).

## Optional engines and external methods

Whenever a component exposes an optional external library, executable, accelerator,
service or saved-result adapter, apply the
[optional engine integration contract](https://github.com/uibcdf/molsyssuite/blob/main/devguide/optional_engine_integration.md).
This applies to new integrations and changes to existing boundaries. Record
non-applicability when no such boundary exists; do not add unused dependencies.

Distinguish the selected method/provider from its access route: Python library,
CLI, service, files or local implementation. Keep existing public APIs and justified
environments while recording their adoption. Guard only the selected route, import
optional Python engines lazily, declare actual installer routes and disabled routes,
and keep saved-result and local routes independent of the original engine. An absent
requested engine must not silently choose another method. An intentional automatic
selection must expose its rule and actual choice.

For Python boundaries, use DepDigest for availability/dependency declarations and
SMonitor for diagnostic events, following their canonical guides. The consumer owns
execution, service configuration, conversions and scientific validation. Preserve
transitive import, command, service and parser failures separately from absence.
When accepting a custom executable, check and execute that same command/path.
Verify the published provider version before requiring a new capability publicly;
a controlled source pin is integration evidence, not a public installation route.

Keep method/backend identity, submitted input mappings, original output provenance,
measurement definitions/units and transformations explicit at consumer result
boundaries. Result schemas and scientific tolerances remain component-owned.
Availability, installed-adapter verification, live service checks and receiving-member
compatibility are separate evidence. Ordinary justified absence skips do not replace
a designated installed-engine gate, which must reject missing, shadowed or unexecuted
engines. Follow the existing CI lane/recovery policy and local verification schedule.

Link the member ecosystem review and complete the starter's
`devguide/optional_engine_review.md` worksheet or a documented local equivalent.
Any exception records the affected route/rule, reason, owning member/provider issues,
interim behavior/evidence, responsible maintainer, removal condition and dated review
deadline. Source implementation, synchronized guidance, provider publication and
runtime adoption are independent states. Shared rollout is tracked in
[MolSysSuite #62](https://github.com/uibcdf/molsyssuite/issues/62).

## Public release versions

MolSysSuite defines member release identity in its [release-version policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/release_version_policy.md), enforces it, and maintains the historical-tag inventory and separate `policy-vX.Y.Z` governance-release namespace.

## Conda staging and publication

When preparing or changing Conda publication, apply the
[shared publication contract](https://github.com/uibcdf/molsyssuite/blob/main/devguide/conda_publication_policy.md).
Classify native ABI3, noarch Python or metapackage artifacts; retain the
component's actual platform/Python matrix, recipe, installed-resource/launcher
checks, secrets and scientific gates. A member without Conda publication records
non-applicability.

For qualifying new or changed Conda routes, apply `noarch: python` when Python
code and resources are independent of OS/architecture/ABI. Third-party native
dependencies alone do not disqualify the consumer; bundled extensions/platform
binaries or selectors changing payload require a different profile. Use the
[shared noarch workflow](https://github.com/uibcdf/molsyssuite/blob/main/devguide/noarch_conda_workflow.md),
a reviewed tested equivalent or a bounded policy exception. Build one file once,
inspect versions/resources before upload, and preserve the claimed installed
matrix. The first migration requires staging and installed qualification. Pinned
wrappers reuse common build/upload and exact-file promotion; components own their
scientific installed gates. A green probe with skipped tests cannot authorize
publication. These controls add no suite to ordinary internal pushes.

Commit a reviewed route decision before tagging. Stage candidates that require
pre-public installed/pair validation, add unvalidated compatibility, are coupled
or already have files registered under any label. Eligible ordinary direct
releases keep automatic publication, after exact-source native gates and a fresh
conclusive all-label absence check. Manual builds are staging-only; public builds
never use `--no-test` or overwrite immutable coordinates. A bootstrap exception
identifies the cycle, exact candidate, counterpart gate, owner and expiry.

Promote the exact validated files by SHA-256 with retained receipts; use additive
build repairs and the reviewed dependency-first order. Verify public main labels
and solver-index records independently with the pinned common Conda verifier.
After a verifier/index failure, rerun that read-only boundary without repeating
promotion. Its file/inventory evidence, producer receipts and installed-pair
tests remain separate claims. Adopt the lightweight publication guard or a
documented tested equivalent before affected release work; it adds no general
scientific suite to internal development pushes. Scope, versioned templates,
commands, existing-profile adoption and dated exceptions are in the policy and
its [rollout inventory](https://github.com/uibcdf/molsyssuite/blob/main/devguide/rollouts/conda_publication.md).

## Repository badges

MolSysSuite owns member badge evidence, its role taxonomy and generated suite identity baseline. Every member README carries the centrally generated MolSysSuite identity baseline in
this order: role, live policy workflow, supported Python versions when applicable, and
license. Generate or verify that row from the MolSysSuite checkout with
`devtools/scripts/repository_badges.py`; do not copy another component's Markdown.

Tests, coverage, documentation, releases, DOI records and package channels are
conditional evidence badges. Include one only while its own authoritative surface is
maintained and belongs to that repository. A failing live workflow badge is truthful
and must not be hidden; a static green replacement is not. Omit stale or unverifiable
capabilities and track concrete remediation in the component repository. The common
repository policy gate enforces the offline identity baseline; service freshness still
requires a separate networked audit under `devguide/repository_badges.md`.

When meaningful coverage reporting is maintained, the README displays Codecov's
live repository-specific percentage between tests and documentation. Explain
report scope and cadence: the last uploaded report may lag later direct/skip
commits and does not certify a full matrix or scientific correctness. Review the
complete report and actual upload, not only a numeric cached badge. Missing or
stale evidence needs an owner-local issue; justified non-applicability and bounded
exceptions remain visible in the central inventory, including auxiliary tools.
Use the common badge generator and public coverage probe in MolSysSuite. This
rule adds no full suite to internal pushes and no common coverage floor. Follow
the [coverage evidence contract](https://github.com/uibcdf/molsyssuite/blob/main/devguide/repository_badges.md#coverage-percentage-applicability-and-cadence).

## Quantities crossing boundaries

Follow the [quantity boundary contract](https://github.com/uibcdf/molsyssuite/blob/main/devguide/quantity_boundaries.md)
for new or changed persistence, backend, message and frontend routes. PyUnitWizard
owns interchange design (`uibcdf/pyunitwizard#83`) and implementation (#82);
members own scientific schemas and migration. Use its shared record/codec route
for general quantity interchange. Fixed-unit numerical protocols extract with
explicit `to_unit=` matching the receiver's declared contract; do not strip a
standardized quantity and assume its unit.

Applicable boundaries need a real regression under a non-default application
policy, with explicit output classification and reader unit validation. Provider
API promotion and published compatibility remain separate from source pilots.
Existing schema/provider limitations need reviewed member exceptions with interim
unit-preserving controls, owner, expiry and removal condition. These focused
compatibility checks do not require full scientific suites at every internal push.
Complete adoption remains tracked in `uibcdf/molsyssuite#46` and #18.

## macOS support boundary

macOS support is currently limited to Apple Silicon (arm64). Intel-based macOS
(x86_64) is not part of the supported platform matrix. Support may be
reconsidered if there is demonstrated user demand. Apply this boundary to current
support statements, future CI/release targets and installed-package gates.
Historical artifacts and dated evidence retain their original identity.

An eligible architecture is not proof of member compatibility: a component must
provide its own installed/runtime evidence before claiming macOS arm64 support.
Incubating members may make no platform claim. See the
[CI policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_ci_policy.md#platforms-and-experimental-versions)
and [member rollout](https://github.com/uibcdf/molsyssuite/blob/main/devguide/rollouts/macos_arm64.md).
Reconsideration requires a concrete user need in a MolSysSuite issue and an
explicit support decision with component evidence and ownership.

## Optional scientific attribution

For new or changed optional scientific attribution boundaries, follow the
[Ackredit client policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/ackredit_client_policy.md)
and the synchronized `ACKREDIT_GUIDE.md` where present. Defer provider imports and
registration until use, credit the executed branch, contribute to the application's
session and keep detached bibliography and original versions in results. Provider
absence or diagnosed failure preserves completed scientific results. Libraries
must not automatically enable hooks, enrichment, journals or reminders.

Evidence must observe a real provider, reused references, enclosing workflows,
absence/failure and fresh readers; pilot evidence does not certify published
dependency closure. Ackredit owns portable attribution APIs; members own their
scientific schemas and runtime adoption. Utilities without attribution boundaries
record non-applicability. Different initialization/session semantics require a
reviewed member exception with its rule, reason, owner, interim controls, expiry
and removal condition. Guide distribution alone does not establish adoption.

## GitHub Actions inspection

Follow the [MolSysSuite developer-tools policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_ecosystem_policy.md)
and the repository's `GH_RUN_RECEPTOR_GUIDE.md` where present. The suite's
[dogfooding profile](https://github.com/uibcdf/molsyssuite/blob/main/devguide/gh_run_receptor_policy.md)
tracks readiness and actual operator use, provider feedback, and any bounded
member exception. Guide presence alone does not establish active adoption.

## Release archival and DOI claims

MolSysSuite owns member DOI/archival rules, applicability, evidence inventory,
rollout and exceptions; each component still owns its metadata, release gates,
artifacts and release
decision. A successful GitHub Release, metadata file, reported account toggle or observed
webhook is not proof of archival. Only an independently verified public Zenodo record and
exact file inventory permit an archival claim.

Use the concept DOI for stable project badges and general citation, and a version DOI for
an exact release. When both `CITATION.cff` and `.zenodo.json` exist, validate their shared
metadata; Zenodo gives `.zenodo.json` precedence during GitHub archiving. Never print or
retain credential-bearing webhook configuration. Follow the complete
[Zenodo archival and DOI policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/zenodo_policy.md)
and its central inventory before publishing or changing a DOI claim.

Use bounded probes with scheduled/manual follow-up for delayed ingestion. The
default intervention window is 72 hours from original publication; pending and
service-unavailable states never establish archival. Adopt the common pinned
recovery workflow or a documented equivalent before the next applicable release;
the policy specifies complete discovery, evidence and tracked exceptions.

## Member classification and planning

MolSysSuite records independent fields for each member: `role` says what it provides,
`membership` says whether it is primary or auxiliary, `maturity` records the strength of
its public contracts, `development-mode` distinguishes active from maintenance-focused
work, and `capabilities` activate concrete technical policies. These fields must not be
collapsed into a single cohort. Both primary and auxiliary repositories are fully
governed suite members.

The active stabilization initiative currently prioritizes SMonitor, ArgDigest,
DepDigest, PyUnitWizard, MolSysMT and MolSysViewer. TopoMT, PharmacophoreMT, ElastNetMT,
DockingMT and the support library Ackredit are incubating. Lindelint is an auxiliary
developer tool created for ElastNetMT and the wider suite. Priority affects scheduling,
not governance or whether contributors communicate valuable discoveries from any
component. Consult the central `devguide/member_classification.md` and `suite.toml` for
the complete vocabulary and current assignments.

## Before finishing component work

Check whether the change:

1. exposes a provider limitation that needs a cross-component issue;
2. changes a shared contract and therefore needs a central issue;
3. requires updating a local report, generated index, archived record, or issue state;
4. affects the common Python/tooling baseline or needs a documented exception;
5. should propose an improvement to this guide or another central policy.

Run the component's own tests and local gates. The MolSysSuite conformance workflow
checks the common baseline; it does not replace component-specific validation.
