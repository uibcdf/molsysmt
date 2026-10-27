---
summary: H5MSM writes an unreadable identity association when structure and chemical-state counts differ
issue: uibcdf/molsysmt#481
status: resolved
opened: 2026-10-26
closed: 2026-10-26
severity: high
verification: reproduced
area: [form, chemical-states, data]
guard: tests/form/file_h5msm/test_associations_v05_probe.py::test_public_unequal_structure_state_populations_roundtrip
normative:
blocked_by: []
supersedes: []
---

# H5MSM unequal structure/state association cannot round-trip

**Reported:** 2026-10-26 during the independent state/reference controls for
uibcdf/molsysmt#480. This is a separate storage defect, not a selector failure.
**Status:** Resolved; original reproduction used source
312a73200f5c578ba758618ec42179edb0228221.

## What

A valid native MolSys with one structure, two chemical states and explicit
structure-to-state indices `[0]` writes successfully to H5MSM 0.5. Reading it
back raises `ValueError: Identity axis link requires equal cardinalities`.
The generated file therefore cannot round-trip through the public converter.

## How

```python
import molsysmt as msm
molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
                     structure_indices=[0])
molsys.chemical_states.append_state()
msm.set(molsys, structure_chemical_state_index=[0])
msm.convert(molsys, to_form='one-structure-two-states.h5msm')
msm.convert('one-structure-two-states.h5msm', to_form='molsysmt.MolSys')
```

The native source has 62 atoms, one structure and two states. No malformed
external input, empty topology or Viewer is involved. Linux/Python 3.14.7;
existing native backend unchanged. The reproduction writes only under /tmp.

## Why

Supported independent structure and chemical-state populations may legitimately
have different cardinalities. Normalizing a valid explicit map into an invalid
identity marker silently creates an unreadable public-format file. This affects
H5MSM persistence and partial populations even though the molecule is valid.

## Inspected mechanism

`molsysmt/form/_h5msm05_associations.py::_normalize_link` validates explicit
mapping length and bounds, then replaces any sequence equal to
`arange(source_size)` with `identity`, without requiring equal source and target
sizes. Reading that marker correctly requires equal cardinalities. A prefix of
a larger target axis must remain an explicit map. No format-schema change is
suggested; the current explicit encoding can represent it.

## Acceptance and recovery

Add a public one-structure/two-state round trip and focused association controls
for prefix maps into larger target populations, equal-cardinality identities,
nonidentity maps, unknown associations and invalid bounds. Preserve explicit
maps where identity is not valid. Verify chemical reference and structure-state
indices after persistence and readiness assessment. Keep reader validation
strict; accepting a malformed identity marker would conceal the writer defect.

## Scope and exclusions

At opening, no storage code was changed. The #480 guard used a two-structure,
two-state fixture to test its independent selection contract; that does not
resolve this unequal-cardinality failure. The native storage correction below
is separate from selection semantics; final candidate qualification remains
under uibcdf/molsysmt#334.

## Resolution — 2026-10-26

The shared association normalizer only emits an identity marker when source
and target populations have equal cardinalities and the explicit vector is
exactly the identity on that complete domain. Prefix maps into a larger target,
including an empty source map, retain the existing explicit int64 encoding.
No root/layer schema, public signature, state-resolution policy, dependency or
compiled backend changes. No new parallel chemical authority is introduced.
The code short-circuits the index-array comparison for unequal cardinalities;
no workload speedup or memory benchmark is claimed.

**Contract-tested:** the regression guard exercises public native conversion,
physical mapping encoding, layer reads, coordinate preservation and readiness
on unequal/equal populations, reordered and unknown state links. Per-state
formal charges and a distinct reference prove that association semantics survive
storage. The original bundled 62-atom pentalanine one-structure/two-state
reproduction also round-trips with identical coordinates and map `[0]`.

Shared atom, structure and structure-to-state controls cover empty prefix maps,
nonempty prefixes, compact full identities, repeated normalization and unchanged
input vectors. Independent layer tests round-trip partial atom/structure links,
then forge invalid identity markers and verify that readers still reject them.
Invalid bounds, lengths, identities and duplicate atom targets preserve an
existing destination unchanged. No reader restriction is weakened to admit the
formerly malformed output.

The before-fix module has 11 failures and 25 passes in 7.12 seconds. Two failures
catch incorrect on-disk identity labels; nine catch repeated normalization
rejecting the marker invented by its own first call. After the fix, the initial
36 cases pass. Two subsequent independent-layer/tampering controls bring the
module to 38 cases within the broader regression.

## Local qualification and documentation

The H5MSM form, sparse-interaction persistence, public workflow, complementary
composition, readiness and native state selection passes **871 cases**, zero
failures or skips, in 19.77 seconds with twelve workers and pytest-receptor.
Its 696 warnings are expected legacy-H5MSM notices. The h5msm module doctest
passes one case; all 491 notebook-schema cases and all 14 fast gates pass.
Ruff, docstring fidelity and public-signature guards pass. Incremental HTML
exits 0 with zero errors and 23 known markup/navigation warnings under #144. The introductory and new
persistence examples execute successfully in a temporary directory. The course
Module 04 changes only prose, preserving all code, outputs and execution metadata.

Public writer help, the H5MSM 0.5 guide, Foundations, migration Cookbook, course
and maintained format contract describe equal-population identity requirements
and explicit structure/state maps. The release ledger records the source fix
without changing artifact identities or the publication pause. The
[qualification receipt](../../../devtools/data/h5msm_prefix_associations_20261026.json)
retains commands, hashes, environment and exclusions. These are local source
results, not full-suite, cross-platform, installed-pair or release qualification.
