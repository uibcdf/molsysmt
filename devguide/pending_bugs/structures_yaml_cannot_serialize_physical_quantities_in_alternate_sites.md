---
summary: Structures YAML cannot serialize physical quantities in alternate sites
issue: uibcdf/molsysmt#332
status: open
opened: 2026-10-05
closed:
severity: medium
verification: reproduced
area: [form, convert, units]
guard:
normative:
blocked_by: []
supersedes: []
---

# Structures YAML cannot serialize physical quantities in alternate sites

**Reported:** 2026-10-05 during cross-form alternate-location controls for
uibcdf/molsysmt#329.
**Status:** Reproduced; a unit-preserving YAML alternate-site boundary is pending.

## What

A valid sparse alternate-site record containing a coordinate quantity fails in
public conversion to `file:structures_yaml`:

```python
import numpy as np
import molsysmt as msm
from molsysmt.native import Structures
molsys = Structures(coordinates=msm.pyunitwizard.quantity(np.zeros((1, 1, 3)), 'nm'))
molsys.alternate_location = [{0: {
    'location_id': np.array(['A', 'B']), 'atom_id': ['10', '11'],
    'occupancy': None, 'b_factor': None,
    'coordinates': msm.pyunitwizard.quantity(np.zeros((2, 3)), 'nm'),
}}]
msm.convert(molsys, to_form='file:structures_yaml', output_filename='alternate.yaml')
# AttributeError: Magnitude 'float' does not support tolist.
```

The original five-form control included both alternate coordinates and B-factor
quantities and failed for the same serializer route. Label-only entries with
`coordinates=None` and `b_factor=None` remain queryable. The #329 YAML control
explicitly uses that narrower supported case and does not claim physical
alternate-site persistence.

## How

`form/molsysmt_StructuresDict/to_file_structures_yaml.py::_to_builtin()` calls
`tolist()` on any nested object exposing that method. A quantity is recursively
expanded into scalar quantities rather than a unit-bearing serialized record.
The top-level coordinate/B-factor serialization path uses explicit fixed units,
but nested alternate sites do not have a negotiated unit boundary. The reader
passes the nested payload through without quantity reconstruction.

## Why

Alternate-site evidence commonly contains coordinates and B-factors. Saving it
cannot safely discard units or depend on the current session unit policy. This
prevents YAML persistence of that scientific evidence, independently of #329's
index/ID normalization defect.

## What is measured and what is assumed

**Reproduced:** the minimal public example above raises the scalar-quantity
`tolist()` AttributeError; the richer cross-form fixture also fails.
**Inspected:** nested quantities bypass the top-level fixed-unit codec.
No changed schema, successful physical roundtrip or exhaustive NumPy-scalar key
support is claimed.

## What was refuted

The getter key-type correction does not repair YAML writing. Removing quantities
from the fixture demonstrates label-only support; it is not a repair for the
scientific persistence defect.

## Scope and exclusions

Define and implement explicit unit-bearing alternate-site serialization and
reading, including integer atom-index keys. Preserve label-only legacy YAML
records. Do not infer units from bare nested values or session defaults.
Other molecular file formats and alternate-conformer selection are separate.

## Acceptance criteria

A public YAML roundtrip must preserve sparse keys, string atom IDs, selected
structure/atom correspondence, alternate coordinates and B-factors. Exercise
nondefault application units and verify wrong/missing/contradictory serialized
units fail with clear diagnostics. Use an existing general quantity codec when
appropriate rather than a parallel chemical store. Define a compatible schema
migration before changing the existing version-0.1 payload.

## Provenance

Linux x86_64, 2026-10-05, Python 3.14.7, NumPy 2.4.6, released ArgDigest 0.13.0
source overlay. Reproduced against editable source based on `bac92dcdb` with the
#329 getter correction. Installed producer metadata reports
`0.22.4+60.g7a8350f76.dirty`; that metadata is not rewritten as source qualification.
