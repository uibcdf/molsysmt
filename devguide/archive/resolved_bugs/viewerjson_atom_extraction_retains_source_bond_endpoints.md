---
summary: ViewerJSON atom extraction retains source bond endpoints
issue: uibcdf/molsysmt#399
status: resolved
opened: 2026-10-21
closed: 2026-10-21
severity: medium
verification: reproduced
area: [form, extract, tests]
guard: tests/form/molsysmt_ViewerJSON/test_extract.py
normative:
blocked_by: []
supersedes: []
---


# ViewerJSON atom extraction retains source bond endpoints

**Reported:** 2026-10-21 while reviewing the independent #397/#398 fixes.
**Status:** Resolved; graphics selections remap bonds, preserve axis order and copy selected data.

## What

Extracting two atoms from a three-atom ViewerJSON retains both source bonds,
including an endpoint outside the new atom axis:

```python
import molsysmt as msm
from molsysmt.native import Topology
molsys = Topology(n_atoms=3)
molsys.add_bonds([[0, 1], [1, 2]])
payload = msm.convert(molsys, to_form="molsysmt.ViewerJSON")
subset = msm.extract(payload, selection=[1, 2])
assert subset.data["bonds"]["atom_pairs"] == [[0, 1], [1, 2]]
msm.convert(subset, to_form="molsysmt.Topology")
# StructuralInconsistencyError: Bonded atom indices must be between 0 and 1.
```

The intended surviving bond is source (1, 2), remapped to local (0, 1).

## How

`molsysmt/form/molsysmt_ViewerJSON/extract.py` slices atom columns and
coordinates, but copies the bonds block without filtering or endpoint remapping.
It also uses list(np.array(values)[idx]) for atom columns, which may retain
NumPy scalar types. The endpoint failure above is executed evidence; the scalar
risk is source inspection and requires a separately qualified labeled fixture.

## Why

A declared atom subset may carry unrelated bonds or out-of-range endpoints into
native reconstruction or rendering. This adapter is independent of MolSys
extraction and does not demonstrate a defect in native/H5MSM remapping.

## What is measured and what is assumed

**Reproduced:** the exact public example above on Linux/Python 3.14.7, after the
native exporter scalar fix. The subset has two atoms and still carries both
source pairs. Native conversion rejects the out-of-range endpoint.
No client rendering, installed-package or performance claim is made.

## What was refuted

This is not an ID-label interpretation error: the reported failing fields are
positional atom endpoints. The extractor source was not changed by #397/#398.

## Scope and exclusions

Own the atom-selection route and alignment of all bond columns/endpoints,
including legacy endpoint fields and JSON-safe selected atom columns.
Structure-list ordering and duplicate-selection policies must be inspected and
explicitly scoped during implementation; they are not qualified here.
No additional chemistry inference or viewer scene implementation is requested.

## Acceptance criteria

A public guard must check a subset that removes an incident bond and remaps a
retained bond, with aligned order/type columns and no mutation of the source.
Cover a reordered atom selection, zero bonds and standard JSON serialization
before native decoding. Define repeated atom-selection semantics explicitly.

## Provenance

Observed 2026-10-21 in the existing development environment, Linux/Python 3.14.7.
The extraction adapter matches main before the native ViewerJSON repairs.

## Resolution — 2026-10-21

**Implemented:** atom extraction preserves the requested graphics atom order,
retains only bonds with both endpoints selected, and remaps atom_pairs and
indexA/indexB together. Aligned list-valued bond columns are selected with the
same bond-row population. Each nested set is processed independently and remains
a separate graphics block. Legacy endpoint-only blocks gain canonical pairs.
JSON atom columns use list selection without NumPy coercion, preserving strings,
integers and nulls. Invalid bounds, duplicate atom selections and inconsistent
columns/endpoint encodings fail explicitly through existing SMonitor exceptions.
General index validators are reused with direct local counts; the format-specific
column/endpoint translation remains private behind the supported extractor.

Structure lists preserve order and repetitions rather than using a set. Empty
atom/structure selections are supported, and the reader restores empty coordinate
lists as (n_structures, 0, 3). Structure aliases normalize to structures. Selection
precedes copying, so discarded structures/atom rows are not copied. The wrapper's
standard memo-aware protocol retains concrete wrapper metadata independently;
unrestricted copy_if_all=False still returns the original object. This is a
resident JSON operation, not file-backed queries or a benchmarked constant-memory
claim. Full native permutation across every molecular domain remains #369.

The two registered ViewerJSON converters now accept keyword-only atom_indices and
structure_indices, retaining their original item and positional skip_digestion
arguments. They delegate selected conversion to the same extractor. This is
required because msm.extract(..., to_form=...) uses msm.convert; those paths
previously ignored the requested population. Two scoped signature declarations
name the actual route guard; the API validator is unchanged.

**Contract-tested:** the initial 22-case extraction module obtained 21 failures
and one pass against the old adapter. Three additional target-form tests also
failed against the old converter signatures. The final 26-case module checks
literal bond endpoints/order/type/custom columns, source isolation, JSON encoding,
native recovery including zero atoms, endpoint aliases, separate bond sets,
nonconsecutive/repeated structures and legacy structure keys, invalid inputs,
wrapper metadata, and rejection of copying an unselected structure's payload.
The target-form tests qualify ViewerJSON, MolSys and Topology result routes.

The combined native Topology/MolSys/Structures/ViewerJSON form scope, remaining
copy-protocol tests and public signature-validator tests obtained **1,894 passed**,
no omissions, in 17.99 s with `python -m pytest --receptor=llm -n 12` on
Linux/Python 3.14.7. Seven existing legacy H5MSM deprecation warnings were retained.
Three doctest items pass across the extractor and its converters. Documentation
updates cover Foundations, Toolbox, Cookbook and course Module 18; existing
notebook executable cells/outputs are preserved. These are source checks, not
installed-client, rendering, full scientific or multi-platform qualification.
No full Sphinx build or complete notebook reexecution is claimed.

No scientific detection, third-party method, dependency floor or quantity schema
changed; no new Ackredit or external-engine integration boundary applies.
The independent disagreement between direct native legacy-bond import and its
getters is reproduced and tracked in uibcdf/molsysmt#400. This extraction repair
does not choose a multi-set chemical-state import policy or claim to fix that
unrestricted import route.

The 14 fast repository gates, full package Ruff lint, focused formatting, public
docstring fidelity (247 functions) and scoped signature validation passed. The
graphics Cookbook sequence was also executed against the bundled 181l system:
select atoms [2, 1] and structure [0], encode with the standard JSON route, and
recover a two-atom native system with one structure. These checks add no release
or installed-pair authorization.
