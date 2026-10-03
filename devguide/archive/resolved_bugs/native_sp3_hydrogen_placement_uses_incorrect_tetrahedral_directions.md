---
summary: Native sp3 hydrogen placement uses incorrect tetrahedral directions
issue: uibcdf/molsysmt#306
status: resolved
opened: 2026-10-03
closed: 2026-10-03
severity: high
verification: reproduced
area: [build, structure]
guard: tests/build/test_native_placers.py::test_sp3_one_neighbor_has_analytic_tetrahedral_angles
normative:
blocked_by: []
supersedes: []
---

# Native sp3 hydrogen placement uses incorrect tetrahedral directions

**Reported:** 2026-10-03 while reviewing reusable placement tools for #300.
**Status:** Resolved; independent tetrahedral and legacy regression checks pass.

## What

`build._native_placers.place_hydrogens_on_parent` places one-neighbor sp3 H on a
cone giving parent-neighbor-H angles of 160.5 degrees rather than the ideal
109.4712206 degrees. The isolated sp3 four-H branch produces a planar square
rather than a tetrahedron. Reproduction on the pre-fix source:

```python
import numpy as np
from molsysmt.build._native_placers import place_hydrogens_on_parent
parent = np.zeros((1, 3))
neighbor = np.array([[.15, 0., 0.]])
h = np.asarray(place_hydrogens_on_parent(parent, [neighbor], 3, 'sp3', .109, 1))[:, 0]
print(np.degrees(np.arccos(h[:, 0] / np.linalg.norm(h, axis=1))))
# Before: [160.5 160.5 160.5]; after: [109.47122063 109.47122063 109.47122063]
```

## How

The axis `vAP = normalize(P - A)` points away from the neighbor. Its cone angle
must be `arccos(1/3)`, so its dot product with the actual parent-to-neighbor
vector is -1/3. The original `109.5 - 90` degree cone angle exchanges the axial
and transverse weighting. Correct the one-neighbor branches for one, two and
three added H, preserving the established azimuthal convention. For isolated
sp3 centers with up to four H, use unit tetrahedron vertices, whose pairwise dot
products are -1/3. Other isolated hybridizations retain the previous distribution.

## Why

The helper is used by the native amino-acid/capping hydrogen-addition engine.
Counts and nominal bond lengths can be correct while directional donor or local
steric geometry is wrong. #300 must not inherit this error when considering a
future native ligand engine; its first RDKit route has independent geometry checks.

## What is measured and what is assumed

**Reproduced:** The command above gives three 160.5 degree angles on the pre-fix
source. The isolated four-H pair cosines are approximately [0, -1, 0, 0, -1, 0].

**Scientifically validated, bounded:** Four new parametrized analytic checks verify
bond length and -1/3 products, including two frames and a rotated neighbor axis,
for one-neighbor sp3 H counts 1/2/3 and isolated four-H geometry. The existing
native-placement and pH-engine regressions pass in the joint 199-test run.
This does not validate every hydrogen geometry branch or receptor orientation.

## What was refuted

- Bond-length and atom-count checks cannot detect the incorrect cone angle.
- 19.5 degrees is not the required tilt around the away-from-neighbor axis.
- An evenly spaced planar distribution is not tetrahedral for four H.

## Scope and exclusions

Correct these existing ideal-sp3 directions. Do not introduce a new protonation
model, engine, energy minimization, receptor refinement or universal native ligand
support. Other degenerate/fallback placement branches are not certified here.

## Acceptance criteria

The addressable guard above and
`tests/build/test_native_placers.py::test_sp3_isolated_four_hydrogens_form_analytic_tetrahedron`
must fail on the original directions and pass on the correction. Existing native
hydrogen-addition regressions must retain their chemistry/count contracts.

## Provenance

2026-10-03, local Linux x86_64 checkout, Python 3.13.14, NumPy 2.4.6. The released
ArgDigest 0.13.0 source snapshot is used through the documented test PYTHONPATH.
Local interpreter deviation is tracked by uibcdf/molsysmt#237 and does not certify
Python 3.14 or a platform matrix. Joint command:

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
  tests/build/add_missing_hydrogens tests/build/test_native_placers.py \
  tests/build/add_terminal_atoms tests/physchem/get_hydrogen_inventory \
  tests/physchem/test_chemical_template.py tests/physchem/test_chemical_template_est.py \
  tests/physchem/test_get_chemical_readiness.py tests/physchem/test_get_cip_stereochemistry.py \
  tests/test_ackredit.py
```

Final joint run: **209 passed, 67.07 s**, including the addressable guards and all legacy hydrogen-addition tests. Later preparation-only controls do not change this geometric correction.
