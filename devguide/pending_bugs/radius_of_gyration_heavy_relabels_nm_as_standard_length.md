---
summary: Heavy radius of gyration relabels nm values as the active length unit.
issue: uibcdf/molsysmt#440
status: open
opened: 2026-10-23
closed:
severity: medium
verification: reproduced
area: [structure, heavy, units]
guard:
normative:
blocked_by: []
supersedes: []
---

# Heavy radius of gyration changes physical scale under alternate length units

**Reported:** 2026-10-23 during scientific-owner review for the structure tools
addon, uibcdf/molsysmt#421 / uibcdf/molsysviewer#264. Filing explicitly authorized
by the principal maintainer.
**Status:** open; no scientific algorithm or routing fix is added to the addon.


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

The reducer in [get_radius_of_gyration.py](../../molsysmt/structure/get_radius_of_gyration.py)
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
