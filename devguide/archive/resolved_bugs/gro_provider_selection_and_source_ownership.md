---
summary: GRO provider selections misbind coordinates or consume the source reader.
issue: uibcdf/molsysmt#477
status: resolved
opened: 2026-10-26
closed: 2026-10-26
severity: high
verification: reproduced
area: [form, convert, structure]
guard: tests/form/file_gro/test_provider_selection_contract.py
normative:
blocked_by: []
supersedes: []
---

# GRO provider selections misbind coordinates or consume the source reader

## What

openmm.GromacsGroFile to native MolSys extracts topology and coordinates
separately. Native topology extraction sorts selected atom indices, while the
coordinate getter retains requested order. A reordered list can attach a
coordinate to the wrong atom. MDTraj GRO attributes rewind and read the
caller's stream, including the atom-count query performed during public convert.

## How

Build the complete native topology/selected-structure geometry first, then use
MolSys.extract once for the atom selection. Reuse its existing ordering rules
rather than sorting fields independently. For MDTraj, read an independent
read-only cursor with the original topology shared read-only; use the
provider's already stored atom count without reading coordinates. The public
copy operation separately clones mutable topology and starts a fresh cursor.
No source file is rewritten or main Iterator modified.

## Why

A conversion must preserve geometry-to-topology binding and caller ownership.
Successful completion and target type alone cannot detect these defects.
The repairs reuse existing native extraction and owning adapter operations;
no new chemistry inference, scientific criterion or public utility is needed.

## Reproduction

The independent two-structure literal water fixture selects atoms [2, 0] or [1]
and structures [1, 0, 1] under nm/pm policies through direct and public calls.
Before repair it reports 20 failures and 12 passing controls in 14.61 seconds:
four OpenMM atom-axis mismatches and sixteen consumed MDTraj readers.
An earlier run failed at file creation because the tmpfs user quota was full;
it provides no converter evidence. Two obsolete generated HTML directories
were removed after verifying ownership, generated markers and absence of active
build processes. Their regenerable outputs were unnecessary; repository
receipts and logs are retained. The valid baseline above was rerun afterwards.

## Acceptance

Check literal coordinates, distinct triclinic boxes, selected times, actual
source labels and repeated/reordered structures. Native MolSys output follows
native sorted atom ordering; coordinate-only Structures keeps requested order.
Reading/converting a MDTraj handle already positioned after its first structure
must preserve the remaining source text and iteration metadata. Source files
and OpenMM coordinate arrays remain unchanged. All direct/public routes and
both length policies must execute without missing-provider skips. Reachability
extension remains uibcdf/molsysmt#181; default-copy/bridge failures are separately
tracked in uibcdf/molsysmt#476.

## Default coordinate-delivery follow-up

After repairing selected conversion, a direct public `get(source,
coordinates=True)` guard exposes a missing system-coordinate getter despite
the form advertising coordinates. It rejects before calling the reader, so
it cannot qualify reader cleanup. The owning adapter now delegates the system
coordinate request to its existing atom reader on all atoms, with the normal
public argument boundary. This delivers an existing advertised attribute, not
a new coordinate field or guessed pipe. Failure/interruption guards exercise
real independent provider readers and assert their cleanup and original source
readability.

## Resolution — 2026-10-26

All selected direct/public OpenMM and MDTraj provider conversions retain
literal coordinate/box correspondence under both length policies. Native
MolSys extraction uses one sorted source atom axis; Structures-only selection
retains requested atom order. Selected structure order/repetitions and available
MDTraj times remain exact. The original unread second structure survives both
conversion and attribute/count queries. Real independent readers close after
success, RuntimeError and KeyboardInterrupt; source ownership and bytes remain
unchanged.

The first repair left eight public MDTraj cases failing because atom counting
still consumed the stream. Reading provider n_atoms metadata removes that I/O.
Three further query/cleanup cases exposed missing system-coordinate delivery;
the new documented wrapper delegates to the existing atom reader, after which
the final regression passes. These failed intermediate runs remain evidence,
not successful qualifications.

The final combined GRO/conversion-plan selection passes 437 cases with no
failures or skips in 36.15 seconds using twelve workers and Pytest Receptor;
21 intentional legacy H5MSM warnings remain. Both converter/query doctest
modules pass, the 491-notebook raw-schema guard passes and all fourteen fast
gates pass. Ruff lint/format pass. Incremental HTML compilation exits 0 with
zero errors and 21 warnings; broader documentation debt remains #144. Exact
scope/environment/hashes and commands are in
[the GRO receipt](../../devtools/data/conversion_execution_gro_20261026.json).
The current [form contract](../forms_and_conversions.md) and
[execution guide](../conversion_execution.md) own the durable rules. No
installed-artifact, full-suite, large-file benchmark, universal chemistry or
release pass is asserted. #181 retains remaining execution coverage debt.
