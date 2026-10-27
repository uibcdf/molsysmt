---
summary: H5MSM writes an unreadable identity association when structure and chemical-state counts differ
issue: uibcdf/molsysmt#481
status: open
opened: 2026-10-26
closed:
severity: high
verification: reproduced
area: [form, chemical-states, data]
guard:
normative:
blocked_by: []
supersedes: []
---

# H5MSM unequal structure/state association cannot round-trip

**Reported:** 2026-10-26 during the independent state/reference controls for
uibcdf/molsysmt#480. This is a separate storage defect, not a selector failure.
**Status:** Open; reproduced on source 312a73200f5c578ba758618ec42179edb0228221.

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

No storage code is changed by this report. The #480 guard uses a two-structure,
two-state fixture to test its independent selection contract; that does not
resolve this unequal-cardinality failure. Repair remains an explicit follow-up
before final candidate qualification under uibcdf/molsysmt#334.
