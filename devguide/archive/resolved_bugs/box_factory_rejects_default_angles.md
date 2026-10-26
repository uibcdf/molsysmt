---
summary: Box factory rejects its declared default angles.
issue: uibcdf/molsysmt#465
status: resolved
opened: 2026-10-26
closed: 2026-10-26
severity: medium
verification: reproduced
area: [pbc, api]
guard: tests/pbc/get_box_from_lengths_and_angles/test_get_box_from_lengths_and_angles.py
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
[receiving receipt](../../../devtools/data/molsysviewer_tools_pbc_receiving_20261026.json)
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

## Resolution — 2026-10-26

The box-angle digester permits None only for the public box factory; it remains
invalid for unrelated contracts requiring angles. The factory builds a shared
orthogonal triple, broadcasts it to length rows, and checks explicit row counts
before Rust. This also repairs the one-dimensional default reaching a kernel
requiring two dimensions. Shared and per-structure explicit angular quantities
normalize to radians without requiring an unrelated application angle standard.
The output follows the active length standard and always retains the structure
axis, including single/empty boxes. Six-decimal-nanometer precision is unchanged.

The pre-fix selected baseline has eight default/None failures and two invalid
input controls passing. During repair, explicit angles under length/time-only
policies additionally exposed unnecessary angle-standard lookup; the factory's
canonical-radian boundary fixes that measured path without changing other
angle consumers. The final 28-case guard covers omitted/None/degree/radian
angles, one/multiple rows, shared/per-structure triclinic geometry, nm/pm output,
raw-nanometer and empty lengths, invalid dimensions/shape/counts, and the
unrelated required-angle rejection. Analytic matrices provide the oracle.

Docstrings and the box tutorial document shapes, units and broadcasting. The
membrane course reconstructs its actual orthogonal cells with the default;
[native structural rules](../../native_structures_contract.md) retain the boundary.

## Qualification receipt — 2026-10-26

The integrated PBC/centering/translation/dictionary/argument/documentation
selection passes **1,121 tests** in 45.92 seconds with `--receptor=llm -n 12`,
without skips (13 intentional legacy-H5MSM warnings). Four source modules pass
all 27 doctest examples. All five modified executable notebooks run successfully.
The Cookbook change is explanatory prose; its pre-existing solvation workflow
was not newly executed. Ruff and format checks, 251-function docstring validation
and all fourteen fast repository gates pass. Incremental Sphinx HTML completes
without errors and with 29 existing heading/toctree warnings; no warning-free
full build or installed release qualification is claimed.

Commands, environment, tested source hashes, fixture bindings and limitations
are retained in the [PBC repair receipt](../../../devtools/data/pbc_repairs_20261026.json).
