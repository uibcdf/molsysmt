---
summary: Account for compatibility-output memory beyond native neighbor CSR admission.
issue: uibcdf/molsysmt#693
status: open
opened: 2026-11-10
closed:
verification: inspected
area: [structure, performance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Account for compatibility-output memory beyond native neighbor CSR admission.

## What

Measure and account for memory in existing Python compatibility outputs beyond
#690's native numerical input/grid/scratch/CSR estimate. Do not equate that
estimate with process RSS or an OS reservation.

## How

Source inspection finds default neighbor object arrays retain per-row NumPy
view headers/object slots. Contact pair output keeps its Boolean map while
upper-triangle/nonzero/column-stack intermediates and `.tolist()` create arrays
and Python objects. The new native guard reserves the Boolean map and reduces
map filling, but does not claim to bound these separate legacy costs. No OOM
or incorrect result is reproduced for this representation scope.

## Why

A sparse search does not make dense or boxed compatibility results small. The
[guarded native repair](../archive/resolved_bugs/native_neighbor_cell_grids_can_allocate_gigabytes_for_two_atoms_and_a_small_cutoff.md)
must not imply a whole-process guarantee.

## Acceptance and exclusions

Measure representative row/occurrence populations under finite cgroup limits;
choose a justified estimate, bounded conversion or explicit representation
recommendation. Reuse existing CSR and iteration tools. Preserve public shapes,
units, indices, empty results and scientific values. Unsupported output sizes
need a clean refusal or documented bounded alternative. No speculative API,
dependency or automatic new pre-1.0 blocker is introduced.
