---
summary: Public alternate-location queries stringify atom-index keys as IDs
issue: uibcdf/molsysmt#329
status: open
opened: 2026-10-05
closed:
severity: medium
verification: reproduced
area: [basic, attribute]
guard:
normative:
blocked_by: []
supersedes: []
---

# Public alternate-location queries stringify atom-index keys as IDs

**Reported:** 2026-10-05 during uibcdf/molsysmt#304 peptide-candidate controls.
**Status:** Reproduced; public-query normalization correction remains pending.

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
