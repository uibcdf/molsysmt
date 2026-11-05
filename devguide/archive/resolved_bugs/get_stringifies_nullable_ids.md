---
summary: Get stringifies nullable IDs instead of preserving missing labels.
issue: uibcdf/molsysmt#579
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: reproduced
area: [basic, tests]
guard: tests/basic/get/test_nullable_ids.py::test_nullable_ids_remain_missing_in_public_and_native_queries
normative:
blocked_by: []
supersedes: []
---

# Get stringifies nullable IDs

## What

On main b8cdbd101, setting `atom_id=['alpha', None]` on a native MolSys
stores `['alpha', pandas.NA]`. Both public and native get() return
`['alpha', '<NA>']`. Reproduced while implementing #574, with Python 3.14.7
and pandas 2.3.3. A missing value becomes a present literal label.

## How

The shared `basic.get._coerce_ids_to_string` explicitly preserves Python None
but its final string cast does not recognize pandas.NA or numeric NaN. Both
query routes and some nested alternate-location ID data reuse this function.

## Why

Source missing metadata must remain distinct from actual labels '<NA>',
'None', 'nan' and empty strings. ID labels never provide positional identity.
Fix the shared owner and have #574 reuse public get(), rather than adding
another missing-value interpreter inside solvation.

## Acceptance criteria

Normalize missing scalar, flat and nested IDs to None. Retain present labels
as strings, including literal sentinel spellings. Preserve selection order,
repetition and source storage. Exercise universal and native public queries.

## Evidence status

**Contract-tested**. The common normalizer classifies missing IDs with pandas
before casting present labels to strings. Object construction preserves original
mixed-list scalar types, so numeric NaN does not first become literal 'nan' and
an integer label does not first become a float. Actual sentinel spellings remain
literal labels. Both native get() and universal get() reuse this path; no
solvation-specific missing-value workaround was needed.

## Receiving — 2026-11-05

The shared #574/#579 receiving passes **3,273 affected tests**, **167 published
support-floor tests** and **585 documentation/governance/doctest checks**. The
addressable guard checks public/native atom, group and chain ID queries, source
storage and selected order/repetition. Separate scalar/nested assertions cover
None, pandas.NA and numeric NaN without conflating literal strings. No public
signature, unit policy or dependency floor changes.

Get/solvate docstrings, the Foundations overview, both tools tutorials, the
solvation Cookbook and course lessons 8/12 reflect the normalization contract.
Code cells, outputs and notebook metadata are preserved. Shared diagnostics,
argument and dependency boundaries remain intact; metadata normalization is not
a new scientific calculation or attribution event.

The [shared receiving receipt](../../../devtools/data/source_identifier_receiving_574_579_20261105.json)
retains commands, hashes, limitations and source identity. Routine hosted and
release-candidate qualification are separate evidence.

## Failed draft corrected

An initial change handled missing object-array values but still let np.asarray
turn `[numeric_nan, '<NA>']` into strings and `[7, numeric_nan]` into floats
before classification. The nested guard failed. Keeping the original scalar
types in object storage before classifying missing values resolves that failure
without treating real 'nan' strings as missing.
