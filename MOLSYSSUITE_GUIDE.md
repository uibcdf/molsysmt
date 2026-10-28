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

## Mandatory common instructions and local scope

Read and follow this guide before working in any registered component, including
auxiliary, incubating and subsystem repositories. Its applicable common rules
and the authoritative policies linked below take precedence over root and nested
`AGENTS.md` files. Local instructions refine product/scientific behavior, source
layouts, commands and directory conventions; they do not silently waive or
reverse a common rule. A conflicting deviation uses that policy's documented
exception, owner, reason, interim controls, review/expiry and removal condition.
Stricter local scientific/release gates remain local obligations, not new suite
requirements. A directory-specific instruction can refine another local rule
while preserving this common layer. Explicit human/session authorization and
higher-priority instructions retain their authority.

Every root `AGENTS.md` carries the mandatory read/follow and scoped-precedence
entry defined by the [instruction policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/working_instructions_policy.md).
Keep its remaining instructions specific to that repository. Common rules live
here and in their normative owners; root/nested files need not repeat them.
Use the official versioned starter for new members and review conflicts before
receiving an existing repository. Copying files, a green structural checker or
membership alone does not establish semantic compliance or scientific readiness.

Maintain repository code, documentation and commits in English. Human discussion
may follow the collaborator's preferred language. Preserve human work and declared
scientific scope, keep changes focused and never publish credentials, private
attachments or unrestricted evidence. Existing explicit authorization for the
same work persists across commits; this guide does not add a permission round.

## Find the rules for the current task

Use this map after reading the common instructions. Follow each linked rule's
applicability and the component's actual adoption/evidence state.

