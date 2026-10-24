---
summary: Heavy radius of gyration relabels nm values as the active length unit.
issue: uibcdf/molsysmt#440
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

# Heavy radius of gyration changes physical scale under alternate length units

**Reported:** 2026-10-23 during scientific-owner review for the structure tools
addon, uibcdf/molsysmt#421 / uibcdf/molsysviewer#264. Filing explicitly authorized
by the principal maintainer.
**Status:** resolved in native MolSysMT; the addon needs no formula override.


## What

Forced chunking and eager calculation produce different physical lengths in
an active picometer context, even after both outputs are explicitly converted
to nm. The first eager value is 0.11865379536374124 nm; the forced value is
0.00011865379536374126 nm, a factor of 1000 smaller.

```python
import molsysmt as msm
puw = msm.pyunitwizard
molsys = msm.convert(
    msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    structure_indices=[0, 8, 3],
)
with puw.context(standard_units=['pm', 'ps', 'degrees']):
    for mode in ['off', 'force']:
        result = msm.structure.get_radius_of_gyration(
            molsys, selection=[0, 2, 4], structure_indices=[2, 0, 2],
            heavy_mode=mode,
        )
        print(mode, puw.get_value(result, to_unit='nm')[0])
```

## How

The reducer in [get_radius_of_gyration.py](../../../molsysmt/structure/get_radius_of_gyration.py)
computes from chunk coordinates in nm. The heavy return attaches the configured
length unit directly to those numeric values. It needs a correctly attributed
nm quantity followed by unit conversion, rather than relabeling values.

## Why

The physical observable must not depend on processing mode or session display
units. Automatic heavy selection can expose this discrepancy without an explicit
forced request. Other units besides pm need coverage; they are not exhaustively
measured here.

## What was refuted

The same selected structures and atoms are used in both routes, including repeated
and nonconsecutive structures. Explicit conversion of both results to nm retains
the disagreement, so this is not merely different printed units. Native centers
and vectors retain their physical values across the same mode/unit comparison.

## Acceptance criteria

Native eager and heavy values agree after conversion to a common unit for nm,
angstrom and pm contexts, weighted/unweighted selections, and repeated/nonconsecutive
structures. Results obey the native unit policy without modifying coordinates
or session policy. Add a native regression guard protecting actual physical
values rather than checking only the unit label or output shape.

## Scope and exclusions

This is a native MolSysMT defect, reproduced without importing MolSysViewer.
The addon preserves public native options and outputs. It does not silently
rewrite heavy_mode, change standard units, substitute a different algorithm or
claim scientific validation of this affected route. Existing frozen artifacts
and publication pauses are unaffected.

## Provenance

Observed 2026-10-23 on Linux, Python 3.14.7 in molsyssuite@uibcdf_3.14. Provider
HEAD c4b71b2069b3613f0b1e340f7448f645cc80f0b4 with concurrent unrelated PDBQT
work preserved; reviewed geometry sources are unchanged. Tests use bundled
pentalanine, retaining its H5MSM 0.4 legacy-read warning. These are source
observations, not clean installed-artifact qualification.

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
