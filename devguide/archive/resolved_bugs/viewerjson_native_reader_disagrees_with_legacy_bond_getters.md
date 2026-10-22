---
summary: ViewerJSON native reader disagrees with legacy bond getters
issue: uibcdf/molsysmt#400
status: resolved
opened: 2026-10-21
closed: 2026-10-21
severity: medium
verification: reproduced
area: [form, convert, tests]
guard: tests/form/molsysmt_ViewerJSON/test_bond_decoding.py
normative:
blocked_by: []
supersedes: []
---


# ViewerJSON native reader disagrees with legacy bond getters

**Reported:** 2026-10-21 while qualifying #399 endpoint encodings.
**Status:** Resolved; direct native import and bond queries share one unambiguous bond decoder.

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

## Resolution — 2026-10-21

**Implemented:** flat canonical atom_pairs, aligned indexA/indexB endpoint lists,
and wrappers containing a unique bond definition feed one shared private format
reader. Empty definitions and empty collections yield zero bonds. Empty outer
placeholder columns are allowed around a unique set; populated competing flat
columns are rejected. The decoder validates integer positional endpoints,
bounds when the atom count is known, agreement between redundant encodings and
aligned bond columns. Source dictionaries are read without mutation.

Native import, bond count/index/order/type queries and data-level bonded_atoms
availability use the same interpretation. FormatError propagates instead of
being reported as a missing attribute. Capability-only include_none=True queries
retain their established meaning. Native import validates the graphics bond
block before building native tables; the existing chemical-state translator
retains ownership of chemical validation and order/type normalization. Arbitrary
graphics metadata do not become chemical assignments.

The format helper also supplies flat-block endpoint validation to the graphics
extractor, removing its separate decoder. Graphics extraction, copying and JSON
transport retain separate sets. Native conversion and bond queries reject more
than one set with FormatError, including when an atom selection makes one set
empty. Users can copy the payload, assign the intended existing set to
chosen.data["bonds"], then convert/query it. This uses current supported operations;
no new function, argument, chemical store, dependency floor or schema version
was introduced. The unused duplicate first-set helper in the structural adapter
was removed.

### Decision and alternatives

The graphics schema supplies no declared mapping from sets to chemical states or
structures. Silently choosing the first set discards represented connectivity;
merging sets could introduce incompatible edges/orders. Inferring ChemicalStates
would invent state identity and associations. Explicit selection on a copy is
available now, so no speculative selection API is needed. A future multi-state
codec requires its own declared contract. The conservative rejection fully meets
this issue's accepted resolution option without extending the 1.0 format scope.

The format decoder scans represented bond rows and checks column lengths. It
reuses canonical endpoint lists read-only and constructs canonical pairs only
for legacy endpoint columns. It does not allocate all possible atom pairs,
construct a native system just to count bonds, or cache mutable payload state.
No production timing or memory benchmark is claimed.

### Evidence and limits

**Contract-tested:** the initial 44-case module obtained 35 failures and nine
passes against the old reader/getters. The final 45-case module checks literal
pairs and orders on all three endpoint encodings, flat/unique wrapped imports,
zero bonds, empty outer placeholders, nullable orders, unique nested wrappers,
malformed indices/columns and competing declarations, consistent rejection of
multiple sets on conversion and bond queries, explicit set selection and source
immutability. The graphics subset guard preserves both set blocks independently.
The tests compare explicit expected values, rather than two routes sharing the
same decoder as their only oracle.

On Linux/Python 3.14.7, the combined Topology/MolSys/Structures/ViewerJSON form
scope and remaining native copy regressions obtained **1,930 passed**, no omissions,
in 19.19 s with `python -m pytest --receptor=llm -n 12`. Six existing legacy H5MSM
deprecation warnings were retained. Four doctest items across the graphics
extractor, converters and wrapper pass. Ruff package/new-test lint, public
docstring fidelity (247 functions), and public signature validation also pass.

Foundations, Toolbox, Cookbook and course Module 4 document the policy. Existing
notebook executable cells/outputs are preserved; no full notebook reexecution,
Sphinx build, installed-client, rendering or full scientific matrix is claimed.
Read-only inspection of the sibling MolSysViewer source found its current loader
uses native data instead of ViewerJSON; that inspection does not qualify a client
package or authorize a publication. No sibling files were changed.

No new scientific calculation or third-party method is involved, so no new
Ackredit or optional-engine boundary applies. Native/h5msm chemical-state
persistence and the existing Interactions contract are unchanged.

The 14 fast repository gates and focused formatting checks also pass. The
Cookbook sequence was executed with two declared sets: copy the payload, select
its second legacy-encoded set, import the literal (1, 2) double bond, and verify
the original still contains both sets. These results add no release or
installed-pair authorization.
