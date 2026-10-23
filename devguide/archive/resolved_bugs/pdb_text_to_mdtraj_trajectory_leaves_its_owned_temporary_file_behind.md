---
summary: PDB text to MDTraj trajectory leaves its owned temporary file behind
issue: uibcdf/molsysmt#425
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: medium
verification: reproduced
area: [form, convert]
guard: tests/form/string_pdb_text/test_to_mdtraj_Topology.py::test_pdb_text_retires_owned_scratch_on_success_and_failure
normative:
blocked_by: []
supersedes: []
---

# PDB text to MDTraj trajectory leaves its owned temporary file behind

**Reported:** 2026-10-22, while qualifying scratch ownership in uibcdf/molsysmt#181.
**Status:** Resolved; direct/public success, error and interruption cleanup pass.

## What

The PDB text-to-MDTraj trajectory adapter creates an unnamed caller-independent
PDB through `to_file_pdb` and never removes it. A wrapped file reader captures
the actual filename: after a successful three-atom, two-structure conversion,
`Path(filename).exists()` is True. The reproduction removes only its own file.

## How

Use an owned `TemporaryDirectory` and pass an explicit path to the existing
text writer. The existing file reader performs selection and unit handling.
The context retires the file after normal return, exceptions and interruption.
Declare the optional MDTraj dependency at the public adapter boundary.

## Why

Repeated text imports accumulate disk data without returning the path to the
user. Downstream workflows cannot retire an intermediate they do not own.

## What is measured and what is assumed

The successful leak was measured on the original adapter with literal local
PDB text, not inferred from source alone. New tests wrap the actual registered
file reader, check the path exists during parsing and assert both file and
parent disappear afterwards, through direct and public conversion.

## What was refuted

Caller-owned output is not involved: this route returns a resident trajectory.
Fixing the text-to-topology buffer defect (uibcdf/molsysmt#424) does not itself
retire the independent trajectory adapter's temporary file.

## Scope and exclusions

Only adapter-owned scratch data. Explicit public file output remains owned by
the caller; no global temporary-directory cleanup or parser replacement.

## Acceptance criteria

`tests/form/string_pdb_text/test_to_mdtraj_Topology.py` checks both MDTraj
targets, normal return, reader errors and KeyboardInterrupt, directly and publicly.
Separate trajectory checks compare selected structure order, positions and units.

## Provenance

Linux x86_64, Python 3.14.7, MDTraj 1.11.1, OpenMM 8.6.1, 2026-10-22.
Original source baseline: fe5036c1f4c145ec2eecf1627e80eb70fc995618.

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
