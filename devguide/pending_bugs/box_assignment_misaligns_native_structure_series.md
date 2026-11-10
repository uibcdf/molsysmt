---
summary: Full geometry assignment can silently misalign native structural series.
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

# Geometry assignment must preserve the shared structure axis

## What / How / Why

On public 68bd19103, assigning one box to three coordinate/time structures returns
normally through msm.set, Structures.set_box or direct box assignment without
named analyses. The next n_structures read raises. An attached analysis happened
to enable validation, but alignment is an invariant for standalone Structures
and analysis-free MolSys too. The protected 18-case baseline has twelve failures
and six passing existing analysis guards; it does not import Viewer. Coordinates
are unchanged, but successful mutation leaves an unusable shared structure axis.

Companion checks reproduce the same defect for full coordinate replacement.
The standalone and analysis-free MolSys public, native-method and property paths
accept one or four coordinate structures over three time/box entries. Twelve
new protected cases fail before the shared correction; the six cases with named
analyses already reject. Both geometry setters require this same invariant.

## Contract and implementation

Keep the existing exact-cardinality contract: supply one matrix per addressed
structure. A single box is one structure, not an implicit constant-cell broadcast.
Uniform cells can be repeated explicitly. Selected/nonconsecutive edits already
require exact shapes in protected block replacement; full-axis edits must be
consistent with that contract. No new broadcast policy is introduced during
stabilization. None clears a full series; an empty selection is a no-op.

The native geometry-publication owner validates proposed coordinates or boxes against all
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

## Rebuilder integration receiving — 2026-11-10

The first corrected full cohort has 8,447 passes and five failures. Stricter
coordinate publication exposes old staged mutations in native hydrogen placement,
explicit terminal attachment and default native Iterator chunks. The two
builders copied a domain, assigned its larger coordinates, and only afterwards
removed atom observations their existing policy cannot carry. They now finish
removing those observations before assigning the new coordinates; strict
rejection, warnings, source preservation and scientific placement stay unchanged.

Iterator previously described one multi-attribute set as atomic, although basic
set is sequential. Native outputs now use existing selected conversion for each
complete chunk,
including chemical-state associations, other observables and named-analysis maps.
They return independently owned native chunks; a final short chunk is assembled
with all its structural series together. The non-native reuse route is unchanged.
No initialization bypass is added to edits. The source remains unchanged, units and repeated structure positions
are preserved, and owner association/analysis consistency checks still apply.

The intermediate 217-case receiving exposes three retained association-length
failures in a reusable-container attempt; that attempt is not accepted. A later
363-case receiving exposes the separate selected-reference conversion defect
tracked as #698. With the selected conversion correction, 535 affected builder,
PDBQT, native chunk and composed-conversion controls pass without omissions.
