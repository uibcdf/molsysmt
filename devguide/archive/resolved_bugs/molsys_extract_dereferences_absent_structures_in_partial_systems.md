---
summary: MolSys.extract dereferences absent structures in topology-and-chemistry partial systems
issue: uibcdf/molsysmt#307
status: resolved
opened: 2026-10-03
closed: 2026-10-03
severity: high
verification: reproduced
area: [extract, form]
guard: tests/native/test_molsys.py::test_extract_topology_chemistry_without_structures_preserves_domains
normative:
blocked_by: []
supersedes: []
---

# MolSys.extract dereferences absent structures in partial systems

**Reported:** 2026-10-03 by MolSysViewer in uibcdf/molsysviewer#151.
**Status:** Resolved; native and public extraction preserve absent domains.

## What

A valid native `MolSys` containing topology and chemical states but no structures
fails on an atom subset. Its partial extraction branch checks only for absent
topology; a topology-present source dereferences `self.structures.extract` although
structures are absent. H5MSM 0.5 permits this combination.

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
  tests/native/test_molsys.py::test_extract_topology_chemistry_without_structures_preserves_domains
```

On the pre-fix source: `AttributeError: 'NoneType' object has no attribute 'extract'`
at `molsysmt/native/molsys.py:874`.

## How

Route sources with absent topology or absent structures through native partial
extraction. Extract present topology and chemical states without creating another
chemical store, preserving the reference collection alias. Reuse native topology
selection and its established sorted atom-index convention. Preserve absent
chemistry too when the source is topology-only. Validate an explicitly requested
structure axis against present structures or named interactions; reject undeclared
axes deliberately. Remap analyses and per-atom mechanics where a topology exists.

## Why

MolSysViewer's complementary-file workflow delegates selections to MolSysMT.
It cannot safely substitute its own partial-domain extraction. The defect also
affects public `extract` and `convert` routes that delegate to native extraction.
Selecting atom indices must not require invented coordinates.

## What is measured and what is assumed

**Reproduced:** One native regression fails with the reported AttributeError at
commit `d04299cc4`. The first local fixture attempt incorrectly reused an owned
topology and was rejected; copying the topology supplies a valid detached source
and reproduces the actual defect.

**Contract-tested:** The consumer's real pentalanine H5MSM preparation is exercised
through native extraction, public native extraction/conversion and file-to-native
extraction/conversion, followed by public H5MSM subset roundtrips. Independent
expected atom IDs and endpoint maps check chemistry. Unknown structure axes
fail deliberately. Topology-only extraction retains absent chemistry, multiple
states retain reference/metadata, and named analyses can supply a repeated,
nonconsecutive frame selection without coordinates. Per-atom mechanics and
source immutability have a native guard. Fixing this defect alone cannot qualify
arbitrary complementary-file composition or Viewer rendering.

## What was refuted

- An attached topology does not imply structures are present.
- Equal axis lengths alone do not establish correspondence between independent
  files; valid H5MSM fixtures must still declare their identity associations.
- Creating empty structures would erase the absent-domain distinction.

## Scope and exclusions

Correct extraction of existing partial native domains and supported public/H5MSM
delegations. Keep complete-system behavior, identity associations and source
immutability. Do not add a Viewer composition engine or infer cross-file maps.
General `remove`, merge and append behavior is not expanded by this fix.
The additional topology/chemistry/interactions-without-Structures persistence
combination remains unsupported and is recorded in the open #252 implementation
record. Its observed writer error must not be mistaken for an extraction failure.

## Acceptance criteria

Native and public extraction retain absence, selected identities and chemistry,
including state metadata and bonds. Unknown structure axes raise deliberate
errors. Declared interaction axes allow explicit frame selection without
coordinates; occurrences and source maps remain aligned. A real pentalanine
topology/chemistry file can be selected and roundtripped through public H5MSM.
Preserve all/all copy behavior and existing complete/topology-free regressions.
Close with an addressable failing-before/passing-after guard and this archived record.

## Dependencies and risks

Consumer relationship: uibcdf/molsysviewer#151. Main risks are accidentally creating
absent layers, making a second chemistry copy or remapping analyses with a different
atom order than topology. No external engine is needed.

## Provenance

2026-10-03, local Linux x86_64, Python 3.13.14 under uibcdf/molsysmt#237 and released
ArgDigest 0.13.0 snapshot. This local evidence does not certify Python 3.14 or
MolSysViewer rendering. The consumer's report supplies separate Python 3.14.7 evidence.

## Final validation — 2026-10-03

The joint focused run passes **80 tests in 14.09 s**. Ten expected warnings
identify the bundled legacy 0.4 source and its migration path. The native module
doctest passes (one test, 0.17 s). Ruff, docstring fidelity, course validation,
developer-guide validation and diff whitespace checks pass. The course change
is narrative-only and preserves previous code/output cells.
A final five-route real-file run passes in 6.32 s after strengthening its atom
selection to retain covalent bonds and requiring a nonempty expected bond map.
Thus the endpoint comparison cannot pass vacuously on an entirely disconnected
subset. This final run also reports the expected legacy-source warnings.

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
  tests/native/test_molsys.py \
  tests/form/file_h5msm/test_topology_chemistry_v05_probe.py \
  tests/form/file_h5msm/test_topology_free_molsys_v05_probe.py \
  tests/form/file_h5msm/test_state_only_molsys_v05_probe.py \
  tests/form/file_h5msm/test_absent_chemical_states_v05_probe.py \
  tests/form/file_h5msm/test_public_h5msm_v05.py \
  tests/native/test_molsys_interactions.py \
  tests/native/test_molsys_chemical_state_association.py

env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
  --doctest-modules molsysmt/native/molsys.py
python devtools/scripts/validate_course.py
python devtools/scripts/validate_docstrings.py
python devtools/scripts/validate_devguide.py

env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
  tests/form/file_h5msm/test_topology_chemistry_v05_probe.py::test_real_topology_chemistry_atom_selection_without_coordinates
```

The primary guard fails at the original absent-Structures dereference and passes
when native extraction preserves that absence and remaps topology, chemistry and
mechanics. The public-file tests protect the consumer delegation independently.
The durable user contract is in
[H5MSM 0.5](../../../docs/content/user/tools/form/file/h5msm_05.md) and
[MolSys](../../../docs/content/user/foundations/native_world/classes/molsysmt_MolSys.md).
