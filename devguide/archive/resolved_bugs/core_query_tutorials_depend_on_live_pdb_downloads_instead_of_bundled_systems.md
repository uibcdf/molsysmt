---
summary: Core query tutorials depend on live PDB downloads instead of bundled systems.
issue: uibcdf/molsysmt#753
status: resolved
opened: 2026-11-14
closed: 2026-11-14
severity: low
verification: reproduced
area: [docs]
guard: devtools/tests/test_basic_tutorial_data.py::test_basic_query_tutorial_loads_a_real_system_without_network
normative:
blocked_by: []
supersedes: []
---

# Core query tutorials require remote data unnecessarily

**Reported:** 2026-11-14, during essential-example execution under #334.
**Status:** corrected; actual notebooks, offline guards and strict site receiving pass.

## What

The get, info, select and extract tutorials load `1TCD` or `181L` through the
PDB identifier form. These are actual downloads, including fallback formats
and retry delays, even though both systems are bundled. The four real setup
cells fail when the download boundary refuses external data. This is a
reproducibility defect in local tutorials, not a defect in remote conversion.

## How

Load the same named structures from `msm.systems`: TcTIM's `1tcd.bcif.gz`
and T4 lysozyme L99A's `181l.bcif.gz`. Retain the native target, all examples,
scientific scenarios and anchors. Add the demo-catalog explanation after the
first load. The get introduction also identifies its bond-bearing object as
a molecular system, preserving Topology's independent inventory ownership.

The guard executes each tutorial's actual setup cells, refuses real sockets
and the remote download boundary, and requires a native molecular system
with a populated atom axis and matching coordinates. No molecular values
are supplied by the guard. Rejecting the download boundary immediately avoids
exponential backoff without converting an unsuccessful download into success.

## Why

A basic query lesson should work with its included data independently of
network availability and remote record changes. Dedicated identifier/download
tutorials and adapter tests retain their external-service contracts.

## What is measured and what is assumed

The initial socket-only experiment was deliberately terminated after about
87 seconds while retrying; its native signal result is retained, not counted
as four failures or a pass. The immediate-boundary baseline has four genuine
failures. The four corrected full notebooks execute 127 cells successfully
in fresh Jupyter kernels. Runtime origins identify the frozen source,
PyUnitWizard 0.29.2, ArgDigest 0.15.0, DepDigest 0.15.1 and SMonitor 0.21.0.
The subsequent independent #755 repair receives a separate selection rerun.

## What was refuted

A matching code fingerprint or a clean Sphinx build does not establish that
examples still execute against the current library. Returning fabricated
molecular data from a network mock would not establish offline loading.

## Scope and exclusions

Only tutorial inputs/prose/actual saved outputs and developer guards change.
No adapter, dependency, public query signature or scientific method changes.
This receives local examples, not browser behavior, installed artifacts,
other platforms, the entire notebook corpus or the final release pair.

## Acceptance criteria

- Four actual setup cells succeed with external data services unavailable.
- All four complete tutorials execute; existing native/chemical examples remain.
- Save real outputs and runner-produced marks; retain failures and runtime scope.
- Relevant documentation checks and Ruff pass before publication to main.

## Receiving record

The [dated #334 receipt](../../../devtools/data/documentation_examples_receiving_334_20261114.json)
retains original unsuccessful attempts, actual runtime identities, full notebook
execution, strict full-site rendering and selected-article/asset receiving.
