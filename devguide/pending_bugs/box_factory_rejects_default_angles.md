---
summary: Box factory rejects its declared default angles.
issue: uibcdf/molsysmt#465
status: open
opened: 2026-10-26
closed:
severity: medium
verification: reproduced
area: [pbc, api]
guard:
normative:
blocked_by: []
supersedes: []
---

# Box factory rejects its declared default angles

**Reported:** 2026-10-26, authorized by the principal maintainer after PBC addon receiving.

## What

The public call rejects its declared `box_angles=None` default:

```python
import molsysmt as msm
puw = msm.pyunitwizard
msm.pbc.get_box_from_lengths_and_angles(puw.quantity([2, 3, 4], 'nm'))
# ArgumentError: Error in argument 'box_angles' with value 'None'.
```

Supplying `puw.quantity([90, 90, 90], 'degrees')` succeeds and produces
shape `(1, 3, 3)` with the expected diagonal in nm.

## How

The public `box_angles` digester rejects None before the native function's
orthogonal-box default can execute. Source inspection also finds an outdated
single-box return-shape description. No additional failure after bypassing
validation is asserted here.

## Why

The addon under uibcdf/molsysviewer#264 must preserve native defaults and may
not silently supply scientific inputs. Its explicit-angle route passes local
independent geometry receiving; the default remains unqualified. The source
implementation and repair belong to MolSysMT, independently of Viewer.

## What is measured and what is assumed

The native-only audit `/tmp/msv-pbc-native-audit.json` is preserved by the dated
[receiving receipt](../../devtools/data/molsysviewer_tools_pbc_receiving_20261026.json)
with digest, observed outputs and native source hashes. Explicit-angle, shape
factory and nonorthogonal-classifier controls succeed. Thirty-three addon
cases and the 1,077-case scoped regression do not certify this failing default.

## What was refuted

The exception occurs without Viewer and before any scene update. Supplying
explicit valid angles works; the wrapper is not a substitute scientific fix.

## Scope and exclusions

Default-angle construction and accurate shape documentation. Keep explicit
angles, quantities, public validation and native output ownership intact.

## Acceptance criteria

Make the public declared default executable for one and multiple structures;
add pytest cases for omitted/None/explicit orthogonal and triclinic angles,
units, supported structure axes and invalid inputs. Correct the output-shape
contract. Guards must execute the real native public boundary, not insert
right angles in the addon or force skipped digestion.

## Provenance

Python 3.14/Linux, explicit `molsyssuite@uibcdf_3.14` interpreter, isolated
source c7fb92a62 plus the received addon changes; native PBC hashes agree with
integrated provider 9061e2149. No native scientific correction is made here.
