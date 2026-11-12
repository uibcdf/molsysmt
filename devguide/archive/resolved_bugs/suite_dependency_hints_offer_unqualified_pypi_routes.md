---
summary: Suite dependency hints offer unqualified PyPI routes
issue: uibcdf/molsysmt#730
status: resolved
opened: 2026-11-12
closed: 2026-11-12
severity: medium
verification: reproduced
area: [deps]
guard: tests/test_dependencies_architecture.py::test_missing_suite_provider_offers_only_its_uibcdf_conda_route
normative:
blocked_by: []
supersedes: []
---

# Suite dependency installation hints

## What

The incoming central audit identifies Ackredit and MolSysViewer installation
hints that advertise PyPI rather than the reviewed `uibcdf` Conda route.
The current source retains both declarations. This is acquisition guidance,
not a missing-engine, version-floor or scientific defect. MolSysSuite #167
owns the shared route inventory and generator.

## How

Two missing-provider controls fail against the original configuration.
The correction sets explicit `pypi=None`, package name and `channel="uibcdf"`,
preserving optional Ackredit and required MolSysViewer. Tests model absence;
no provider is uninstalled, installed, upgraded or contacted. Real DepDigest
introspection and the guarded diagnostic must offer only the expected Conda
command; the consumer must not execute after the missing-provider error.

The first combined attempt has nine failures and 99 passes. Eight expose an
old auditor assumption that every hard dependency has a PyPI hint. One old
mutation guard changes the first `pypi=None` entry, which now belongs to
Ackredit rather than its intended PyTraj provider. Targeting that provider
preserves the same negative assertion; it does not relax the contract.

## Why

A missing-library message must give a usable acquisition route. Hard/soft
classification does not establish PyPI availability. The auditor now accepts
a valid explicit hard Conda route while retaining the required public runtime
declaration. Independent negative controls reject malformed package/channel
metadata, embedded constraints/extras/markers and an absent requirement.
Third-party routes, version floors, optionality and lazy loading remain.

## Resolution

The final cohort passes 118 cases without warnings or skips: actual dependency
architecture/diagnostics, existing OpenFF acquisition contracts and the full
read-only auditor suite. Ten new positive/negative auditor cases preserve the
underlying checks. The maintained
[dependency audit guidance](../../dependency_contract_audit.md) distinguishes
route metadata from provider/publication qualification. The
[receipt](../../../devtools/data/suite_installation_hint_receiving_730_20261112.json)
retains original failures, exact inputs and one-CPU/1.5-GiB resource controls.
Common governance and publication/board receiving are recorded separately.

The addressable guard checks both real library classifications, DepDigest's
reported acquisition metadata and the SMonitor-backed missing-library error.
It fails if either unsupported pip hint returns or an absent provider executes
its consumer. This is source receiving, not installed-pair qualification.


### Common-check closeout — 2026-11-12

All fifteen common fast gates, generated-index checking and whole-repository
Ruff lint/format pass with unchanged checked inputs. Twenty-four exact task-owned
terminal services are retired/already collected after MainPID-zero checks; no
foreign process is signalled. The receiving records retain the staged scope
and native exits. Full scientific/source, installed and publication obligations
remain outstanding rather than being replaced by these controls.
