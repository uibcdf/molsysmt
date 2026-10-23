---
summary: PDB text to MDTraj topology passes an unsupported closed buffer
issue: uibcdf/molsysmt#424
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: medium
verification: reproduced
area: [form, convert]
guard: tests/form/string_pdb_text/test_to_mdtraj_Topology.py
normative:
blocked_by: []
supersedes: []
---

# PDB text to MDTraj topology passes an unsupported closed buffer

**Reported:** 2026-10-22, during the local PDB execution expansion of uibcdf/molsysmt#181.
**Status:** Resolved; direct/public routes and value or resource contracts pass.

## What

`string:pdb_text -> mdtraj.Topology` passes a closed `StringIO` to MDTraj load_topology, which requires a supported path or topology-bearing object and raises `TypeError: A topology is required`.

```bash
python -m pytest tests/conversion_truth/test_declared_pdb_edges.py --receptor=llm -n 12
```

The initial correctly constructed 32-edge profile gives four failures and
28 passes. Those failures comprise this report and the other PDB reports
uibcdf/molsysmt#422, uibcdf/molsysmt#423 and uibcdf/molsysmt#424.

## How

Write the literal input through the existing PDB text writer in an owned TemporaryDirectory and call the registered file-to-MDTraj topology reader. Retire scratch files after success and failure; keep MDTraj as the parser rather than changing chemical interpretation.

## Why

A registered public route cannot read valid local PDB text even with MDTraj installed.

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
- Values or file content, not only returned forms, are checked in `tests/form/string_pdb_text/test_to_mdtraj_Topology.py`.
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
