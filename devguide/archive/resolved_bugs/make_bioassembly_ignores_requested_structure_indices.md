---
summary: make_bioassembly ignores requested structure indices
issue: uibcdf/molsysmt#401
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: medium
verification: reproduced
area: [build]
guard: tests/build/make_bioassembly/test_structure_selection.py
normative:
blocked_by: []
supersedes: []
---

# make_bioassembly ignores requested structure indices

**Reported:** 2026-10-22 during the public builder checks for uibcdf/molsysmt#396.
**Status:** Resolved on 2026-10-22; the reproduction below describes the original defect.

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

## Resolution — 2026-10-22

**Implemented:** both supported chain-scope branches pass the validated public
`structure_indices` argument to the existing extraction tool. The operations
are then broadcast over the selected resident structures through the existing
rotation/translation tools. Operation copies expand the atom axis; structure
order, repetitions, IDs and times follow the selected source axis. The default
still selects structure 0, and `"all"` selects the complete structure axis.
Invalid explicit indices now reach the existing range checks instead of being
silently replaced by `[0]`.

The public file-input guard also exposed a necessary composition boundary:
H5MSM extraction with no output filename tries to preserve a file form. The
builder now loads file inputs through public conversion to a resident `MolSys`
before assembly construction. It leaves the input file unchanged and honors an
explicit final `to_form`; the default file-input result is resident `MolSys`.
Resident inputs keep their prior routes. Complete H5MSM loading may precede
selection; this is not a new bounded-file or streaming contract.

**Contract-tested:** the new 21-case public guard covers nondefault scalar
indices, nonconsecutive/repeated indices, `"all"`, unchanged default behavior,
common and repeated per-operation scopes, one/multiple selected chains, direct
and stored/default assembly instructions, H5MSM file input with default/explicit
native output, rejected out-of-range indices, and source nonmutation. Structure
labels deliberately differ from index values. Nondefault output units and
Angstrom input translations remain explicit.

**Analytically checked:** expected coordinates are calculated from the selected
source arrays by identity and quarter-turn-plus-translation operations, rather
than comparing two consumers of the same implementation. Metadata and output
axis lengths are checked alongside coordinates. Against the original code,
the initial 16 guards produced 15 failures and one pass: 14 numerical mismatches
and the independently exposed H5MSM file-extraction error. The expanded final
guard supplies additional file-output and range-validation cases.

**Validation:** Linux/Python 3.14.7 in the existing development environment;
12 workers and `pytest-receptor`. The initial integrated selection passed 121
tests with three visible expected warnings. All fourteen fast gates, full-package
Ruff, docstring fidelity and public API drift checks pass; six function doctest
examples pass. The final broad extraction/merge/H5MSM/native-copy/translation/builder campaign
passes **885 tests**, no omissions, in 16.56 s with the same 12-worker receptor
configuration. Its 659 visible warnings comprise 657 expected legacy H5MSM
deprecations and the existing structural-drop/off-axis cases. This does not
qualify an installed release artifact or the full platform/Python matrix. User Guide Foundations, Toolbox, Cookbook and Common Core
Module 12 explain the selected-structure contract. Notebook code cells and saved
outputs are unchanged; no new complete notebook execution is claimed.

No new public signature, scientific criterion, dependency, Rust kernel or file
schema is introduced. This reuses existing general extraction, conversion and
geometry tools; it creates no new scientific attribution execution boundary.
The separate native-copy design work in uibcdf/molsysmt#121 remains active.
