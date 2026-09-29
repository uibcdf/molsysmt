---
summary: Luzard-Chandler hydrogen bonds fail on empty or variable per-structure counts
issue: uibcdf/molsysmt#259
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

# Luzard-Chandler hydrogen bonds fail on empty or variable counts

**Reported:** 2026-09-29, during the optional detector-result adapter work
under `uibcdf/molsysmt#250` and `uibcdf/molsysmt#252`.
**Status:** Active; reproduced before changing the detector.

## What

Eligible donors and acceptors can produce an evaluated frame with no
candidates. The detector raises `IndexError` rather than returning shaped
empty triples, distances, and angles. Two nonempty frames with different
accepted counts raise a ragged-array `ValueError`.

```bash
python - <<'PY'
import runpy
import molsysmt as msm
molsys = runpy.run_path('tests/interactions/hbonds/test_buch_results.py')['_varying_system']()
for indices in ([1], [2, 0]):
    try:
        msm.interactions.hbonds.get_luzard_chandler_hbonds(
            molsys, structure_indices=indices, pbc=False)
    except Exception as error:
        print(indices, type(error).__name__, str(error))
PY
```

## How

`interactions/hbonds/get_luzard_chandler_hbonds.py` concatenates an empty
distance list before shaping the empty triple array. For varying counts,
it converts the list of per-frame triple arrays to one rectangular NumPy
array. Both the one-selection and two-selection routes repeat this logic.

## Why

Sparse trajectories contain empty frames and varying counts. This prevents
normal detector use and blocks its optional `Interactions` result, including
the explicit evaluated-empty coverage requested by `uibcdf/molsysviewer#114`.
The client subsequently excludes Luzard-Chandler from its initial integration;
the MolSysMT defect and adapter remain in scope here.

## What is measured and what is assumed

**Reproduced:** `[1]` raises `IndexError: list index out of range`;
`[2, 0]` raises a NumPy inhomogeneous-shape `ValueError`. The synthetic fixture
has four atoms and one covalent donor-H pair. This is a return-contract
failure, not independent scientific validation of the method.

## Scope and exclusions

Preserve rectangular default outputs when counts agree. Support aligned
lists with shaped empty entries when counts vary, using nm and radians.
Do not change the D-A distance or strict H-D-A angular criterion. The
Interactions adapter and software-version metadata are tracked by #250/#252.

## Acceptance criteria

A focused test must check a mixture of zero, one, and two accepted bonds,
nonconsecutive structure order, and aligned triples, nm distances, and radian
angles. It must fail on the original detector. Both selection routes need
coverage, including a direction with no eligible donors.

## Provenance

Reproduced on 2026-09-29 under Linux x86_64, Python 3.13.14, NumPy 2.4.6,
and PyUnitWizard 0.27.0, with the bundled Rust backend.
