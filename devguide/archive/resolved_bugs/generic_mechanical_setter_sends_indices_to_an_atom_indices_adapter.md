---
summary: Generic mechanical setter rejects supported native atom assignments
issue: uibcdf/molsysmt#316
status: resolved
opened: 2026-10-04
closed: 2026-10-04
severity: medium
verification: reproduced
area: [basic, form, attribute]
guard: tests/basic/test_set_mechanical_atom_types.py
normative:
blocked_by: []
supersedes: []
---

# Generic mechanical setter rejects supported native atom assignments

**Reported:** 2026-10-04 during manual replacement controls for uibcdf/molsysmt#222.
**Status:** Resolved; generic dispatch and string-label validation reach native mechanical storage.

## What

`msm.set(mechanics, element='atom', selection=[0], atom_ff_type=['C'])` failed
with `UnknownArgumentError`: the native adapter accepts `atom_indices`, while
the generic setter sent `indices`. After repairing dispatch, value digestion
also rejected supported string-label vectors.

## How

Both generic dispatch paths used the common `indices` keyword for the mechanical
form. The caller-specific value digester had a partial-charge route but no
atom_ff_type route. Native label subset assignment also needed shape/range checks
before allocation or mutation.

## Why

Users could not perform declared manual mechanical replacements, including the
operation that clears named typing provenance. Charge setters on the same form
had the dispatch mismatch too. This is a setter contract defect, not a chemical
typing rule, parameterization or provenance authentication.

## What is measured and what is assumed

**Reproduced:** Focused native mechanical and named-type tests observed both errors.
**Contract-tested:** All/subset assignments cover labels and charge values,
requested index order, invalid vectors and source immutability on refusal.

## What was refuted

The label list and index selection were valid. Skipping digestion would hide an
unsupported public route and was rejected. Adapters keep their existing public
atom_indices signature; other forms keep their own indices convention.

## Scope and exclusions

Native MolecularMechanics dispatch, finite charge delegation already provided,
and one-dimensional manual string labels. Unknown parameter vocabularies are not
chemically certified; the named writer performs its separate vocabulary and
binding checks. This does not add a new MolSys mechanical type storage domain.

## Acceptance criteria

Generic native setters work with all and reordered subset selections. Invalid
label vectors fail before modifying storage. Existing native charge setters and
manual provenance-clearing behavior remain intact.

## Resolution

Map the mechanical form's index keyword at generic dispatch, validate label
vectors at the value boundary, and check subset range/shape in its adapter.
Named labels are cleared after manual replacement. The focused guards cover
actual stored values and failure immutability, not only accepted argument names.


## Local checkpoint

On 2026-10-04, `python -m pytest --receptor=llm
devtools/tests/test_validate_public_api_stability.py
tests/basic/test_set_mechanical_atom_types.py tests/basic/test_set_partial_charge.py`
passed 28 cases in 4.39 seconds. Python 3.13.14 is the bounded development
runtime (uibcdf/molsysmt#237), using the released ArgDigest 0.13 source snapshot
at `9880fa7b990fd0987ff0de715b665eb9e11c11b2`. These focused controls do not
establish a full platform matrix or release qualification.