| When | Required action and owning guidance |
| --- | --- |
| Starting work or coordinating clones | Read local instructions; verify the [development workspace](#local-development-workspace) and inspect [cross-repository state](#cross-repository-working-state) when applicable. |
| Adding or changing a capability | Consult the [responsibility map](#component-responsibility-map), reuse supported [tools/contracts](#modular-reusable-tools), and review [support-library](#applicable-support-libraries-and-developer-tools), [quantity](#physical-quantities-and-units) and [optional-engine](#optional-engines-and-external-methods) boundaries. |
| Changing dependencies or acquisition routes | Align manifests/environments/recipes and update the [dependency inventory and CI route](#dependencies-and-ci-acquisition). |
| Finding a defect or improvement | Follow [issue feedback](#human-facing-issue-feedback); hand provider limitations to their [owning component](#shared-stewardship-across-components), with consumer evidence. |
| Changing shared guidance, APIs or tooling | Give the [consumer-impact notice](#shared-stewardship-across-components); publish canonical sources and use the registered [guide-adoption route](#guide-revisions-and-distribution). |
| Preparing a commit or push | Select relevant [quality checks](#common-development-baseline) and follow the authorized [CI checkpoint route](#direct-pushes-and-validation-checkpoints). |
| Preparing a release or package | Verify exact-candidate [version](#public-release-versions), [platform](#supported-platforms), [publication](#conda-staging-and-publication) and applicable [archival](#release-archival-and-doi-claims) gates; deliver the [release notice](#release-and-package-publication-notices). |
| Closing work | Follow [closeout](#before-finishing-component-work), update owning records and review [temporary resources](#temporary-development-resources). |

An applicable rule with pending adoption remains owned work. Non-applicability
names the absent boundary and its reassessment condition. A deviation needs the
owning policy's bounded exception; neither early development nor an exception
turns an unexecuted gate into passing evidence. Python-only and release-specific
rules activate only within their stated scope.

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

The current central member-policy release is recorded in `suite.toml`. Each
member's effective automated policy is the
release pinned by its workflow; older compatible releases remain visible in
the adoption inventory. The MOLI commit recorded in `suite.toml` identifies
platform-contract context for the suite; it is not a source of member
engineering values.

For a new member absent from its frozen policy registry, the [official starter admission route](https://github.com/uibcdf/molsyssuite/blob/main/devguide/new_component_starter_kit.md#immutable-policy-and-separate-admission) supports a separate full central admission commit from `policy-v1.5.5`. It adds registration and classification only; engineering rules and exceptions remain those of the selected policy.

The wider platform architecture belongs to [MOLI Architecture 1.0](https://github.com/uibcdf/moli/blob/main/architecture_1.0/README.md). MOLI describes MolSysSuite as
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

### Guide revisions and distribution

The guide's exact revision is its canonical Git commit and content SHA-256;
delivery records retain the consumer commits and applicable executed checks.
Its links to `blob/main` are live maintained documents. Recovering an old guide
commit reproduces those guide bytes, not a frozen snapshot of every linked
policy. Use recorded exact document/input revisions for historical decisions
and candidate evidence. A compatible older automated caller retains its frozen
behavior without waiving current normative obligations or certifying adoption.

Edit and publish the canonical source in its owner first. From the MolSysSuite
clone, distribute registered copies with `sync_vendored_guides.py`, then publish
the reviewed consumer commits and verify their live adoption. The synchronizer
requires published, committed canonical input and protects modified consumer
copies. Report a bounded inability to adopt through the owning policy's
exception mechanism. Follow the [vendored-guide policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/vendored_guides.md)
and [adoption lifecycle](https://github.com/uibcdf/molsyssuite/blob/main/devguide/adoption_lifecycle.md);
keep advance notice, delivered bytes and tested runtime/public artifacts separate.

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
bounded exceptions and member adoption are recorded by the policy. The accepted
human-facing action below and the remaining pilots are tracked separately in
uibcdf/molsyssuite#65.

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

### Human-facing issue feedback

During development, tests, scientific exploration and conversations, surface
actionable suspected defects, inconsistencies, missing analyses and improvements,
even when uncertain or nonblocking. State what was observed and what remains
uncertain; identify the owning repository and check for an existing issue.
When working with a human, explicitly offer to open or update that issue at a
natural pause. File or update under the applicable authorization; existing
authorization for the same work does not require another permission request.
Respect a declined or deferred report, retain only an authorized sanitized
disposition, and do not publish the human's confidential material without authority.
The reporting commitment creates a durable feedback route; it does not override
disclosure authority or promise immediate implementation. Use private reporting
first for exploitable or confidential findings.

This contributor action applies to every registered member, including early
development components, under uibcdf/molsyssuite#65. Follow the existing reporting,
cross-component feedback and durable-instruction routes. Bounded instruction
exceptions use the working-instruction policy's registered owner, rationale,
removal condition and expiry. Scientist-facing pilots, opt-in notifications and
automatic retries remain pending; this instruction does not implement them.

### Reporting ownership and records

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

## Release and package-publication notices

For every new component release, including a source/tag-only release without a
published package, and every new package version/build/distribution route, open
or update a release-specific issue in `uibcdf/molsyssuite` as part of closeout.
MolI components outside suite membership report to `uibcdf/moli` through its
separately owned rule. Include exact version/tag/source/release identity, the
actual package channels/files/digests and verification evidence or explicit
unpublished/pending state, and ecosystem pins/packages/consumer follow-up owners.
Update the same component/version notice when packages arrive later.

Follow the [release-notice policy and template](https://github.com/uibcdf/molsyssuite/blob/main/devguide/release_notifications.md).
The notice is required even without known consumer impact; it supplements the
separate advance shared-provider impact notice. Reporting does not authorize
automatic consumer updates, immutable tag/file replacement or a scientific run,
and is not a new central pre-release permission gate. Retain an owned bounded
exception or private/sanitized handoff when required by that policy.

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
obligations. Both receptors are primary suite members with the developer-tool
role; role and membership are independent registry fields.

## Applicable support libraries and developer tools

At each new or changed boundary, review and use the registered provider where
applicable: ArgDigest for nontrivial public argument constraints/normalization,
DepDigest for optional/heavy/backend availability, SMonitor for user-visible
structured diagnostics and PyUnitWizard for physical quantity conversion and
dimensional/interchange contracts. Optional scientific attribution uses the
Ackredit client contract. Do not add an unused dependency to satisfy a checklist;
record non-applicability and reassess when the boundary appears. Preserve justified
provider bootstraps, dependency direction and documented exceptions.

Use a published Pytest Receptor with `--receptor=llm` for local agent pytest and
`--receptor=ci` for hosted output; pin the exact reviewed CI version. Preserve
native test selection, assertions, exit status and mandatory suite. Use a published
GH Run Receptor for first Actions inspection, then authoritative native GitHub
run/job/step facts for missing evidence and exact-candidate acceptance. Record a
reviewed source pin honestly for an unreleased experiment. Receptors do not gain
publication/mutation authority. Missing tools or unsupported environments require
a visible bounded exception and the native fallback, not a hidden skipped gate.
Read the registered canonical integration guides for actual consumer boundaries;
these tools are not runtime dependencies merely because a repository develops Python.

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

Unit-policy authority is explicit operation parameter, local context, application
policy, then factory default. Importing or lazily activating a sibling must not
overwrite an application choice. A member needing the shared suite baseline
initializes it only when `has_active_policy()` is false. The accepted provider
context mechanism serializes writers in one process; it is not thread/async-local
isolation. Follow the [session-authority contract](https://github.com/uibcdf/molsyssuite/blob/main/devguide/quantity_boundaries.md#session-authority)
and the boundary/adoption route below.

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

For applicable Python changes, run `ruff check .` and `ruff format --check .`
with the shared lint/format baseline. Keep Ruff's target `py311` for the oldest
supported syntax even though routine development uses Python 3.14. The called
policy supplies the exact reviewed CI tool version; local development may use
that version or a compatible newer version producing the same required result.
Preserve additional local rules. Replace legacy format/lint gates only after
the equivalent Ruff migration checks pass, as specified by the tooling policy.

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

### Direct pushes and validation checkpoints

For explicitly authorized internal work by Diego (`dprada`), Liliana (`LMMV`) or
an agent working directly under their supervision, the granted commit/direct-push
route remains available within that scope. Do not ask again for each commit when
that authorization already exists. Other contributors use owner-reviewed PRs
with the full required suite before integration; an internal maintainer choosing
a PR follows the same PR gates. Cross-owner fixes retain their separate
contribution route above; shared team membership alone grants no write authority.

For those authorized internal direct pushes, keep focused commits local and batch pushes when collaboration, backup or current CI evidence
does not need a checkpoint. A permitted interim skip is conditional, never the
default after every locally checked change. Select local checks by affected
code, inputs and scope; reuse completed results only while they remain applicable.
Documentation and evidence need their relevant governance checks, scientific
hypotheses their informative cases, and executable or integration changes their
relevant code/contract checks. Reconcile contradictory local instructions in
the owning repository before claiming adoption.

Normally finish with an unskipped head and inspect its applicable CI, or use
an explicitly authorized manual execution and verification of those exact-head
gates. Record missing evidence, untested scope, owning issue and recovery route.
Administrative checks and smoke runs do not clear full-suite backlog. Preserve
daily recovery, weekly full matrices and tracked scientific deferrals.

External PRs and admission/release/publication keep all mandatory executed gates.
A producer commit carrying a skip marker can qualify through the authorized
manual route only with every required gate verified for the exact candidate,
installed bytes and dependency closure. Keep its original producer identity and
artifact digest; a workflow correction does not authorize rebuilding the file.
Follow the [CI checkpoint policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_ci_policy.md#direct-push-decisions-and-validation-checkpoints)
for applicability, result-reuse limits and bounded owner-linked exceptions.
This adds no complete suite before each internal push.

### Local development workspace

For routine Linux development use the qualified `molsyssuite@uibcdf_3.14`
Conda environment created from the suite's
[canonical recipe](https://github.com/uibcdf/molsyssuite/blob/main/devtools/conda-envs/molsyssuite-dev-py314.yaml).
Install every participating eligible local clone with `python -m pip install
--no-deps --editable PATH`; Conda supplies its dependencies. Where native builds
need the declared in-environment tools, add `--no-build-isolation`. Verify Python
3.14, `python -m pip check` and actual editable import origins, then run the
selected tests with `python -m pytest --receptor=llm` in that environment.
Ordinary Python source edits are visible without reinstalling; changes to
metadata, entry points or compiled extensions can require reinstalling/rebuilding.

Eligibility comes from the registered development profile; the automated
installer selects the complete current cohort. The current
cohort, exclusions and measured source snapshots come from that profile and the
linked development-workspace receipts; no fixed member count in this guide
substitutes for them. A member not yet qualified uses its own compatible Python 3.14 Conda
development environment and tracks the shared-environment gap and exit condition
in its owning issue. An older interpreter requires the existing bounded migration
exception. MolSys-AI's umbrella is not an installable Python package; a MOLI
component such as Sabueso retains its own membership and qualification owner.

Use the [development workspace contract](https://github.com/uibcdf/molsyssuite/blob/main/devguide/development_workspace.md)
and registered profile/receipts for current eligibility, bootstrap, exclusions and
cross-domain work. An editable installation or development probe does not qualify
a public artifact, full scientific suite, GUI rendering or another platform.

Every root integration guide synchronized from another repository is generated, read-only content. List its exact path in Ruff `extend-exclude`; propose changes at the canonical source and resynchronize the exact copy. The suite checks the exclusion and byte-level drift.

### Dependencies and CI acquisition

When changing a dependency, Python bound or runtime-bearing route, align the
required names and constraints in `pyproject.toml`, maintained environments and
Conda recipe. Keep optional features optional and record intentional Python/Conda
name translations. Review provider API floors and actual installed versions;
solver success alone does not prove the required capability exists. Run the
applicable dependency-route preflight before an expensive candidate build and
for the exact release candidate, under the [distribution contract](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_distribution_policy.md#early-dependency-contract-preflight).

Required siblings need a working CI acquisition route on every claimed lane.
Use a committed resolvable Conda environment, or a reviewed source installation
pinned to a full commit where permitted. Suite packages are not assumed to be
on PyPI. Floating branches and local editable siblings do not establish release
evidence; a source pin supports tests without proving public availability.
Follow [CI dependency resolution](https://github.com/uibcdf/molsyssuite/blob/main/devguide/ci_dependency_resolution.md).

After affected direct dependency or development-profile changes, coordinate the
registry graph update with immutable inspected source evidence and regenerate
its human view through central `dependency_graph.py`. Keep runtime, optional,
test, CI and documentation edges distinct. Use its provider/consumer queries to
plan impact and prerequisite order; a cycle is a coordinated unit, not an
arbitrary release order. The [dependency graph policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/dependency_graph_policy.md)
owns these records; inspected edges do not certify installed compatibility.

## Modular reusable tools

Before implementing a new or changed capability, inspect existing tools and identify
the owning domain/module or MolSysSuite provider. Reuse supported operations. Implement
or extend missing independently useful operations as documented general tools in that
owner, with their own contracts and tests, and have consumers call them. Keep feature
selection, interpretation, rendering and orchestration in the consumer; implementation
helpers remain private behind supported tools.

Document reusable inputs/outputs, units, selection/frame and index mappings,
configuration authority, empty/degenerate cases and failure behavior. Preserve
supported signatures, diagnostics and justified environments; an intentional
scientific-definition or schema change needs its owner's compatibility/migration
decision, with a shared contract change registered centrally before requiring
it from other components.

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

## Component responsibility map

Before implementing a capability, inspect the registered owner's supported APIs
and the [suite roster](https://github.com/uibcdf/molsyssuite#registered-molsyssuite-components).
Reuse or propose independently useful tools in that owner. Keep consumer-specific
scientific requirements, selection, interpretation and orchestration in the
consumer. Report a missing capability with its reproduction/use case and impact
in the owning issue; cross-link the consumer and any workaround. A linked PR or
an explicitly authorized principal-supervised contribution can propose the fix;
the provider owns its contracts, priority and acceptance. Do not silently copy
an implementation because its owner is incubating or the needed API is absent.

| Capability | Owning component |
| --- | --- |
| Molecular-system representation, manipulation, general analysis, selection and format interoperability | MolSysMT |
| Molecular visualization, rendering and interaction | MolSysViewer; specialized scientific add-ons retain their own owners |
| Cavities, pockets and molecular surface topography | TopoMT; OpenCASTp owns its independent CASTp numerical kernel |
| Pharmacophore modeling | PharmacophoreMT |
| Elastic-network definitions and analysis | ElastNetMT |
| Molecular docking workflows | DockingMT |
| Peptide-specific design and functional evaluation | PeptideMT |
| Interpolation support | LinDelINT |
| Scientific/AI subsystem understanding and operation of the suite | MolSys-AI, preserving its subsystem/platform boundary |
| Public argument constraints and normalization | ArgDigest |
| Optional dependency availability/loading | DepDigest |
| Structured diagnostics | SMonitor |
| Physical quantities, conversion and interchange | PyUnitWizard |
| Optional scientific attribution | Ackredit |
| Pytest reports and Actions-run inspection | Pytest Receptor and GH Run Receptor, respectively |

This map routes ownership, not a promise that an API is implemented or stable.
Review current registration, actual contracts and evidence before depending on a
capability. It does not require eager dependencies, force all numerical work into
one library or authorize a scientific implementation. Other direct MOLI components
keep their own contracts; propose cross-platform boundaries through MOLI.

## Temporary development resources

Use temporary locations such as `/tmp` when appropriate. Keep task ownership
clear, retain resources and evidence while needed, and remove them when their
usefulness ends. Evidence may stay in `/tmp`; relocation is not required.
Review retained resources at task/release closeout. Prefer managed temporary
directories that clean after success and failure. Preserve active/human work,
shared environments and required evidence; report cleanup failures.
Follow the [temporary-resource policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/temporary_resources.md)
for applicable tools, owner-controlled cleanup and tracked implementation
exceptions. Member adoption and historical cleanup are tracked in
[MolSysSuite #104](https://github.com/uibcdf/molsyssuite/issues/104).

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

### GitHub Release titles

When preparing, publishing or intentionally editing a public component release,
set its GitHub Release title/name to exactly `X.Y.Z`, equal to its canonical tag
and project/package version. Use `0.14.0`, without a project name, `v` prefix,
subtitle or comment. Put descriptions in the body/notes. Check the separate
title field: use `--title X.Y.Z` with GitHub CLI, or `name == tag_name == X.Y.Z`
with the API, including when generating notes. This applies to every registered
member; existing governance policy-release and archive namespaces retain their
separate meanings. Follow the release policy's documented exception route.
Accepted under [MolSysSuite #119](https://github.com/uibcdf/molsyssuite/issues/119),
with direct MOLI-component adoption in
[MOLI #68](https://github.com/uibcdf/moli/issues/68).

### Archive tags

Use `archive/<description>` to retain an experiment or another historical commit
without presenting it as a public release. Record the preserved commit, purpose
and owner in the tag annotation or an owning issue. Keep the tag stable. An
archive tag is never a package version, GitHub Release, public-release receipt
or publication authorization. Public versions and release tags remain exact
`X.Y.Z`; publishers must reject other identities before any registry write.
Keep an unconditional conformance caller on all tag pushes, normally with
`tags: ["**"]` so names containing `/` are included. A Python member using archive
tags adopts `policy-v1.5.7` or a compatible newer caller first; other members may
retain their compatible callers. Preserve exact-candidate gates and immutable
public artifacts. Exceptions use the release policy's owning issue, reason and
expiry mechanism. This capability is accepted under
[MolSysSuite #84](https://github.com/uibcdf/molsyssuite/issues/84).

## Conda staging and publication

When preparing or changing Conda publication, apply the
[shared publication contract](https://github.com/uibcdf/molsyssuite/blob/main/devguide/conda_publication_policy.md).
Classify native ABI3, noarch Python or metapackage artifacts; retain the
component's actual platform/Python matrix, recipe, installed-resource/launcher
checks, secrets and scientific gates. A member without Conda publication records
non-applicability.

The official public route is the `uibcdf` Conda channel, with third-party
dependencies from `conda-forge`. PyPI is optional and may be advertised only
after the published artifacts and full declared dependency closure install on
the claimed platforms/minors. A GitHub Release or local pip install proves
neither channel availability nor installed compatibility.

Request selected-repository access to `ANACONDA_UIBCDF_TOKEN` from Diego
(`dprada`) through the owning distribution/release issue, linking central #45
and `uibcdf/moli#8`. Identify the package, release maintainer and trusted
publisher/events/environments. Record the administrator's disposition and
presence-only readiness in the actual trusted workflow; never retain the
credential value. PR/fork tests receive no upload credential, and there is no
personal-token fallback. The shared workflow retains its explicit
`ANACONDA_TOKEN` input mapping. Follow the [credential-access contract](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_distribution_policy.md#conda-publication-credential-access);
an access grant alone does not authorize a release or prove delivery.

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

For a noarch Python recipe, `build.entry_points` must match
`[project.scripts]` exactly, including command names and callable targets.
Exercise every command's `--help` from the installed Conda artifact on every
claimed platform, including Windows when claimed. A passing Linux build or
corrected source recipe does not repair or qualify an existing public file.
Follow the [launcher contract](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_distribution_policy.md#console-commands-in-noarch-conda-recipes)
and retain resource/archive checks separately for each distribution route.

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

## Supported platforms

Linux and macOS arm64 are the suite support target for public Python packages;
Windows is optional. A component claims support only with its own evidence.
Keep required Linux lanes; an incubating member may make no public OS claim.
For macOS arm64, and Windows if claimed, execute required tests at least weekly
on the routine Python minor. Before a release claim, test the exact installed
candidate and dependency closure on every claimed OS and supported Python minor,
including representative behavior, resources and entry points. Bounded
exceptions retain their actual limitations and never certify an untested platform.

### macOS support boundary

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
artifacts and release decision. Archival is required for primary members with
stabilizing/stable maturity. Auxiliary or incubating members use the registered
optional mode and explicitly review applicability when preparing a public
release; electing archival activates its verification/recovery obligations.
A successful GitHub Release, metadata file, reported account toggle or observed
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

Read the active initiatives and current member assignments from `suite.toml`
and the central `devguide/member_classification.md`, rather than inferring them
from a version number or another member's status. Priority affects scheduling,
not governance or the responsibility to communicate valuable discoveries.

## Before finishing component work

Check whether the change:

1. exposes a provider limitation that needs a cross-component issue;
2. changes a shared contract and therefore needs a central issue;
3. requires updating a local report, generated index, archived record, or issue state;
4. affects the common Python/tooling baseline or needs a documented exception;
5. should propose an improvement to this guide or another central policy.

Run the applicable component checks and selected tests for the affected inputs
and scope, following the checkpoint policy. Full PR/admission/release gates keep
their own executed evidence requirements. The MolSysSuite conformance workflow
checks the common baseline; it does not replace component-specific validation.

## Complete common-policy index

Every accepted policy below is mandatory within its stated applicability. Follow
the full normative document, its local adoption/evidence state and exception route,
even when the operational summary above does not repeat every detail. Python-only
rules do not make a non-package subsystem installable; future publication/engine
rules activate when the corresponding work is undertaken. The registered policy
release continues to own frozen automated values.

| Registered policy | Normative owner |
| --- | --- |
| `member-classification` | [devguide/member_classification.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/member_classification.md) |
| `conda-publication` | [devguide/conda_publication_policy.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/conda_publication_policy.md) |
| `quantity-boundaries` | [devguide/quantity_boundaries.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/quantity_boundaries.md) |
| `ackredit-clients` | [devguide/ackredit_client_policy.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/ackredit_client_policy.md) |
| `repository-badges` | [devguide/repository_badges.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/repository_badges.md) |
| `working-instructions` | [devguide/working_instructions_policy.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/working_instructions_policy.md) |
| `release-notices` | [devguide/release_notifications.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/release_notifications.md) |
| `temporary-resources` | [devguide/temporary_resources.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/temporary_resources.md) |
| `component-dependencies` | [devguide/dependency_graph_policy.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/dependency_graph_policy.md) |
| `python` | [devguide/python_policy.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_policy.md) |
| `python-ci` | [devguide/python_ci_policy.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_ci_policy.md) |
| `python-quality` | [devguide/python_tooling_policy.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_tooling_policy.md) |
| `python-support-libraries` | [devguide/python_ecosystem_policy.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_ecosystem_policy.md) |
| `modular-reusable-tools` | [devguide/modular_reusable_tools.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/modular_reusable_tools.md) |
| `optional-engine-integration` | [devguide/optional_engine_integration.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/optional_engine_integration.md) |
| `python-developer-tools` | [devguide/python_ecosystem_policy.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_ecosystem_policy.md) |
| `python-distribution` | [devguide/python_distribution_policy.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_distribution_policy.md) |
| `ci-dependency-resolution` | [devguide/ci_dependency_resolution.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/ci_dependency_resolution.md) |
| `release-version` | [devguide/release_version_policy.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/release_version_policy.md) |
| `reporting-lifecycle` | [devguide/reporting_protocol.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/reporting_protocol.md) |
| `cross-component-feedback` | [devguide/cross_component_feedback.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/cross_component_feedback.md) |
| `cross-component-issue-labels` | [devguide/reporting_protocol.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/reporting_protocol.md) |
| `component-guide` | [MOLSYSSUITE_GUIDE.md](https://github.com/uibcdf/molsyssuite/blob/main/MOLSYSSUITE_GUIDE.md) |
| `component-starter-kit` | [devguide/new_component_starter_kit.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/new_component_starter_kit.md) |
| `vendored-guides` | [devguide/vendored_guides.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/vendored_guides.md) |
| `adoption-lifecycle` | [devguide/adoption_lifecycle.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/adoption_lifecycle.md) |
| `gh-run-receptor-dogfooding` | [devguide/gh_run_receptor_policy.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/gh_run_receptor_policy.md) |
| `zenodo-archival` | [devguide/zenodo_policy.md](https://github.com/uibcdf/molsyssuite/blob/main/devguide/zenodo_policy.md) |
