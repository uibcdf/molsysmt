---
summary: Public MolSys geometry edits preserve stale attached interactions
issue: uibcdf/molsysmt#285
status: resolved
opened: 2026-10-01
closed: 2026-10-01
severity: high
verification: reproduced
area: [form, native, tests]
guard: tests/form/molsysmt_MolSys/test_geometry_edit_interactions.py
normative:
blocked_by: []
supersedes: []
---

# Public MolSys geometry edits preserve stale attached interactions

**Reported:** 2026-10-01 during the post-qualification native lifecycle audit.
**Status:** Resolved with staged frame-local invalidation in native adapters.

## What

A public coordinate edit preserves outdated attached observations and evaluated
coverage. An explicit N-H bond at 0.1 nm and an O at 0.3 nm gives a Buch
H-A observation. After moving O to 1.0 nm:

```python
msm.set(source, selection=[2], structure_indices=[0],
        coordinates=msm.pyunitwizard.quantity([[[1, 0, 0]]], 'nm'))
source.interactions['buch'].query(structure_indices=[0]).n_interactions
# 1: stale observation
msm.interactions.hbonds.get_buch_hbonds(
    source, pbc=False, output_type='molsysmt.Interactions'
).query(structure_indices=[0]).n_interactions
# 0: recalculated geometry
```

## How

Native MolSys coordinate and box adapters delegate to Structures without
invalidating attached analyses. Domain validation cannot detect changed geometry.
Reuse the existing immutable `Interactions.invalidate_structures()` primitive
through a private MolSys owner operation; private helpers remain undecorated.
Stage all changed results before geometry writes so allocation or index errors
cannot occur after a write while leaving old observations attached. Once the
geometry delegate starts, uncertain/partial failures must retain unevaluated
coverage rather than preserving possibly stale observations.

## Why

Clients can query, draw or persist observations against incompatible geometry.
Related provider lifecycle: uibcdf/molsysmt#252; consumer: uibcdf/molsysviewer#114.

## What is measured and what is assumed

**Reproduced:** provider `df1a298e7`, Python 3.13.14, Linux x86_64. Stored count
remained one and recalculated count became zero in structure 0. No performance
claim. Existing immutable invalidation copies packed columns; this correction
is not an incremental editor or a bounded-memory replacement algorithm.

## What was refuted

Matching atom/frame dimensions does not establish current observation geometry.
Deleting observations without removing evaluated coverage would incorrectly
label an edited frame as evaluated-empty. Recomputing every frame is unnecessary.

## Scope and exclusions

Public native MolSys coordinate and box setters, including delegated transforms,
multiple named analyses, frame selection, no-ops, prior views and persistence.
Raw edits through separately obtained Structures, mutable-array access, chemistry
edits, and incremental insertion/replacement remain separately scoped under
uibcdf/molsysmt#251 and uibcdf/molsysmt#252. No observer ownership is introduced
for arbitrary aliased objects; no automatic scientific recalculation occurs.

## Acceptance criteria

1. Coordinate and box edits remove target-frame observations and evaluated
   coverage for attached analyses, including previously evaluated-empty frames.
2. Nonconsecutive/repeated selections affect only the requested frames; untouched
   frames, named analyses, roles, images, units and producer metadata survive.
3. Existing result/query snapshots remain unchanged. Empty selections and
   non-geometric edits preserve results; pre-delegation validation errors preserve
   geometry and analyses. A possibly partial delegate failure leaves target
   frames unevaluated.
4. Public H5MSM conversion preserves invalidated versus evaluated-empty coverage.
5. Document the supported mutation boundary, update User Guide/Cookbook/course,
   and close with the public regression guard after affected tests and gates pass.

## Resolution

Native MolSys coordinate and box setters enter the shared private
`_editing_structure_geometry` owner context. It constructs independent
invalidation snapshots for affected named analyses before any geometry write.
Its finalizer publishes those snapshots even if delegation raises after a
partial write. Allocation or earlier validation failures leave both geometry
and analyses unchanged. Results with no intersecting evaluated frames are
reused, and empty frame/atom selections skip invalidation.

Full geometry assignment with attached results rejects structure-axis resizing
before mutation; callers use supported extraction/append operations instead.
The context reuses `Interactions.invalidate_structures`; no detector runs, no
new storage layer is introduced, and its packed-array copy cost remains explicit.
General transforms that delegate through the setters inherit this ownership rule.

Updated the public and adapter docstrings, the normative interaction contract,
Foundations, Set Toolbox, executable sparse Cookbook and Common Core Module 10.
The #251/#252 records identify this concrete lifecycle fix without implying that
raw Structures writes, chemistry edits or incremental replacement are solved.

## Verification

**Contract-tested**, Python 3.13.14, Linux x86_64:

- The guard's real Buch fixture failed before correction: moving the acceptor
  left one stored observation while recalculation returned zero.
- The final guard has **16 passing cases**, covering coordinate/box changes,
  nonconsecutive and repeated frames, evaluated-empty and unevaluated frames,
  multiple names, previous views, angstrom input, H5MSM conversion, no-ops,
  allocation failure, a simulated partial-write failure, axis-resize rejection,
  box clearing, and public translation in-place and on a copy.
- Affected setters, native collection, translate/center, result queries and
  public persistence: **111 passed** at the combined checkpoint. The final
  box-clearing case was checked in the focused run below.
- Final focused guard plus `--doctest-modules molsysmt/basic/set.py
  molsysmt/form/molsysmt_MolSys/set.py`: **17 passed** (16 regressions and one
  public doctest case).
- All interaction families, native attachment, InteractionsDict and public
  H5MSM/association tests: **568 passed**. Warnings came from deliberate
  tiny-budget tests and legacy H5MSM fixtures; no skips.
- All five Python blocks in the sparse Cookbook executed successfully.
  Notebook code cells and saved outputs were preserved. Sphinx HTML returned
  exit 0 with existing course/MyST/toctree diagnostics.
- Ruff, dependency validation, public signature stability and the form-adapter
  audit passed (93 forms; delivery debt did not regress).

No incremental-edit performance or browser qualification is claimed.
