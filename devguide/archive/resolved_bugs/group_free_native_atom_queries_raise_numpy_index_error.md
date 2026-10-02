---
summary: Group-free native atom queries leak a NumPy indexing error.
issue: uibcdf/molsysmt#233
status: resolved
opened: 2026-10-02
closed: 2026-10-02
severity: high
verification: reproduced
area: [form, get, topology]
guard: tests/form/rdkit_Mol/test_contract.py::test_group_free_native_queries_return_absent_without_inventing_groups
normative:
blocked_by: []
supersedes: []
---

# Group-free native atom queries leak a NumPy indexing error

**Reported:** Existing upstream issue, rechecked locally on 2026-10-02.
**Status:** Resolved with executable regression guards.

## What

A valid RDKit-derived MolSys with zero groups and has_attribute(group_name) false raised a raw NumPy IndexError when group_name was requested at atom level.

## How

Native group_id, group_name, and group_type atom getters indexed an empty group inventory using nullable atom memberships. They now return None before indexing when the native topology has no groups. MolSys delegates to these getters and inherits the same result.

## Why

Clients such as uibcdf/dockingmt#9 must distinguish absent residue metadata from an invalid molecular system without requiring fabricated LIG groups.

## What is measured and what is assumed

The old failures were reproduced against main 78981d6c1. The focused tests
exercise the corrected paths. No unit is inferred from numerical values.

## What was refuted

The input is not an invalid molecule and does not require invented
residue groups. Connectivity and atom inventory are valid even when
residue metadata is absent.

## Scope and exclusions

The guard checks Topology and MolSys, all atoms and explicit atom selections, all three affected metadata attributes, retained atom counts, and zero groups before and after queries. Partially assigned memberships in a nonempty group inventory are outside this zero-group defect.

## Acceptance criteria

The addressable guard `tests/form/rdkit_Mol/test_contract.py::test_group_free_native_queries_return_absent_without_inventing_groups` must pass and fail when its reported mechanism
returns. The public documentation and affected course modules describe the
observable behavior.

## Provenance

Linux x86-64, CPython 3.13.14, NumPy 2.4.6, Pandas 2.3.3, h5py 3.16.0;
2026-10-02. Focused pytest runs use the repository's Pytest Receptor profile.
