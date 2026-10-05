---
summary: Structural conversions retain source alternate-site keys after atom selection
issue: uibcdf/molsysmt#333
status: resolved
opened: 2026-10-05
closed: 2026-10-05
severity: medium
verification: reproduced
area: [form, convert]
guard: tests/form/molsysmt_StructuresDict/test_alternate_remapping.py::test_selected_conversion_remaps_alternate_atom_indices
normative:
blocked_by: []
supersedes: []
---

# Structural conversions retain source alternate-site keys after atom selection

**Reported:** 2026-10-05 during uibcdf/molsysmt#332 YAML quantity roundtrips.
**Status:** Resolved; supported conversions use the owning native remapping helper.

## What

A native Structures to StructuresDict conversion with selected atoms slices the
coordinate axis but leaves sparse alternate-site keys in the source atom domain:

```python
import numpy as np
import molsysmt as msm
from molsysmt.native import Structures
molsys = Structures(coordinates=msm.pyunitwizard.quantity(np.zeros((1, 5, 3)), 'nm'))
molsys.alternate_location = [{4: {'location_id': ['A']}}]
selected = msm.convert(molsys, to_form='molsysmt.StructuresDict', selection=[4, 2])
print(selected['coordinates'].shape)  # (1, 2, 3)
print(list(selected['alternate_location'][0]))  # observed [4], expected [0]
```

## How

The native/dictionary converters reuse source-index getters to retrieve the
selected sparse mappings. Query filtering is correct, but creating a new object
also requires an atom-axis remap. The inverse dictionary-to-native converter
had the same missing step. Native `Structures.extract` already owned the correct
algorithm. It is factored into one private native helper and reused by both
converters; no YAML-specific index algorithm or competing structural store is
introduced. Only keys are remapped; site arrays and IDs do not need coordinate
copies or relabeling.

## Why

An alternate-site key can fall outside the selected coordinate axis, or point to
a different selected atom. A new serializer must reject such a malformed domain,
not persist it as if it were valid. This differs from uibcdf/molsysmt#329: an
ordinary query deliberately preserves source keys; a conversion creates local
indices.

## What is measured and what is assumed

**Reproduced:** a five-atom source converted with selection [4, 2] retains key 4
beside two-atom coordinates. Source-based public query behavior is independently
specified by #329's guard.
**Inspected:** missing remapping in both conversion directions.
No exhaustive external-form audit or performance measurement is claimed.

## Scope and exclusions

Correct supported native/dictionary structural conversions and their YAML writer
route; retain native extraction behavior. Structure order and repeated indices
remain aligned. Direct selected StructuresDict-to-StructuresDict extraction is
still explicitly unimplemented; this checkpoint does not introduce that separate
capability. Native zero-structure materialization conventions are unchanged.

## Acceptance criteria

`tests/form/molsysmt_StructuresDict/test_alternate_remapping.py::test_selected_conversion_remaps_alternate_atom_indices`
independently specifies local keys [1], [0], [1] and coordinate values for source
atoms [4, 2] and structures [1, 0, 1], across supported native/dictionary routes.
Source queries still return keys 4 and 2. YAML roundtrip controls also test the
local keys, selected coordinates, ID labels and empty structures.

## Provenance

Linux x86_64, 2026-10-05, Python 3.14.7, NumPy 2.4.6. Source based on `e05c285e3`
plus #332 work. Focused controls use the released ArgDigest 0.13.0 source overlay
and an installed wheel built from the exact PyUnitWizard 0.28.1 tag. They do not
qualify a released MolSysMT artifact or a complete platform matrix.

## Resolution — 2026-10-05

The existing native extraction algorithm is factored into
`_remap_alternate_atom_indices` and reused by both supported native/dictionary
converters. Native extraction still copies its selected data before remapping;
converters introduce only local key mappings and retain their prior array-copy
behavior. Ordinary public queries continue to preserve source indices.

The named guard independently specifies source coordinates and local sparse
keys for reordered atoms and nonconsecutive repeated structures, across the
native-to-native, native-to-dictionary and dictionary-to-native routes. #332's
public selected YAML roundtrip adds an empty structure and checks site geometry
and structure ID order. The combined 107-control checkpoint includes native
structural and conversion-report regressions and uses installed PyUnitWizard
0.28.1. No performance benchmark, complete platform matrix or selected
StructuresDict-to-StructuresDict extraction support is claimed.

The public converter notes and Structures YAML/Foundation/Cookbook/course
material distinguish query source indices from conversion local indices. Ruff,
dependency contract/import audits, docstrings, signature and course gates pass.
Sphinx HTML compiles with 23 reported incremental warnings; inherited warnings
are not suppressed or represented as a warning-free build.
