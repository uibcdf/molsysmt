---
summary: Native atom membership loses hierarchy order and fabricates missing parents
issue: uibcdf/molsysmt#498
status: resolved
opened: 2026-10-27
closed: 2026-10-27
severity: medium
verification: measured
area: [form, native, attribute]
guard: tests/form/molsysmt_Topology/test_atom_membership_order.py::test_all_memberships_match_explicit_source_element_order
normative:
blocked_by: []
supersedes: []
---

# Native atom membership order and missing parents

**Reported:** 2026-10-27, while implementing contribution aggregation in
uibcdf/molsysmt#497.
**Status:** Fixed and locally qualified through public/native query guards.

## What

A group-free native system with three atoms reports zero group indices but
three singleton atom-membership rows. Chain queries have the same defect.
For real groups/chains/molecules/entities, `selection='all'` can enumerate
memberships in first-atom-encounter order instead of source element-index order,
and omit empty source elements. A missing molecule parent can also be indexed
as `-1` into the entity table, assigning its atoms to the final entity.

```python
from rdkit import Chem
import molsysmt as msm
molsys = msm.convert(Chem.MolFromSmiles('CCO'), to_form='molsysmt.MolSys')
msm.get(molsys, element='group', group_index=True, atom_index=True)
# Before: [[], [[0], [1], [2]]]
# Required: [[], []]
```

## How

`get_atom_index_from_group/chain/component/molecule/entity` in the native
Topology adapter grouped observed labels into insertion-ordered dictionaries
for `all`, rather than enumerating the declared parent axis. Missing parent
labels therefore became real rows, unobserved rows vanished and numerical order
was lost. Entity projection also used direct array indexing with missing
molecule membership represented as `-1`.

Initialize rows from the requested source indices, including the full declared
axis for `all`, then append only valid assigned atoms and return rows in the
requested order. Explicit repeated indices repeat rows; empty selections remain
empty. Entity projection reuses the existing nullable hierarchy mapper rather
than copying parent inference. No groups/chains or chemical assignments are
created. Public `basic.get` documents the native membership guarantees.

## Why

Atom membership can become misaligned with group/chain/molecule/entity indices
and any property built on them. Fixing only a descriptor consumer would retain
incorrect public queries and duplicate selection semantics. The owning form
adapter repair benefits native `get` and form-agnostic queries alike.

## Evidence and acceptance

The focused guard covers group-free Topology/MolSys queries, reversed source
parent order, repeated/empty selections, explicit empty groups and unassigned
atoms. Existing native form, generic get and group-free molecule regressions
must continue to pass. Qualification scope and environment are retained with
the associated contribution implementation receipt.

## Refuted paths and exclusions

Do not invent parent groups for missing labels, infer hierarchy by atom encounter
order or repair grouping only inside physchem. Other derived attribute families
are outside this atom-membership fix; this does not certify all external adapter
hierarchy behavior or change public signatures, IDs or chemical state storage.

## Provenance

Reproduced on the existing Linux/Python 3.14 development interpreter, native
queries from source `4e2e18ce71d64256baf3c0a7fd52f89e6aa9b792`. No clean installed,
cross-platform or release qualification is claimed.

## Qualification closeout — 2026-10-27

The expanded scope passes 3,185 tests; final targeted qualification passes
1,464 native query/form tests and 218 descriptor/primary-control tests. The
556-case documentation/receiving scope includes two doctests, notebook schema
checks and all seven valid bound TPSA output levels with preserved scene state.
Legacy atom/group rejection controls were replaced by positive forwarding
checks and unsupported bond rejection, preserving test intent after the extension.
All 14 fast gates, scoped Ruff, docstring and signature checks pass.

Both tool notebooks were executed on the final implementation (8.2 and 8.5
seconds); the Cookbook exports were executed and asserted. All five edited
course notebooks retain their original code and saved outputs. HTML exits zero
with existing header/orphan diagnostics outside the new contribution examples.
No warning-debt reduction, whole-suite, benchmark, installed-pair, cross-platform
or release qualification is claimed. Exact commands, chronology, warnings,
environment, hashes and scientific limits are in the
[qualification receipt](../../../devtools/data/descriptor_contributions_20261027.json).
