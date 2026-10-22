---
summary: ViewerJSON native reader disagrees with legacy bond getters
issue: uibcdf/molsysmt#400
status: open
opened: 2026-10-21
closed:
severity: medium
verification: reproduced
area: [form, convert, tests]
guard:
normative:
blocked_by: []
supersedes: []
---


# ViewerJSON native reader disagrees with legacy bond getters

**Reported:** 2026-10-21 while qualifying #399 endpoint encodings.
**Status:** Open; direct legacy bond import remains separate from extraction.

## What

The getters recognize legacy endpoints or the first bond set, but native import
does not read the same connectivity:

```python
import molsysmt as msm
from molsysmt.native import ViewerJSON
payload = ViewerJSON(data={
    "atoms": {"atom_id": ["A", "B"], "atom_name": ["C", "O"]},
    "bonds": {"indexA": [0], "indexB": [1], "order": [1]},
})
assert msm.get(payload, n_bonds=True) == 1
msm.convert(payload, to_form="molsysmt.Topology")
# StructuralInconsistencyError: Bond order received 1 values; expected 0.
```

With bonds={"sets": [{"atom_pairs": [[0, 1]], "order": [1]}]}, the getter
still reports one bond, but native import succeeds with zero bonds.

## How

The existing _bonds_dict getter helper unwraps the first set, and the count
getter falls back to indexA. The native reader obtains the outer bonds dictionary
and reads only its atom_pairs field. Atom-subset extraction under #399 remaps
legacy endpoints into canonical pairs, but an unrestricted copy/import does
not run that normalization.

## Why

A source can advertise covalent connectivity and then fail to import, or silently
lose that connectivity. Native chemistry has explicit state semantics, so a
multi-set graphics payload also requires an agreed import policy rather than
silently ignoring or merging competing bond sets.

## What is measured and what is assumed

**Reproduced:** the two public examples above on Linux/Python 3.14.7, with the
reader still using the #397 identity implementation. Legacy endpoints with order
raise the metadata-length error; a single nested set imports zero bonds.
Multiple nested sets and downstream rendering have not been qualified.

## What was refuted

This is not an ID-label failure: both atom IDs are valid strings. It does not
require extracting a subset, and the source provides both bond endpoints.

## Scope and exclusions

Own direct ViewerJSON bond decoding and agreement with available getters.
Do not silently combine multiple sets into one chemical state. The atom-subset
remapping and JSON copying work is tracked independently in #399.

## Acceptance criteria

A guard must compare literal connectivity on direct legacy/canonical imports,
not just counts from two routes sharing one decoder. Explicitly decide whether
multiple sets select one declared set, map to chemical states, or raise a clear
error; keep getters and documentation consistent with that policy. Preserve
bond orders and aligned metadata and cover zero bonds. Avoid a graphics-to-native
conversion that silently reports success after discarding represented bonds.

## Provenance

Observed 2026-10-21 in the existing development environment, Linux/Python 3.14.7.
No installed-client, performance or full scientific qualification is claimed.
