---
summary: Structures YAML cannot serialize physical quantities in alternate sites
issue: uibcdf/molsysmt#332
status: resolved
opened: 2026-10-05
closed: 2026-10-05
severity: medium
verification: reproduced
area: [form, convert, units]
guard: tests/form/file_structures_yaml/test_alternate_quantity_records.py::test_public_yaml_preserves_alternate_quantity_records
normative:
blocked_by: []
supersedes: []
---

# Structures YAML cannot serialize physical quantities in alternate sites

**Reported:** 2026-10-05 during cross-form alternate-location controls for
uibcdf/molsysmt#329.
**Status:** Resolved; Structures YAML 0.2 uses verified quantity records.

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

## Resolution — 2026-10-05

The Structures YAML writer now emits schema 0.2 with the general PyUnitWizard
QuantityRecord codec for top-level supported quantities and sparse alternate
coordinates/B factors. Each record is bound to its semantic field and canonical
physical unit. The reader verifies the provider's seal and its own field/unit
handshake. It validates site counts, shapes, finite alternate coordinates and
integer index bounds when coordinates establish the axes. Labels and NumPy
scalars have safe YAML representations. Non-finite B factors use the provider's
base64 encoding, preserving the value and unit without inventing geometry.

Schema 0.1 retains its existing negotiated top-level units and label-only site
records. Bare legacy nested geometry has no negotiated unit and is rejected.
Unknown or missing schema versions and malformed records raise FormatError;
no fallback to a session unit is introduced. Migrate a readable 0.1 file by
loading StructuresDict and writing it again. The file-to-file byte-copy route
retains its original version. Durable schema and migration rules are in
[declarative_serialization_forms.md](../../declarative_serialization_forms.md).
MolSys/Topology YAML 0.1, H5MSM, and chemical stores are unchanged. YAML remains
intended for small snapshots, not large ensembles. The existing supported-field
inventory is retained; this does not add thermodynamic serialization fields.

The public PyUnitWizard floor advances from 0.25.0 to 0.28.1, which includes the
quantity-record API and immutable/empty-array fixes. GitHub Release 0.28.1 was
independently verified as published on 2026-10-05. Both recipes, runtime-bearing
environments and controlled CI source are updated. The latter uses the exact
released tag commit `25a4bc2468da4ef3af2a638c0bf068becf2acfb4`; it does not follow
main. Static contract agreement does not qualify a Conda solver or a new MolSysMT
release. This consumer boundary follows uibcdf/molsyssuite#46 and the provisional
codec designed and implemented in uibcdf/pyunitwizard#83 and uibcdf/pyunitwizard#82; no provider
implementation or shared policy is changed.

**Contract-tested and parity-tested:** 107 focused controls pass with an
installed wheel built from the exact PyUnitWizard 0.28.1 tag. The named guard
independently asserts values in angstroms and squared angstroms, site/ID mappings,
occupancies, canonical record fields, unchanged source data and both nm/pm
application policies. A fresh Python reader uses a different unit policy.
Separate controls reject absent/altered units, contradictory SI descriptions,
wrong physical dimensions, wrong field bindings, shapes, scalar labels/IDs,
invalid occupancy, out-of-range indices, missing/unknown versions and bare
values. A bad writer quantity leaves an existing file unchanged. The dictionary
codec preserves a typed empty coordinate tensor; this does not change native
zero-structure materialization, which can represent absent coordinates as None.

The five-form #329 control now uses full YAML geometry instead of its former
label-only workaround. uibcdf/molsysmt#333 fixes source-to-local key remapping in
supported native/dictionary conversions. Native structural, conversion-report,
alternate-conformer and doctest regressions remain green. The run reports four
expected legacy-H5MSM warnings and one existing incompatible-box control warning.
It is not full-suite, performance or published MolSysMT artifact qualification.

Minimum-provider evidence: Python 3.14.7 on Linux x86_64; wheel
`pyunitwizard-0.28.1-py3-none-any.whl`, locally built from the released tag, SHA-256
`cc07be4a0c9cafe60e51cf55796e589fb11786a53173fa1f30e992c6e22fad5d`.
The imported distribution and module both report 0.28.1. Other test inputs are
editable MolSysMT based on `e05c285e3` with this patch and the released ArgDigest
0.13.0 source overlay. These local wheel bytes are not claimed as the published
provider archive bytes.

The public converter docstrings, Foundations, form Toolbox, chemical-template
Cookbook, course module 19 and documentation manifest are updated. Notebook code
and outputs are retained. Ruff, docstrings, dependency/import audits, public
signature stability and the normative 156-notebook course gate pass. Sphinx HTML
compiles with 23 warnings in this incremental build; inherited course markup,
labels and orphan pages remain visible. No warning-free or matched-baseline
warning claim is made.
