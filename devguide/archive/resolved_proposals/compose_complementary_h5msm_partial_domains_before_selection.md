---
summary: Compose complementary H5MSM partial domains before selections
issue: uibcdf/molsysmt#309
status: resolved
opened: 2026-10-03
closed: 2026-10-03
verification: measured
area: [basic, convert, form]
guard: tests/basic/convert/mult_to_one/test_convert_complementary_h5msm_domains.py
normative:
blocked_by: []
supersedes: []
---

# Compose complementary H5MSM partial domains before selections

**Reported:** uibcdf/molsysviewer#151; provider issue uibcdf/molsysmt#309.
**Status:** Implemented and contract-tested on the public conversion boundary.

## What

Public `msm.convert([topology_chemistry_file, structures_file])` must compose
complementary H5MSM 0.5 inputs before atom or structure selections. A supplied list
declares positional correspondence, as for existing chemical/structural composition.
It does not prove origin or infer atom alignment from equal counts.

## How

Inspect actual native domains and H5MSM 0.5 axis metadata during classification.
The form-wide topology declaration cannot classify a Structures-only file as a
second topology. Metadata inspection does not materialize coordinates or analysis
columns. Legacy forms retain their existing classification routes.

The conversion boundary materializes supported files with their ordinary native
reader, validating each file's internal associations. A private general composer
joins partial native MolSys domains before conversion/extraction. Require one
provider for each topology, chemistry and Structures domain; combine disjoint named
analyses and reject repeated names. Validate full atom/frame axes before selection,
preserve existing state associations and unknown states, and copy topology for its
single-owner invariant. A full-axis `copy_if_all=False` may share structures, but
cannot attach one topology to another owner. MolecularMechanics is rejected rather
than lost on this bounded partial-domain route.

## Why

MolSysViewer needs one-system loading from complementary files and must delegate
scientific domain composition to MolSysMT. A consumer-side private conversion
bypass previously reached a native object with Structures absent. Neither that
bypass nor matching counts establishes a sound composition.

## What is measured and what is assumed

**Reproduced:** The bundled pentalanine source subset uses ten atoms and original
structure indices `[0, 8, 3]`. Separate topology/chemistry and Structures files cause
`MultipleMolecularSystemsError` before conversion in the initial regression run
(one failed test, 3.59 seconds). A first composer then exposed the native topology
ownership guard; copying its topology/chemical authority preserves input owners.
The corrected initial regression selection passed 40 tests in 10.57 seconds.

The final composition module, including independent bond-endpoint checks for each
chemical state, passed 16 tests in 8.48 seconds. The broader regression
selection passed **775 tests in 163.03 seconds**:

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
  tests/basic/convert/mult_to_one \
  tests/basic/convert/test_convert_multiple_systems_error.py \
  tests/_private/test_molecular_system_validation.py tests/form/file_h5msm \
  --doctest-modules molsysmt/basic/convert.py
```

The 669 warnings include 668 legacy-format deprecation warnings and one existing
off-axis structural-attribute warning. These runs overlap; they are not summed as
unique tests. Ruff, docstring validation, the public signature guard, developer
guide and course gates pass. Foundations, Toolbox, Cookbook and course Module 05
state the supported composition contract. Notebook changes are prose-only and
preserve executed outputs. Durable rules are in `devguide/forms_and_conversions.md`.

## Resolution

The guard compares real pentalanine coordinates, source atom IDs and ordered
frames against independent source slices in both input orders and both file/native
routes. Separate synthetic observations check remapped participant/structure/source
indices, original producer versions and evaluated-empty coverage through a public
file roundtrip. A frame-only input retains time without inventing an atom axis.
Native state associations and unknown assignments survive, and the source topology
owner remains intact. Negative cases reject atom/frame mismatches, duplicate
Structures/analysis providers, nonempty mechanics and separate complete systems.
A monkeypatched metadata test forbids materializing data during classification.

No new inference of correspondence, trajectory streaming or scientific recognition
benchmark is claimed. Full-file conversion still loads its domain arrays.

## What was refuted

- Form capability declarations imply a topology exists on every instance: false
  for optional H5MSM 0.5 layers and partial MolSys objects.
- Selecting each partial system independently is sufficient: an absent frame axis
  cannot accept frame indices, and small selections can hide full-axis conflicts.
- Reusing a source Topology in a second MolSys preserves ownership: the native
  owner guard correctly rejects that binding.
- Combining chemical and structural files identifies each structure's chemical
  state: only already declared associations or the existing single-state rule apply.

## Scope and exclusions

Complementary partial native MolSys objects and materialized H5MSM 0.5 inputs, with
explicit positional correspondence declared by their list/tuple. Whole-system
files, legacy Amber combinations and other form compositions keep existing routes.
No automatic identity matching, reordering of independent inputs, domain conflict
resolution, subsystem embedding or mechanics transfer. Explicitly align inputs
before composition when their atom/structure order differs.

## Acceptance criteria

- Both input orders and file/native inputs preserve real coordinates, topology,
  state-dependent chemistry and selected frame order.
- Named analysis remapping preserves coverage, original producer versions and
  local-to-source maps, including repeated/nonconsecutive structures and empty frames.
- Missing frame-to-state assignments remain unknown; existing declarations survive.
- Full-axis conflicts and duplicate domain/name providers fail before selections
  or output creation; sources and their owners remain intact.
- Separate complete systems still raise their classification-specific error.
- Public docs, User Guide and relevant course material state correspondence,
  ownership, units and memory limits; the guard is addressable under tests/basic.

## Provenance

Local Linux x86_64, Python 3.13.14 under uibcdf/molsysmt#237, NumPy 2.4.6,
h5py 3.16.0, released ArgDigest 0.13.0 snapshot
`9880fa7b990fd0987ff0de715b665eb9e11c11b2`; 2026-10-03.
Command: `env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest
--receptor=llm tests/basic/convert/mult_to_one/test_convert_complementary_h5msm_domains.py
tests/basic/convert/test_convert_multiple_systems_error.py
tests/_private/test_molecular_system_validation.py
tests/basic/convert/mult_to_one/test_convert_chemical_and_structural_domains.py`.
