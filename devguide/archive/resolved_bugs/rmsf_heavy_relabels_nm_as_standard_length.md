---
summary: Heavy RMSF relabels nm fluctuations as the active length unit.
issue: uibcdf/molsysmt#442
status: resolved
opened: 2026-10-23
closed: 2026-10-24
severity: medium
verification: reproduced
area: [structure, heavy, units]
guard: tests/heavy/test_length_observable_units.py
normative:
blocked_by: []
supersedes: []
---

# Heavy RMSF changes physical scale under alternate length units

**Reported:** 2026-10-23 while reviewing independent structure readers for the
addon under uibcdf/molsysmt#421 / uibcdf/molsysviewer#264. Filing explicitly
authorized by the principal maintainer.
**Status:** resolved in native MolSysMT. No addon calculation is introduced.

## What

With pm as the active standard length unit, forced RMSF returns physical
fluctuations 1000 times smaller than eager processing. The first nm value is
0.5217631435497472 eagerly, versus 0.000521763143549747 with forced chunking.
The three first eager values in the selected scope are
[0.5217631435497472, 0.548865554951073, 0.4382746096723505] nm; forced values
are [0.000521763143549747, 0.000548865554951073, 0.0004382746096723504] nm.

```python
import molsysmt as msm
puw = msm.pyunitwizard
molsys = msm.convert(
    msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    structure_indices=[0, 8, 3],
)
with puw.context(standard_units=['pm', 'ps', 'radians']):
    for mode in ['off', 'force']:
        result = msm.structure.get_rmsf(
            molsys, selection=[0, 2, 4], structure_indices=[2, 0, 2],
            heavy_mode=mode,
        )
        print(mode, puw.get_value(result, to_unit='nm'))
```

## How

[get_rmsf.py](../../../molsysmt/structure/get_rmsf.py) computes the streaming
variance with chunk coordinates in canonical nm, then attaches the active
standard length unit directly to those numeric values. The heavy result needs
correct nm attribution followed by conversion, rather than unit relabeling.
The mechanism resembles #440 but affects a separate public reducer/tool.

## Why

Changing the standard unit or execution policy must not change physical RMSF.
Automatic chunking can expose the heavy branch without an explicit forced call.
This reproduction concerns unit attribution, not whether structures were aligned.

## What was refuted

The same molecular data, atom selection and repeated/nonconsecutive structure
scope are used in both modes. Explicitly converting both outputs to nm retains
the discrepancy. No Viewer import, wrapper, rendering or molecular edit occurs.

## Scope and exclusions

The scientific owner fixes this tool; no addon formula, hidden unit reset or
routing workaround is introduced. RMSF remains pending while four independent
readers are received. This does not broaden the scope of #441 or authorize
publication or movement of any existing candidate/artifact.

## Acceptance criteria

Native eager/heavy fluctuations agree physically for nm, angstrom and pm
contexts, multi-chunk reduction and repeated/nonconsecutive structures. Compare
with independent variance calculations and check that input data and session
unit policy remain unchanged. Guard real numeric values, not only unit labels.

## Provenance

Observed 2026-10-23 on Linux, Python 3.14.7, molsyssuite@uibcdf_3.14.
Provider HEAD 8ebb1b4d5bec058e3be837a35e29ef649f0a5333, with unrelated PDBQT
work preserved; reviewed RMSF source unchanged. Bundled H5MSM 0.4 warning is
retained. This is source evidence, not installed-artifact qualification.

## Correction in progress — 2026-10-24

Canonical nm reducer outputs are now wrapped with their actual unit and only
then standardized through PyUnitWizard. The physical algorithm, selections,
weights, streaming reduction and session policy are unchanged. A shared physical
length guard covers native Structures and H5MSM 0.5, nm/angstrom/pm policies,
one-/two-structure blocks, repeated/nonconsecutive structure indices, independent
weighted-center/variance references and actual auto-mode chunk consumption.
Before correction, 26 of its 38 cases failed; the focused corrected selection
passes all 46 cases, including existing tool regressions. Wider qualification
and executable documentation are pending.

## Final source qualification — 2026-10-24

The combined length-observable, heavy-execution, sequence-mapping, sequence-form
and conversion-truth selection passed **511 tests** in 35.73 seconds with
`--receptor=llm -n 12`. Three public doctests are included. Network-marked
sequence tests were explicitly excluded; no installed/release matrix was run.
The 66 warnings are 63 expected legacy H5MSM notices and three intentional
memory-pressure observations from tiny test budgets. No test failed or skipped.

The two observable tutorials, unit-safety module 09, large-ensemble cookbook,
sequence-identity tutorial and topology module 13 executed successfully. All
250 selected public docstrings passed fidelity/content validation. The final
fast-gate and Sphinx results are retained in the qualification receipt:
[`native_observable_repairs_20261024.json`](../../../devtools/data/native_observable_repairs_20261024.json).

The primary guard calculates independent weighted-center or variance references
from the actual selected coordinates. Assertions compare physical nm values
under nm/angstrom/pm policies, rather than merely checking labels or shape.
Native and H5MSM 0.5 routes, one-/two-structure chunks, auto activation, repeated
structure order, unchanged input coordinates and unchanged session policy are
covered. The geometry/variance kernels are unchanged; no new scientific-method
attribution boundary is introduced by this unit-conversion repair.
