---
summary: Public alternate-location queries stringify atom-index keys as IDs
issue: uibcdf/molsysmt#329
status: resolved
opened: 2026-10-05
closed: 2026-10-05
severity: medium
verification: reproduced
area: [basic, attribute]
guard: tests/basic/get/test_alternate_location_indices.py::test_public_alternate_location_preserves_source_atom_indices
normative:
blocked_by: []
supersedes: []
---

# Public alternate-location queries stringify atom-index keys as IDs

**Reported:** 2026-10-05 during uibcdf/molsysmt#304 peptide-candidate controls.
**Status:** Resolved; source atom-index keys remain integers in public queries.

## What

Native alternate-location mappings use source atom-index keys. The public getter
turns those integer keys into strings while normalizing the entries' atom IDs:

```python
import numpy as np
import molsysmt as msm
from molsysmt.native import MolSys, Structures
molsys = MolSys(n_atoms=3)
molsys.structures = Structures(
    coordinates=msm.pyunitwizard.quantity(np.zeros((1, 3, 3)), 'nm'),
    alternate_location=[{2: {'location_id': np.array(['A', 'B']),
                             'atom_id': np.array([10, 11]),
                             'occupancy': np.array([0.5, 0.5]),
                             'b_factor': msm.pyunitwizard.quantity(np.zeros(2), 'nm**2'),
                             'coordinates': msm.pyunitwizard.quantity(np.zeros((2, 3)), 'nm')}}])
print(list(molsys.structures.alternate_location[0]))  # [2]
print(list(msm.get(molsys, alternate_location=True)[0]))  # ['2']
```

The observed #304 endpoint at source atom index 2 was consequently missed by an
integer-key membership check using this getter. The supported form iterator
returns the integer key and correctly blocks that alternate-backbone candidate.

## How

`basic.get._coerce_alternate_location_ids()` copies each mapping into
`new_struct[str(key)]`. The key is an atom index, not an atom ID. IDs inside each
entry must still be strings. Existing StructuresDict and structures-YAML tests
expect the incorrect string key and need semantic correction with this fix.

## Why

Clients joining coordinates or chemistry by source atom indices can overlook
alternate conformations or join the wrong type of axis. This conflicts with the
native index/ID distinction and differs from supported form iterators. Reported
medium severity because the scientific downstream failure depends on using the
public getter and an integer-key comparison.

## What is measured and what is assumed

**Reproduced:** native mapping key 2 becomes '2' in the public getter, while
entry atom IDs become strings as intended. A peptide control found a candidate
before switching its geometry read to the existing source-preserving iterator.
**Inspected:** `new_struct[str(key)]` in the normalizer explains the change.
No exhaustive affected-format inventory or external consumer failure is claimed.

## What was refuted

The PDB parser did retain the alternate site. The issue is public-query key
normalization, not missing PDB evidence or H5MSM persistence.

## Scope and exclusions

Correct source-index keys in public alternate-location results; keep entry IDs
as strings, detached copies and selected structure/atom behavior. This does not
change alternate-conformer selection or the stored H5MSM schema.

## Acceptance criteria

Add a failing public-query guard for native, dictionary, YAML and H5MSM forms;
assert integer source-index keys, string entry IDs, selected-axis correspondence
and unchanged stored data. Update expectations that protect the old defect and
user documentation, then close with a concrete guard selector.

## Provenance

Linux x86_64, 2026-10-05, Python 3.14.7, NumPy 2.4.6 and released ArgDigest 0.13.0
source overlay. Source is based on `c2f16cbc2` plus #304 candidate work; this is
editable-source evidence, not installed-release qualification.

## Resolution — 2026-10-05

The public getter copies each sparse mapping and entry while retaining the
source atom-index key. Only `atom_id` labels are normalized to strings. Existing
dictionary, YAML, deposited PDB and alternate-conformer controls now assert the
integer-index contract instead of preserving the former defect. No stored
coordinates, alternate-site arrays or H5MSM schema are rewritten.

**Contract-tested and parity-tested:** 147 focused controls pass, including the
public getter doctest, native Structures/MolSys, StructuresDict, label-only YAML,
H5MSM 0.5, real PDB alternate sites, alternate-conformer resolution and the #304
peptide report. The named guard independently specifies keys `[4]`, `[2]`, `[4]`
and an empty dictionary for a nonconsecutive repeated structure selection. It
also verifies string IDs, geometry/units when supported, unchanged stored data
and independent edits to returned mappings/ID lists. Empty selections and absent
evidence have separate controls. General numeric buffers are not promised as
independent copies.

These controls exposed two distinct defects: uibcdf/molsysmt#331's system-level
structure selection is corrected in this checkpoint; uibcdf/molsysmt#332's YAML
physical-quantity persistence remains pending. The YAML index guard explicitly
uses optional coordinate/B-factor fields set to None and does not claim that
pending roundtrip. Sixteen warnings remain visible: fifteen expected legacy
H5MSM deprecation warnings and one existing pandas setter FutureWarning.

The public docstring, Toolbox, Foundations, chemical-template Cookbook and
Common Core module 8 now explain source indices versus site IDs. Notebook code
and saved outputs are unchanged. No full suite, installed-file qualification,
performance benchmark or complete legacy-format inventory is claimed.

Validation also passes Ruff, the current normative course gate
(`devtools/scripts/validate_course.py`: 156 notebooks), docstring validation,
public-signature stability and developer-guide integrity. Sphinx HTML compiles
with 30 warnings in this incremental build, including legacy course heading
levels, an unknown key-takeaway directive, existing admonition syntax and the
undefined user-foundations label. The changed notebooks retain that preexisting
markup. Incremental builds read different page sets; the prior checkpoint's
27 warnings do not establish a matched warning baseline. This does not claim
a warning-free build or zero new warning messages.
