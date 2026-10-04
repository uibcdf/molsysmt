---
summary: ChemicalStatesDict stringifies object-backed bond values.
issue: uibcdf/molsysmt#325
status: resolved
opened: 2026-10-04
closed: 2026-10-04
severity: high
verification: reproduced
area: [form, convert]
guard: tests/form/molsysmt_ChemicalStatesDict/test_roundtrip.py::test_object_backed_bond_fields_preserve_boolean_numeric_values_and_nulls
normative:
blocked_by: []
supersedes: []
---

# ChemicalStatesDict stringifies object-backed bond values

**Reported:** 2026-10-04, during preparation-history persistence for #298.
**Status:** Resolved with a direct typed-value regression and integrated preparation/H5MSM validation.

## What

Converting a chemical-template result's ChemicalStates to ChemicalStatesDict and
back raises `TypeError: Need to pass bool-like values`. Object-backed numeric
bond orders are also serialized as string values. Valid scientific values must
not acquire another meaning because pandas used an object backing column.

## How

`_encode_series` historically treated every object column as strings. Template
assignment through pandas `.at` can produce ordinary object columns with actual
boolean or numeric values. The decoder reconstructs a canonical Bonds_DataFrame,
which cannot interpret strings `False`/`True` as boolean assignments.

The encoder now uses the native bond-column dtype declarations before encoding
values and null masks. This uses the existing owner definitions, preserves row
order and optional-column absence, and does not mutate source tables. It does
not infer chemistry, reorder bonds or introduce covalent defaults.

## Why

Typed state serialization is a public reuse boundary. Incorrect booleans or bond
orders affect aromaticity, component membership and later recognition; an
exception prevents an otherwise supported native round trip.

## Evidence and exclusions

**Reproduced:** native methanol template application followed by dictionary
round trip failed in the boolean decoder; inspection showed bond-order values
`['1', ...]` and boolean values `['False', ...]` in typed string arrays.
**Contract-tested:** the direct regression uses object-backed integer/boolean
columns with true, false and missing values and checks source independence.
This correction covers canonical bond fields, not arbitrary user object columns.

## What was refuted

The failure is not caused by the new preparation-history tree. It occurs in
the existing bond-table decoder, and the independent guard needs no history.
Stringifying booleans and relaxing the decoder would admit ambiguous chemical
assignments; declared native dtypes protect the semantic boundary instead.

## Acceptance criteria

The direct regression must preserve numerical bond order, true/false values,
null masks and source tables. Existing multistate/nullable round trips and the
chemical-template preparation route must continue to pass.

## Provenance

Linux, Python 3.13.14 under the tracked #237 local exception, NumPy 2.4.6,
pandas 2.3.3; released ArgDigest 0.13 override. Direct reproduction uses
`tests/physchem/test_chemical_template.py`'s deterministic methanol control.
Guard command:

```bash
python -m pytest --receptor=llm tests/form/molsysmt_ChemicalStatesDict/test_roundtrip.py
```

## Resolution

The encoder casts canonical bond columns using their owner-declared dtypes before
serializing values and null masks. The direct guard checks integer bond order,
false versus missing aromaticity, true/false component-join flags and input
independence; it fails in the original stringifying implementation without needing
preparation history. The integrated run passed 887 tests in 151.97 s. A subsequent
30-test run verified the final codec/preflight adjustments; both commands and
scope are recorded in the linked #298 checkpoint. This is contract evidence,
not scientific validation of a newly inferred chemical method.
