---
summary: Dihedral editors publish nonfinite coordinates from NaN angular edits.
issue: uibcdf/molsysmt#462
status: open
opened: 2026-10-26
closed:
severity: high
verification: reproduced
area: [structure]
guard:
normative:
blocked_by: []
supersedes: []
---

# Dihedral editors publish nonfinite coordinates from NaN angular edits

**Reported:** 2026-10-26 after maintainer-directed continuation of the prepared
reports from the torsion receiving under uibcdf/molsysmt#421 /
uibcdf/molsysviewer#264. **Status:** reproduced natively; scientific repair pending.

## What

What — Both `structure.set_dihedral_angles()` and `structure.shift_dihedral_angles()` accept NaN angular values and return nonfinite molecular coordinates without a scientific exception. With in_place=True the input MolSys is corrupted; with False the returned independent MolSys is corrupted.

How — Reproduced on the reviewed dihedral source at bb6283ce7, Python 3.14/Linux, without Viewer:
```python
import numpy as np
import molsysmt as msm
p = msm.pyunitwizard
molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'], structure_indices=[0, 8, 3])
quartet = np.asarray(msm.topology.get_dihedral_quartets(molsys, phi=True), dtype=np.int64)[:1]
msm.structure.set_dihedral_angles(molsys, dihedral_quartets=quartet, angles=p.quantity([[np.nan]], 'radians'), structure_indices=[0], pbc=False, in_place=True)
assert np.isfinite(p.get_value(msm.get(molsys, coordinates=True), to_unit='nm')).all()  # fails
```
The equivalent shifter call with `shifts=p.quantity([[np.nan]], 'radians')` also corrupts structure 0. Both methods/modes were measured independently on fresh copies.

## How

Native angular digestion accepts the quantity and the mutation boundary does not reject its nonfinite value before the Rust rotation and coordinate setter. The pure native audit measures both set_dihedral_angles and shift_dihedral_angles, each with in_place=False and True. None raises; every resulting system contains nonfinite coordinates on structure 0. The independent route preserves its input but returns a corrupted result; the in-place route modifies the input.

## Why

The expert addon must delegate native science and preserve native arguments,
units and output ownership. These inputs cannot receive unconditional scientific
qualification. The source wrappers expose their native limits; they contain no
replacement calculation or hidden molecular preparation.

## What is measured and what is assumed

The original source receipt is
[the dihedral receiving record](../../devtools/data/molsysviewer_tools_dihedrals_receiving_20261025.json).
It retains the native-only audit data, raw artifact paths/digests, source hashes
and 61-case valid-route guard. The scientific source files are unchanged at
8511e910d compared with the recorded audit. That valid-route regression does not
certify the failing input. No additional failure modes are asserted from code
inspection alone.

## What was refuted

The defect reproduces without Viewer. The addon does not change blocks, angle
values, PBC or scientific outputs. A successful display or native call is not a
substitute for the scientific value and motion-scope assertions.

## Scope and exclusions

Repair the owning native tools, with standalone pytest guards. General graph
reconstruction, automatic observation of arbitrary MolSys edits, GUI forms,
scientific replay and molecular Undo are outside this report.

## Acceptance criteria

Validate finite edit angles/increments at the owning mutation boundary before coordinate writes. Add native pytest cases for NaN and +/-Inf in scalar/array inputs, degrees/radians, independent/in-place modes, admitted structure selections/broadcasting and PBC/no box. Rejections must preserve coordinates, box, topology and stored interaction coverage, including evaluated-empty results. Retain positive independent quaternion/circular-angle checks for valid inputs. Do not globally forbid nonfinite scientific measurements merely to validate an editing request; read-only undefined-angle semantics are a separate contract.

## Provenance

Linux x86-64, Python 3.14, Conda molsyssuite@uibcdf_3.14, bundled
pentalanine/traj_pentalanine.h5msm, structures [0, 8, 3]. The original audit was
performed during the source receiving recorded on 2026-10-25; filing is on
2026-10-26. Source hashes and original evidence remain in the linked receipt.
No installed package, fresh Rust build or all-platform qualification is claimed.
