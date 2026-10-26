---
summary: shift_dihedral_angles ignores explicit moving blocks.
issue: uibcdf/molsysmt#461
status: resolved
opened: 2026-10-26
closed: 2026-10-26
severity: high
verification: reproduced
area: [structure]
guard: tests/structure/test_dihedral_edit_contract.py
normative:
blocked_by: []
supersedes: []
---

# shift_dihedral_angles ignores explicit moving blocks

**Reported:** 2026-10-26 after maintainer-directed continuation of the prepared
reports from the torsion receiving under uibcdf/molsysmt#421 /
uibcdf/molsysviewer#264. **Status:** resolved; native mutation and receiver guards pass.

## What

What — `structure.shift_dihedral_angles()` ignores its public `blocks` input and moves the automatically detected covalent block instead. The equivalent native setter honors the same explicit block.

How — Reproduced on the reviewed dihedral source at bb6283ce7, Python 3.14/Linux, without Viewer:
```python
import numpy as np
import molsysmt as msm
p = msm.pyunitwizard
molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'], structure_indices=[0, 8, 3])
quartet = np.asarray(msm.topology.get_dihedral_quartets(molsys, phi=True), dtype=np.int64)[:1]
blocks = [quartet[0, 2:].tolist()]
angles = msm.structure.get_dihedral_angles(molsys, dihedral_quartets=quartet, structure_indices=[0], pbc=False)
shifted = msm.structure.shift_dihedral_angles(molsys, dihedral_quartets=quartet, shifts='.3 radians', blocks=blocks, structure_indices=[0], pbc=False)
expected = msm.structure.set_dihedral_angles(molsys, dihedral_quartets=quartet, angles=angles + p.quantity(.3, 'radians'), blocks=blocks, structure_indices=[0], pbc=False)
assert np.allclose(p.get_value(msm.get(shifted, coordinates=True), to_unit='nm'), p.get_value(msm.get(expected, coordinates=True), to_unit='nm'))  # fails
```
The explicit block is [8, 14]. The setter moves atom 14; the shifter moves the automatically selected downstream population. Maximum observed coordinate difference: 0.3647040883889531 nm.

## How

The final delegation in molsysmt/structure/shift_dihedral_angles.py supplies blocks=None instead of forwarding the declared input. The public setter honors the same restricted block. The native example uses quartet [4, 6, 8, 14], blocks [[8, 14]] and a 0.3-radian increment; the setter moves only atom 14, while the shifter moves the automatically selected downstream population. The maximum observed discrepancy is 0.3647040883889531 nm.

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

Preserve the explicit block request when delegating. Add native pytest cases with a deliberately restricted block that differs from the automatic graph partition; cover independent/in-place results, automatic blocks, scalar/multiple quartets and structures where admitted, angular units, PBC/no box and untouched atoms/structures/box/topology/interaction coverage. Assert achieved circular torsions independently and document the actual block container contract. Keep errors and empty/invalid inputs explicit rather than silently choosing automatic blocks.

## Provenance

Linux x86-64, Python 3.14, Conda molsyssuite@uibcdf_3.14, bundled
pentalanine/traj_pentalanine.h5msm, structures [0, 8, 3]. The original audit was
performed during the source receiving recorded on 2026-10-25; filing is on
2026-10-26. Source hashes and original evidence remain in the linked receipt.
No installed package, fresh Rust build or all-platform qualification is claimed.


## Resolution — 2026-10-26

The public functions retain their signatures and existing Rust rotation kernel.
A private editing boundary validates real finite angular values and broadcast
shapes, distinct in-range quartets and nonempty in-range block pools. It does
not impose finite-only semantics on read-only measurements. An undefined input
geometric angle can still be measured as NaN; an edit that would produce
nonfinite moving coordinates is rejected before publication. The setter works
on an independent selected-coordinate buffer, and the shifter forwards explicit
blocks unchanged. Each quartet uses the union of supplied blocks containing its
fourth atom. Automatic covalent blocks remain owned by the existing topology tool.

The native guard initially fails 168 cases and passes 72: 144 nonfinite-request
cases and 24 explicit-block shift cases expose the two reported defects. The
expanded guard adds malformed inputs, coordinate-only forms, undefined geometry,
block-pool union semantics and input/analysis preservation. The receiver now
checks both explicit editors and nonfinite rejections without scene damage.

The final local regression passes **3,092 tests**, zero failures or skips, in
63.06 seconds using twelve workers and Pytest Receptor. One unrelated neighbor
test performs an undeclared remote 5XJH download; the initial broad run fails
that case with unavailable DNS, and it is explicitly deselected from the local
qualification, not counted as passed. That test limitation is tracked by
uibcdf/molsysmt#469. Two doctests and all three updated tutorial/course notebooks
pass. A post-execution schema run validates all 491 documentation notebooks.
The four legacy Path 27 conformational examples have a separate API-mismatch
report, uibcdf/molsysmt#468; this repair does not qualify those workflows.

The [receipt](../../../devtools/data/dihedral_edit_repair_20261026.json) records
commands, versions, source hashes, failures and bounded outcomes. The standalone
native guard is included in the hosted and local smoke selections. Foundations,
Toolbox, Cookbook and Common Core Module 16 describe finite requests, block-pool
semantics and scoped interaction invalidation. No tag, package promotion or
release qualification is performed.

Ruff lint/format, all 251 public docstring contracts, zero unauthorized signature
drifts and the fourteen fast gates pass. Incremental Sphinx HTML exits zero with
zero errors and 63 retained warnings; broad warning cleanup remains under
uibcdf/molsysmt#144. This does not qualify the skipped remote fixture or a new
installed/public package.

The final receiver check overlays the exact staged addon files in the same
development interpreter, excluding concurrent PBC receiving changes. All 71
receiver cases pass in 30.24 seconds with no skips; loaded-module paths and
source hashes are recorded. This is source isolation, not an auxiliary environment
or installed distribution qualification.
