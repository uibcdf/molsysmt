---
summary: Buch hydrogen-bond detector crashes when an evaluated structure has no accepted bonds
issue: uibcdf/molsysmt#253
status: active
opened: 2026-09-29
closed:
severity: medium
verification: reproduced
area: [api, structure]
guard:
normative:
blocked_by: []
supersedes: []
---

# Buch hydrogen-bond detector crashes on an empty evaluated structure

**Reported:** 2026-09-29, while testing the Interactions design against a
bundled molecular trajectory for `uibcdf/molsysmt#251`.
**Status:** Reproduced; the public detector still raises on this input.

## What

An evaluated structure can have eligible donors and acceptors but no accepted
hydrogen bonds. The Buch detector raises `IndexError` rather than returning an
empty per-structure result. The first two structures of the bundled
pentalanine trajectory reproduce the problem:

```bash
python -c 'import molsysmt as msm; p="molsysmt/data/h5msm/traj_pentalanine.h5msm"; msm.interactions.hbonds.get_buch_hbonds(p,structure_indices=[0,1,2,50,99],pbc=False)'
```

## How

`molsysmt/interactions/hbonds/get_buch_hbonds.py` accumulates accepted
distances in `tmp_distances`. When the frame has zero accepted bonds, it calls
`puw.utils.sequences.concatenate(tmp_distances, ...)` at line 133. That
utility accesses `sequence[0]`, raising `IndexError` on the empty list.
The current early empty-result branch only covers a selection with no eligible
donors or acceptors; it does not cover eligible atoms with no observed bond in
a particular structure. The code also builds a NumPy array from per-frame
triple arrays, so frames with different bond counts need a separate shape and
return-contract check before this defect is considered resolved.

## Why

Sparse interaction trajectories naturally include evaluated structures with
zero results. This failure prevents a caller from analyzing the requested
structure set as a whole and masks the distinction between evaluated-empty
and unevaluated coverage. It also blocks direct use of the detector output as
a real-data fixture for `molsysmt.Interactions`.

## What is measured and what is assumed

**Reproduced:** the command above raises `IndexError: list index out of range`
from `pyunitwizard/utils/sequences/concatenate.py:11`, reached through the
detector's empty `tmp_distances`. In the first 100 bundled pentalanine frames,
the same donor/acceptor and distance-neighbor helpers find 59 accepted
geometries across 39 nonempty frames; 61 frames have zero accepted geometries.
The control is reproducible with:

```bash
python devtools/scripts/benchmark_interactions_real_hbonds.py --frames 100 --block-size 25
```

**Not established:** whether the same failure exists in the alternate
selection branch or in the Luzard–Chandler detector. Those require focused
checks rather than extrapolation from this branch.

## What was refuted

The source has eligible atoms: six donor pairs and twelve acceptors are
returned for this trajectory. The CSR neighbor search also returns proximity
pairs in the failing frames. The empty accepted result arises after excluding
self donor/acceptor pairs, so the early no-donors/no-acceptors path cannot
protect this case.

## Scope and exclusions

This report covers the Buch detector's empty evaluated-structure behavior and
the shape of mixed empty/nonempty frame output. It does not change hydrogen-
bond criteria, add an `Interactions` output option, or claim scientific
validation of the Buch criterion.

## Acceptance criteria

- A focused pytest guard reproduces a frame with eligible donors and
  acceptors but zero accepted bonds, and verifies an empty result without an
  exception.
- A mixed empty/nonempty explicit structure list returns aligned triples and
  distance arrays for every requested structure, preserving frame order and
  documented units and shapes.
- Existing nonempty Buch tests still pass, and the return contract is
  documented for variable per-frame counts.

## Provenance

Observed 2026-09-29 on Linux 7.0.0-28-generic x86_64, Intel Xeon E5-2630 v4,
Python 3.13.14, NumPy 2.4.6, using the bundled
`molsysmt/data/h5msm/traj_pentalanine.h5msm` trajectory.
