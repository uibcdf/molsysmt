---
summary: Full geometry assignment can silently misalign native structural series.
issue: uibcdf/molsysmt#695
status: resolved
opened: 2026-11-10
closed: 2026-11-10
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

## Attached atom domains and typed values

Nine additional controls expose six native-method/property paths that resize an
attached coordinate atom axis despite a declared MolSys domain; the three public
set paths already reject. The shared native owner now checks that declaration
before publishing. Geometry-only, topology-bearing and chemistry-bearing owners
are covered without relying on analyses. All 547 affected rebuilder/iterator/
conversion cases pass after this guard.

Positive clearing/initialization controls also retain four original failures:
public first-axis initialization rejects an undeclared atom count, public None
clearing raises AttributeError, and native value digestion rejects None for two
coordinate operations. The public form now distinguishes undeclared from known
atom counts and handles None before shape checks. Typed native coordinate/box
methods delegate to their existing argument digesters, retaining units, shapes
and full-series None clearing. Invalid coordinate shape errors preserve the
structural cause instead of an unbound local exception. No validator is bypassed
and no topology or chemistry is inferred.

## Resolution — 2026-11-10

Native coordinate and box publication preserves all stored series and the declared owner atom domain before mutation/invalidation. Constructors remain strict; unknown first axes and None clearing remain usable. Full native/form, selected/repeated axes, rebuilt domains and independently owned Iterator chunks are guarded.

Qualified final source: `cdf6e878ffa53ef045ee3c9c568efd61cf9dcb61`. The [combined owner receipt](../../../devtools/data/construction_native_owner_receiving_421_695_696_697_698_699_20261110.json) preserves the original failing controls, failed intermediate integration attempts, source identities and bounded resources. The predecessor native cohort passes 8,813 cases. Final receiving retains 8,955 passes and one failed unit-context test oracle in the expanded 8,956-case cohort; the 415-case corrected focused cohort passes with byte-identical product source. All 116 registered scientific cases/74 nodes, 76 public/native doctest examples, strict seven-notebook validation, ten inspected HTML pages, twenty-six actual Jupyter checks and twenty-four representative native Qt checks pass on the explicitly recorded cohorts.

This is guarded Linux/Python 3.14 source resolution, not clean installed, other-platform, human or exact-candidate acceptance. The supplemental fix adds no original milestone weight. Public delivery and owning issue closure use the repository closeout route after independent blob verification.
