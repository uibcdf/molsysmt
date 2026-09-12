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
machine-readable registry of members, profiles, stabilization cohorts, and accepted
policies. Its `devguide/` contains the full normative texts and decision history.

The component repository remains authoritative for its implementation, tests, product
API, scientific evidence, releases, and local development tools. Local rules may be
stricter, but they must not silently contradict a common policy. A deviation needs a
tracked exception with its reason and expiration condition.

Start with these central documents:

- [repository ownership contract](https://github.com/uibcdf/molsyssuite/blob/main/devguide/repository_contract.md);
- [issue and developer-guide reporting protocol](https://github.com/uibcdf/molsyssuite/blob/main/devguide/reporting_protocol.md);
- [cross-component feedback policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/cross_component_feedback.md);
- [Python support policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_policy.md);
- [Python tooling policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_tooling_policy.md).
- [GH Run Receptor dogfooding policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/gh_run_receptor_policy.md).

Consult the central repository before changing a shared dependency boundary, supported
Python range, development baseline, issue vocabulary, reusable workflow, vendored guide,
or behavior expected across components.

## Cross-repository working state

Before work spanning components, use the MolSysSuite checkout to refresh and inspect every
registered component:

```bash
python devtools/scripts/suite_status.py
```

The command derives repository and cohort order from `suite.toml`, fetches remotes, and
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

Python libraries support Python `>=3.11,<3.14`; routine development uses Python 3.13 and
CI covers 3.11, 3.12, and 3.13. Ruff is the common formatter and linter, replacing Black,
isort, and Flake8. The required shared lint core is `E4`, `E7`, `E9`, `F`, and `I`;
repositories may add stricter rules. Pytest is the common test runner. Type checking and
domain-specific scientific or UI gates remain repository-local.

Every root integration guide synchronized from another repository is generated,
read-only content. List its exact path in Ruff's `extend-exclude`; do not reformat or edit
it in a component. Propose changes at the canonical source and resynchronize the exact
copy. The suite checks both the exclusion and byte-level drift.

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

## Stabilization order

The first stabilization wave is SMonitor, ArgDigest, DepDigest, PyUnitWizard, MolSysMT,
and MolSysViewer. Pytest Receptor and GH Run Receptor are supporting infrastructure.
TopoMT, PharmacophoreMT, and ElastNetMT are incubating: common policies still apply, but
their missing adoption work does not block the first stabilization outcome.
Lindelint is an auxiliary component developed for ElastNetMT and the wider suite: it is a
full governed member, while its adoption work likewise does not block wave 1.

Priority affects scheduling, not whether contributors communicate valuable discoveries
from any component.

## Before finishing component work

Check whether the change:

1. exposes a provider limitation that needs a cross-component issue;
2. changes a shared contract and therefore needs a central issue;
3. requires updating a local report, generated index, archived record, or issue state;
4. affects the common Python/tooling baseline or needs a documented exception;
5. should propose an improvement to this guide or another central policy.

Run the component's own tests and local gates. The MolSysSuite conformance workflow
checks the common baseline; it does not replace component-specific validation.
