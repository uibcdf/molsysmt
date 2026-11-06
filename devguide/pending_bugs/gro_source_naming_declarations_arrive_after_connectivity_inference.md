---
summary: GRO source naming declarations arrive after connectivity inference
issue: uibcdf/molsysmt#596
status: active
opened: 2026-11-05
closed:
severity: high
verification: reproduced
area: [form, convert]
guard: tests/form/file_gro/test_mdtraj_connectivity.py::test_gro_source_convention_precedes_candidate_inference
normative:
blocked_by: []
supersedes: []
---

# GRO source declarations arrive after chemical interpretation

## What

An explicit `from_naming_scheme='amber'` reaches GRO native construction after
classification and bond inference. A synthetic ASH/GLH peptide consequently
has no edges despite the declaration. The native source is not reinterpreted
safely by assigning metadata to an already constructed inventory.

## How

The generic naming boundary used a native-first conversion with no source
context. Readers that explicitly accept the declaration now receive it before
construction. Direct readers retain their selection and coordinate-series
routes; native fallback reads receive the same context. Existing native
sources keep their selected-group conflict and independent-copy policy.

GRO native file/handler adapters declare the source vocabulary before rebuilding
group types and inferring candidate bonds. MDTraj file adapters forward that
context while retaining coordinate-series, time, box and selection behavior.
All new public reader parameters use the existing ArgDigest validator. No
chemistry or force field is assigned by the declaration.

## What was refuted

A file extension is not a naming convention. Declaring Amber globally for the
mixed-label bundled GRO loses valid curated YPL/LRT references: this is not an
acceptable route to the historical edge count. The undeclared fixture retains
5,601 supported edges and excludes 31 candidate edges reaching ambiguous
ASH/GLH groups. Its test now asserts that boundary and retains YPL connectivity.
The explicit Amber synthetic fixture independently retains all 16 expected edges.

## Acceptance and evidence

The native file/handler declaration guard checks labels, string IDs, stored
scheme and exact candidate edges; undeclared names never acquire Amber chemistry.
MDTraj controls check nonconsecutive structures [2, 0], atom selection, nm/ps
provider outputs under a noncanonical unit context, boxes and remapped edges.
Existing native declaration/conflict rules remain unchanged. Affected conversion
selection passes 146 cases; serial CCD/conversion selection passes 72 cases.
These suites overlap and are local source evidence, not the full hosted gate.

## Scope and provenance

No schema, dependency floor, compiled backend or scientific threshold changes.
Linux/Python 3.14.7; main ed09f64539a5af6c1dbe9bd352c7ef65dcd4a7a6 plus PR
1c88e785b4327350ad586d437a569eff1a2c5c9a and local receiving corrections.
Receipts: .pytest_cache/543-native-conversion-r3.xml and
.pytest_cache/543-serial-conversion-repaired.xml (private local evidence).
