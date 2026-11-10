---
summary: Full box assignment can silently misalign native structural series.
issue: uibcdf/molsysmt#695
status: active
opened: 2026-11-10
closed:
severity: high
verification: reproduced
area: [native, set, pbc]
guard: tests/native/test_box_assignment_alignment.py
normative:
blocked_by: []
supersedes: []
---

# Box assignment must preserve the shared structure axis

## What / How / Why

On public 68bd19103, assigning one box to three coordinate/time structures returns
normally through msm.set, Structures.set_box or direct box assignment without
named analyses. The next n_structures read raises. An attached analysis happened
to enable validation, but alignment is an invariant for standalone Structures
and analysis-free MolSys too. The protected 18-case baseline has twelve failures
and six passing existing analysis guards; it does not import Viewer. Coordinates
are unchanged, but successful mutation leaves an unusable shared structure axis.

## Contract and implementation

Keep the existing exact-cardinality contract: supply one matrix per addressed
structure. A single box is one structure, not an implicit constant-cell broadcast.
Uniform cells can be repeated explicitly. Selected/nonconsecutive edits already
require exact shapes in protected block replacement; full-axis edits must be
consistent with that contract. No new broadcast policy is introduced during
stabilization. None clears a full series; an empty selection is a no-op.

The native geometry-publication owner validates the proposed box against all
stored structural series before publishing or invalidating named analyses,
independent of owner/analysis presence. New Structures construction assembles
its payload in a short explicit initialization scope, then performs the existing
complete alignment validation. The transient scope flag is removed even on
failure. It is not an escape hatch for edits of an existing object. Existing
immutable blocks, selected-block updates and owner invalidation remain shared.

## Required receiving and limits

Receive native/form/direct property paths, units, complete and nonconsecutive
selected axes, existing/absent boxes, clearing/empty/no-op, original metadata,
invalid cardinalities and named-analysis coverage. Constructors remain strict
about their complete payload. A new box-only object may define its sole axis;
this is distinct from resizing one series in a coordinate-bearing object.
Run affected native/form/geometry/persistence consumers and the registered
scientific cohort. The source-only correction does not qualify a new package,
platform, GUI family or release. The supplemental repair adds no formal weight.
