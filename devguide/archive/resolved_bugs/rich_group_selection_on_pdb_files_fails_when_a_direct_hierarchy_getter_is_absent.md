---
summary: Rich group selection on PDB files fails when a direct hierarchy getter is absent
issue: uibcdf/molsysmt#303
status: resolved
opened: 2026-10-03
closed: 2026-10-03
severity: medium
verification: reproduced
area: [selection, form]
guard: tests/basic/select/test_hierarchy_fallback.py
normative: devguide/forms_and_conversions.md
blocked_by: []
supersedes: []
---

# Rich hierarchy selection requires a direct getter that PDB does not expose

**Reported:** 2026-10-03, while implementing residue coverage in uibcdf/molsysmt#218.
**Status:** Resolved. Public delivery now projects hierarchy indices in both branches.

## What

A supported PDB source supports atom selection and public hierarchy attribute
queries, but a rich selection with `element='group'` raises `AttributeError`.

```python
import molsysmt as msm
source = msm.systems['T4 lysozyme L99A']['181l.pdb']
msm.select(source, element='group', selection="group_name=='HOH'")
# AttributeError: file_pdb has no get_group_index_from_atom
```

## How

The hierarchy projection in `basic.select` directly dereferences a form getter
instead of using the public delivery machinery in `basic.get`. PDB advertises
hierarchy attributes through conversion routes; it need not declare each direct
getter. The same assumption appears in the nested-selection branch.
Use public `get` for the already resolved atom indices in both branches.

## Why

Form-agnostic group/component/chain/molecule/entity selection fails for a supported
source. Native conversion is a workaround, not a justification for breaking the
public source-form contract. No hierarchy, state or source indices may be inferred
by the selector to hide a missing delivery route.

## What is measured and what is assumed

**Reproduced:** The HOH query above failed with the missing direct getter.
**Contract-tested:** Six focused cases compare real PDB hierarchy selection to
native delivery for all five hierarchy elements, empty results and nested atom
selections. The initial run passed in 10.21 s.
**Unassessed:** Exhaustive source-form coverage and performance are not measured.

## What was refuted

A declared attribute does not imply a direct `get_X_index_from_atom` callable;
conversion-backed public delivery is valid.

## Scope and exclusions

Reuse the existing general attribute-delivery contract in hierarchy projection.
No parser, inference, selection-language or scientific classification change.

## Acceptance criteria

- Real PDB rich hierarchy selections match source/native index projection.
- Empty and nested selections retain their result shapes.
- Existing selector regressions and source-state tests remain valid.

## Resolution — 2026-10-03

Both hierarchy branches now call public `basic.get` with resolved source atom
indices instead of requiring a direct form getter. No public signature, parser,
selection language or source-axis convention changed. The normative rule is in
[forms and conversions](../../forms_and_conversions.md).

The guard `tests/basic/select/test_hierarchy_fallback.py` exercises all five
hierarchy elements on the real bundled PDB, compares index results to native
attribute projection and checks empty/nested result shape. A restored direct
getter assumption fails those queries rather than satisfying a superficial
interface check. The full existing selector cohort plus the chemical coverage,
state-selection and modified-residue regressions passed **172 tests in 64.24 s**,
including the six defect-specific tests, with ArgDigest 0.13.0 at
`9880fa7b990fd0987ff0de715b665eb9e11c11b2` (isolated source snapshot), Python
3.13.14 and the current Linux source environment. Reproduce with:

```bash
python -m pytest --receptor=llm tests/basic/select
```

The cross-domain command and environment limits are recorded in the resolution
of uibcdf/molsysmt#218. Exhaustive form parity and performance remain unassessed.
