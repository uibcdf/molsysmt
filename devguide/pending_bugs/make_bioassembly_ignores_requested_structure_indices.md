---
summary: make_bioassembly ignores requested structure indices
issue: uibcdf/molsysmt#401
status: open
opened: 2026-10-22
closed:
severity: medium
verification: reproduced
area: [build]
guard:
normative:
blocked_by: []
supersedes: []
---

# make_bioassembly ignores requested structure indices

**Reported:** 2026-10-22 during the public builder checks for uibcdf/molsysmt#396.
**Status:** Open; confirmed independently of the assembly normalization repair.

## What

`make_bioassembly(..., structure_indices=[1])` silently builds from structure 0.
An identity operation should reproduce the requested structure. This local,
deterministic probe uses the existing two-structure native test fixture:

```python
import numpy as np
import molsysmt as msm
from tests.native.test_molsys import build_minimal_molsys

molsys = build_minimal_molsys(2)
operation = {
    "chain_indices": [0, 1], "rotations": [np.eye(3)],
    "translations": [msm.pyunitwizard.quantity([0., 0., 0.], "nm")],
}
assembled_molsys = msm.build.make_bioassembly(
    molsys, bioassembly=operation, structure_indices=[1],
)
print(msm.pyunitwizard.get_value(
    assembled_molsys.structures.get_coordinates(), to_unit="nm",
)[0, 0])
```

Observed `[0., 1., 2.]` nm; expected `[12., 13., 14.]` nm from structure 1.

## How

**Inspected:** both extraction branches in
`molsysmt/build/make_bioassembly.py` hardcode `structure_indices=[0]` instead
of using the already validated public argument. Rotation and translation
normalization cannot recover the discarded structure selection.

## Why

A caller receives scientifically incorrect source coordinates while the call
appears successful. A nondefault structure selection is required to expose it;
default first-structure assembly is unaffected by this particular defect.

## What is measured and what is assumed

**Reproduced:** Linux/Python 3.14.7 in the existing development environment on
2026-10-22, based on `de0e8654858593c91fa161ca95127c1c8f7ab049` with the #396
normalizer and consumer corrections in progress. An identity operation on the
synthetic two-structure fixture returns structure 0 after requesting structure 1.
Multiple/repeated/nonconsecutive selections have not been qualified here.

## What was refuted

- A periodic-image or rotation error: the probe uses identity rotation, zero
  translation and no periodic reconstruction.
- An H5MSM read error: the fixture is resident and no file is involved.

## Scope and exclusions

Honor the public structure selection through assembly extraction and geometry.
Preserve the current heterogeneous-chain-set limitation and chain naming policy.
Do not change general rotation or translation semantics to repair this caller.
This record supplies no implementation or release qualification.

## Acceptance criteria

- Identity operations preserve selected source coordinates and order for a
  single nondefault index and nonconsecutive/repeated structure indices.
- Nonidentity operations transform every selected structure correctly.
- Common chain scope and repeated per-operation scope use the same selection.
- A public regression guard fails against the current hardcoded first index.

## Provenance

The reproduction runs from the repository root with the bundled native test
fixture and NumPy/PyUnitWizard, without external data or a new environment.
