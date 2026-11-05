---
summary: make_water_box places oxygen sites outside the requested triclinic cell.
issue: uibcdf/molsysmt#564
status: open
opened: 2026-11-04
closed:
severity: high
verification: reproduced
area: [build, pbc, tests]
guard:
normative:
blocked_by: []
supersedes: []
---

# Water-box oxygen sites fall outside the requested triclinic cell

**Reported:** 2026-11-04 while reviewing the remaining expert-addon factories
under uibcdf/molsysviewer#264. The maintainer authorizes the native report.
**Status:** open; the scientific owner must review and correct the native builder.

## What

The native `make_water_box` advertises triclinic support but returns 111 oxygen
sites outside the requested cell among 266 generated waters. A 2 nm orthogonal
control returns 268 waters with zero out-of-cell oxygen sites. The stored box
agrees with the requested row-vector matrix. No Viewer or addon call is needed.

```python
import numpy as np
import molsysmt as msm

puw = msm.pyunitwizard
for name, B in [
    ('orthogonal', 2*np.eye(3)),
    ('triclinic', np.array([[2., 0., 0.], [.7, 1.8, 0.], [.3, .2, 1.7]])),
]:
    molsys = msm.build.make_water_box(puw.quantity(B, 'nm'))
    oxygen = puw.get_value(
        msm.get(molsys, selection="atom_type=='O'", coordinates=True),
        to_unit='nm',
    )[0]
    fractional = oxygen @ np.linalg.inv(B)
    outside = np.any((fractional < -1e-12) | (fractional >= 1+1e-12), axis=1)
    print(name, len(oxygen), int(outside.sum()))
    np.testing.assert_array_equal(
        puw.get_value(molsys.structures.box, to_unit='nm')[0], B,
    )
# orthogonal 268 0
# triclinic 266 111
```

The triclinic fractional minima are approximately
`[-0.35121502, -0.10322059, 0.00766471]`; maxima are
`[0.88991629, 1.24475392, 1.09295882]`. These violations are much larger than the
explicit 1e-12 fractional tolerance. Fractional coordinates are dimensionless;
all Cartesian data and box vectors above are explicitly converted to nm.

## How

`molsysmt/build/make_water_box.py` unpacks the matrix as
`a_vec, b_vec, c_vec = box_matrix`, declaring row vectors. It clips oxygen sites
using `inv_box @ coors_Os.T`, instead of fractional coordinates consistent with
that row convention, and checks only an upper bound. These inspected mechanisms
need owner review; the public coordinate violation is independently reproduced.
The existing native test exercises only an orthorhombic cell.

## Why

Solvent construction can retain wrong cell membership and alter the resulting
population or geometry for triclinic preparation. This affects native scientific
output, not rendering. The issue carries `component:molsysviewer` because addon
factory qualification exposed the limitation; the correction belongs to MolSysMT.
`make_water_box` remains unexposed by the addon. The received terminal-attachment
and heavy-atom-repair wrappers do not depend on it.

## What is measured and what is assumed

Measured: public oxygen coordinates, requested/stored box equality, population,
fractional extrema and out-of-cell counts for the two declared inputs. The
function bytes also match the current owner checkout. Likely cause: the clipping
orientation and missing lower bound identified above. No expected equilibrium
water population, density or packing quality is inferred from this experiment.

## What was refuted

An orthogonal-only failure is refuted by the zero-violation control. Hydrogen
positions extending across a periodic boundary are not counted; only O sites
are checked. Viewer selection, rendering and edit synchronization are absent
from the reproduction. No consumer wrapping or scientific workaround is used.

## Scope and exclusions

This report concerns the native requested-cell membership contract. It does not
qualify a water force field, general solvation, minimization, equilibration,
all triclinic geometries or installed artifacts. No native algorithm change is
authored in the receiving addon contribution.

## Acceptance criteria

The owner should add pytest guards with independent expected fractional
coordinates for skewed cells and both bounds, including nondefault length units
and the passing orthogonal control. Preserve complete three-point molecules and
row-vector box/unit semantics. A relevant mechanically addressable native guard
and durable resolution are required before closing the issue. Any packing or
boundary policy beyond that contract must be explicit rather than inferred.

## Provenance

Native owner basis `5f3af9374f2bf4ce9c3598450e22d43ca14509ae`, consumed from PR
#543 source `32435e6fd300e1753c6d843cb100aaabfc44787e`. Python 3.14.7, NumPy
2.4.6 and PyUnitWizard 0.28.1+15.g6c62ca6 in the existing Linux source environment.
The function SHA-256 is
`87b5c776c30d5c02f36c5a81ce26a1351340f72c4725a3a3f895f7969eb1fd8b`.
Raw probe evidence is retained in Viewer `.pytest_cache` through owner/CI
receiving, with resource review by 2026-11-11. No package or candidate is qualified.
