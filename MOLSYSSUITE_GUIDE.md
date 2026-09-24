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

MolSysSuite is a first-class MOLI component with delegated internal governance. MOLI owns the shared platform engineering baseline; MolSysSuite inherits it and adds modeling-ecosystem policy, rollout/admission machinery, and stricter domain requirements where justified.

A MolSysSuite member therefore follows, as applicable: **MOLI engineering governance + MolSysSuite domain governance + repository-local rules**.

The effective engineering-governance snapshot is MOLI
`888902eb2ccc482c62c6f75da9d8f0bf9bb56442` plus MolSysSuite
`policy-v1.4.10`, as recorded in `suite.toml`. Links to MOLI `main` show
the latest upstream work, not the effective normative text.

The wider platform architecture belongs to [MOLI Architecture 1.0](https://github.com/uibcdf/moli/blob/main/architecture_1.0/README.md), and the shared engineering baseline belongs to [MOLI governance](https://github.com/uibcdf/moli). MolSysSuite is a first-class MOLI component with delegated internal governance. MOLI describes MolSysSuite as
the molecular modeling ecosystem alongside Scientific Context and optional
MOLI Agent reasoning.

Start with these central documents:

- [repository ownership contract](https://github.com/uibcdf/molsyssuite/blob/main/devguide/repository_contract.md);
- [issue and developer-guide reporting protocol](https://github.com/uibcdf/molsyssuite/blob/main/devguide/reporting_protocol.md);
- [cross-component feedback policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/cross_component_feedback.md);
- [effective MOLI Python support policy](https://github.com/uibcdf/moli/blob/888902eb2ccc482c62c6f75da9d8f0bf9bb56442/devguide/policies/python_policy.md) and the [MolSysSuite adoption profile](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_policy.md);
- [effective MOLI Python tooling policy](https://github.com/uibcdf/moli/blob/888902eb2ccc482c62c6f75da9d8f0bf9bb56442/devguide/policies/python_tooling_policy.md) and the [MolSysSuite tooling profile](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_tooling_policy.md);
- [effective MOLI support-library policy](https://github.com/uibcdf/moli/blob/888902eb2ccc482c62c6f75da9d8f0bf9bb56442/devguide/policies/python_support_libraries_policy.md) and [developer-tools policy](https://github.com/uibcdf/moli/blob/888902eb2ccc482c62c6f75da9d8f0bf9bb56442/devguide/policies/python_developer_tools_policy.md), with the [MolSysSuite member review profile](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_ecosystem_policy.md);
- [effective MOLI release-version policy](https://github.com/uibcdf/moli/blob/888902eb2ccc482c62c6f75da9d8f0bf9bb56442/devguide/policies/release_version_policy.md) and the [MolSysSuite release profile](https://github.com/uibcdf/molsyssuite/blob/main/devguide/release_version_policy.md);
- [GH Run Receptor dogfooding policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/gh_run_receptor_policy.md).

MOLI's conceptual architecture does not admit repositories to MolSysSuite.
`suite.toml` alone records governed members; its `role`, `membership`,
`maturity`, `development-mode`, and `capabilities` fields classify real
repositories rather than platform concepts.

Consult MOLI governance before changing an inherited platform engineering baseline. Consult MolSysSuite governance before changing a suite-member contract, dependency boundary, domain extension, reusable suite workflow, vendored integration guide, or behavior expected across MolSysSuite components.

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

Everyone who uses, develops, maintains or operates a suite component or UIBCDF support
tool must report actionable bugs, missing capabilities, improvements and new feature
proposals in the owning repository. Open an issue or add evidence to an existing one;
if you cannot file it, ask a maintainer to record it. Do not leave the finding only
in a chat, workaround or downstream issue. Reporting does not promise immediate
implementation. Use private reporting first for exploitable or confidential findings.
This adopts [MOLI's universal issue-feedback commitment](https://github.com/uibcdf/moli/blob/c6b78e92691fef2cbfa8065b33b0c75f11ba9a01/devguide/governance/reporting_protocol.md#universal-issue-feedback-commitment).

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

## UIBCDF development support

MOLI [catalogs four UIBCDF-owned support resources](https://github.com/uibcdf/moli/blob/c6b78e92691fef2cbfa8065b33b0c75f11ba9a01/devguide/governance/support_infrastructure.md):
[Pytest Receptor](https://github.com/uibcdf/pytest-receptor) for Python test reporting,
[GH Run Receptor](https://github.com/uibcdf/gh-run-receptor) for Actions inspection,
[the Conda build/upload action](https://github.com/uibcdf/action-build-and-upload-conda-packages)
for applicable Conda releases, and
[the Sphinx-to-Pages action](https://github.com/uibcdf/action-sphinx-docs-to-gh-pages)
for applicable Sphinx documentation publication. Use the applicable resource and report
tool defects or improvements in its own issue board. MolSysSuite governs member adoption;
MOLI owns the shared usage contract. The receptors remain suite auxiliary members.

## Physical quantities and units

A quantity must retain its value, unit and scientific meaning across computations,
storage and component boundaries. Serialized values carry their negotiated unit in
the same object; readers verify the record and explicitly name the expected field and
unit or dimension. Never infer a unit from a bare number, field name or session default.
Use an explicit target unit for boundary conversions and test under a non-default
session policy. A wrong but internally consistent source also needs domain checks.
The [published MOLI quantity integrity policy](https://github.com/uibcdf/moli/blob/c6b78e92691fef2cbfa8065b33b0c75f11ba9a01/devguide/policies/quantity_integrity_policy.md)
defines the target contract; member adoption is tracked below and is not established
by this guide alone.

PyUnitWizard owns the [serialization design](https://github.com/uibcdf/pyunitwizard/issues/83)
and [QuantityRecord codec](https://github.com/uibcdf/pyunitwizard/issues/82); take
format questions there. [MolSysSuite #46](https://github.com/uibcdf/molsyssuite/issues/46)
tracks member adoption and migrations. The effective versioned policy snapshot remains
the commit pinned in `suite.toml` until a separate policy rollout changes it.

## Common development baseline

The [effective MOLI engineering governance](https://github.com/uibcdf/moli/blob/888902eb2ccc482c62c6f75da9d8f0bf9bb56442/devguide/governance/policy_inheritance.md) owns the shared Python support, CI, Ruff, support-library, developer-tool and public-release rules. The pinned MOLI revision in `suite.toml` supplies their machine-readable values. Follow the [suite Python adoption profile](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_policy.md), [CI profile](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_ci_policy.md), [tooling profile](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_tooling_policy.md), [ecosystem review profile](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_ecosystem_policy.md) and [release profile](https://github.com/uibcdf/molsyssuite/blob/main/devguide/release_version_policy.md) for member-specific adoption, evidence and historical exceptions. Type checking and scientific or UI gates remain repository-local.

The new support-library and developer-tool policies require member-specific review.
Their publication does not establish adoption by a member. `suite.toml` records
each Python member's separate review states, and
`devtools/scripts/python_ecosystem_status.py` displays them.

During an accepted Python transition, `suite.toml` may authorize named components after component-specific evidence. Only components marked `admitted` may claim the wider target support.

Every root integration guide synchronized from another repository is generated, read-only content. List its exact path in Ruff `extend-exclude`; propose changes at the canonical source and resynchronize the exact copy. The suite checks the exclusion and byte-level drift.

## Public release versions

MOLI defines public component release identity in its [effective release-version policy](https://github.com/uibcdf/moli/blob/888902eb2ccc482c62c6f75da9d8f0bf9bb56442/devguide/policies/release_version_policy.md). MolSysSuite maintains member enforcement, the historical-tag inventory and the separate `policy-vX.Y.Z` governance-release namespace.

## Repository badges

MOLI owns the general evidence principle; MolSysSuite owns its member-role taxonomy and generated suite identity baseline. Every member README carries the centrally generated MolSysSuite identity baseline in
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

Follow the [effective MOLI developer-tools policy](https://github.com/uibcdf/moli/blob/888902eb2ccc482c62c6f75da9d8f0bf9bb56442/devguide/policies/python_developer_tools_policy.md)
and the repository's `GH_RUN_RECEPTOR_GUIDE.md` where present. The suite's
[dogfooding profile](https://github.com/uibcdf/molsyssuite/blob/main/devguide/gh_run_receptor_policy.md)
tracks readiness and actual operator use, provider feedback, and any bounded
member exception. Guide presence alone does not establish active adoption.

## Release archival and DOI claims

MOLI owns the platform DOI/archival principles. MolSysSuite governs its member-level applicability, evidence inventory, rollout and domain-specific exceptions; each component still owns its metadata, release gates, artifacts and release
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
