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

Use [the MolSysSuite repository](https://github.com/uibcdf/molsyssuite) for policies,
compatibility contracts, common tooling, cross-component proposals, coordinated
rollouts, and decisions affecting two or more members. Its `suite.toml` is the
machine-readable registry of members, classification fields, initiatives, and accepted
policies. Its `devguide/` contains the full normative texts and decision history.

The component repository remains authoritative for its implementation, tests, product
API, scientific evidence, releases, and local development tools. Local rules may be
stricter, but they must not silently contradict a common policy. A deviation needs a
tracked exception with its reason and expiration condition.

The wider platform architecture belongs to
[MOLI Architecture 1.0](https://github.com/uibcdf/moli/blob/main/architecture_1.0/README.md),
not to the MolSysSuite registry or developer guide. MOLI describes MolSysSuite as
the molecular modeling ecosystem alongside Scientific Context and optional
MOLI Agent reasoning.

Start with these central documents:

- [repository ownership contract](https://github.com/uibcdf/molsyssuite/blob/main/devguide/repository_contract.md);
- [issue and developer-guide reporting protocol](https://github.com/uibcdf/molsyssuite/blob/main/devguide/reporting_protocol.md);
- [cross-component feedback policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/cross_component_feedback.md);
- [Python support policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_policy.md);
- [Python tooling policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_tooling_policy.md);
- [component release-version policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/release_version_policy.md);
- [GH Run Receptor dogfooding policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/gh_run_receptor_policy.md).

MOLI's conceptual architecture does not admit repositories to MolSysSuite.
`suite.toml` alone records governed members; its `role`, `membership`,
`maturity`, `development-mode`, and `capabilities` fields classify real
repositories rather than platform concepts.

Consult the central repository before changing a shared dependency boundary, supported
Python range, development baseline, issue vocabulary, reusable workflow, vendored guide,
or behavior expected across components.

Canonical-guide publication and versioned policy adoption are independent. A guide-only
change does not require a policy caller bump, and a caller bump does not prove that guide
copies were synchronized. Use the central `devtools/scripts/adoption_status.py` inventory
and `devguide/adoption_lifecycle.md` procedure to find the responsible consumer, observed
state and next action for each relationship.

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

## Common development baseline

Python libraries use the default Python `>=3.11,<3.14` contract; routine development uses
Python 3.13 and CI covers 3.11, 3.12, and 3.13. During an accepted minor-version
transition, `suite.toml` may authorize named components to adopt a wider target after
component-specific evidence. Only components marked `admitted` may claim that wider
support; all others retain the default. Ruff is the common formatter and linter, replacing Black,
isort, and Flake8. The required shared lint core is `E4`, `E7`, `E9`, `F`, and `I`;
repositories may add stricter rules. Pytest is the common test runner. Type checking and
domain-specific scientific or UI gates remain repository-local.

Every root integration guide synchronized from another repository is generated,
read-only content. List its exact path in Ruff's `extend-exclude`; do not reformat or edit
it in a component. Propose changes at the canonical source and resynchronize the exact
copy. The suite checks both the exclusion and byte-level drift.

## Public release versions

Every component release uses exactly `X.Y.Z`: three canonical non-negative integer
components. The package or project version, Git tag and GitHub Release tag are the same
string. Do not prefix the tag with `v` and do not publish `a`, `b`, `rc`, `.dev`, `.post`
or `+local` suffixes. Candidate testing belongs in staging rather than a public
prerelease.

Development checkouts may carry truthful derived identities such as
`1.2.3+4.gabc1234` or a `.dirty` suffix; those are development provenance, not public
release versions. MolSysSuite policy tags (`policy-vX.Y.Z`), third-party Action refs,
schema versions and Conda build numbers are separate namespaces. Follow the central
release-version policy for the exact pattern, historical-tag treatment and exception
process.

## Repository badges

Every member README carries the centrally generated MolSysSuite identity baseline in
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

## GitHub Actions inspection

Use GH Run Receptor as the preferred first inspection path during development, following
the repository's `GH_RUN_RECEPTOR_GUIDE.md` where present. Use the latest published
release for routine work; an unreleased capability is experimental and must be pinned to
an exact reviewed commit, never a floating branch.

GitHub conclusions remain authoritative. Fall back to native `gh run view` inspection
when the receptor reports incomplete evidence, errors, omits a fact needed for the
decision, or disagrees with GitHub. During controlled adoption, the receptor is not the
only approval source for releases, publication, deployment, or other irreversible work.
Report limitations to `uibcdf/gh-run-receptor` with the workflow, run ID, selected profile,
expected and observed results, and only sanitized evidence. The complete contract and
exception process live in the central dogfooding policy linked above.

## Release archival and DOI claims

MolSysSuite centrally governs Zenodo applicability, DOI meaning, evidence states and
exceptions; each component still owns its metadata, release gates, artifacts and release
decision. A successful GitHub Release, metadata file, reported account toggle or observed
webhook is not proof of archival. Only an independently verified public Zenodo record and
exact file inventory permit an archival claim.

Use the concept DOI for stable project badges and general citation, and a version DOI for
an exact release. When both `CITATION.cff` and `.zenodo.json` exist, validate their shared
metadata; Zenodo gives `.zenodo.json` precedence during GitHub archiving. Never print or
retain credential-bearing webhook configuration. Follow the complete
[Zenodo archival and DOI policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/zenodo_policy.md)
and its central inventory before publishing or changing a DOI claim.

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
