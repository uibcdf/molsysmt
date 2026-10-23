---
summary: PDB exports from native topology and OpenMM Modeller delegate incorrectly
issue: uibcdf/molsysmt#423
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: medium
verification: reproduced
area: [form, convert]
guard: tests/conversion_truth/test_declared_pdb_edges.py::test_declared_pdb_edge_executes_directly_and_publicly
normative:
blocked_by: []
supersedes: []
---

# PDB exports from native topology and OpenMM Modeller delegate incorrectly

**Reported:** 2026-10-22, during the local PDB execution expansion of uibcdf/molsysmt#181.
**Status:** Resolved; direct/public routes and value or resource contracts pass.

## What

Native Topology export imports an OpenMM identity converter and binds the box positionally to `atom_indices`, raising `multiple values for argument atom_indices`. Modeller export imports the same foreign identity converter and calls a getter with `atom_indices` instead of `indices`, raising `TypeError`.

```bash
python -m pytest tests/conversion_truth/test_declared_pdb_edges.py --receptor=llm -n 12
```

The initial correctly constructed 32-edge profile gives four failures and
28 passes. Those failures comprise this report and the other PDB reports
uibcdf/molsysmt#422, uibcdf/molsysmt#423 and uibcdf/molsysmt#424.

## How

Reuse native PDB serialization through the actual source adapters. Native Topology text export must pair full-source explicit geometry with the selected topology, preserve its existing MolSys owner and accept equivalent length units. Select once in the final native writer.

## Why

Declared PDB exports are unusable with valid topology and coordinate inputs. Matching topology/coordinate selection is also part of the existing contract.

## What is measured and what is assumed

Runtime failures are reproduced with tiny local sources, normal argument digestion
and installed providers. The profile stops at the first failing direct call;
separate mirrored regression tests exercise direct and public routes explicitly.
No full PDB-field or independent chemical accuracy certification is claimed.

## What was refuted

Missing optional packages are not the cause. MDTraj and OpenMM are installed.
Two initial harness mistakes (a nonexistent root-level handler export and rejecting
valid HETATM records) were corrected before the four runtime defects were counted.

## Scope and exclusions

Repair the registered route and preserve its documented selection and unit semantics.
No new parser, chemical inference policy, file format or release qualification.

## Acceptance criteria

- The affected direct and public conversions complete with valid local input.
- Values or file content, not only returned forms, are checked in `tests/form/molsysmt_Topology/test_pdb_export.py`.
- The complete PDB execution profile passes without runtime-failure skips.

## Provenance

Linux x86_64, Python 3.14.7, MDTraj 1.11.1 and OpenMM 8.6.1,
2026-10-22, starting from source commit fe5036c1f4c145ec2eecf1627e80eb70fc995618.
Provider versions will be checked in the final execution receipt.

## Resolution and verification

The bounded PDB execution profile passes all 32 edges directly and publicly.
The final profile/repair run passes 175 cases (no skips/failures, 18.15 seconds),
plus one separate executor-partition control. The broader PDB/native topology/
Modeller/conversion regression passes 2,284 cases with no skips/failures in
98.67 seconds. Six changed-adapter doctests pass. Three affected User Guide/
course notebooks execute successfully; source-level evidence does not qualify
an installed release candidate.

The full commands, environment and limits are in the
[execution receipt](../../../devtools/data/conversion_execution_pdb_20261022.json).
The guard above executes the affected behavior; additional mirrored native and
Modeller tests compare atom names, selected positions, physical units and source
ownership. Resource guards check actual paths after return, errors and interruption.
