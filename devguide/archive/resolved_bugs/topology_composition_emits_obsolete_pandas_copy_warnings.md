---
summary: Topology composition emits obsolete pandas copy warnings.
issue: uibcdf/molsysmt#386
status: resolved
opened: 2026-10-13
closed: 2026-10-13
severity: low
verification: reproduced
area: [basic, form, deps]
guard: tests/form/molsysmt_Topology/test_composition_pandas_compatibility.py
normative:
blocked_by: []
supersedes: []
---

# Topology composition emits obsolete pandas copy warnings

**Reported:** DockingMT under uibcdf/dockingmt#49.
**Status:** Resolved; tested with real pandas 2.3.3 and 3.0.6.

## What

Public merge emits eight Pandas4Warning instances for a two-system composition.
The native Topology.add path has the same deprecated concat keyword in five calls.
This is diagnostic noise, not demonstrated scientific corruption.

## How

`form/molsysmt_Topology/merge.py` and `native/topology.py` pass copy=False to
pandas.concat. pandas 3 ignores this argument and warns. Remove only this obsolete
keyword; preserve concat axes, selections, order, state/bond remapping and dtype
contracts. No replacement merger, warning suppression or version branch is needed.

## Why

Obsolete warnings obscure scientific diagnostics in clients. Composition outputs
must remain independent of source mutations under both older pandas and Copy-on-Write.

## What is measured and what is assumed

Python 3.14.7 / pandas 2.3.3: reported 22+22 atom fixture produces 44 atoms and no
copy warning. The same development interpreter with the pre-existing pandas 3.0.6
package overlay produces 44 atoms and exactly eight Pandas4Warning instances.
No new environment was created or development installation changed.

## What was refuted

Suppressing warnings would hide the obsolete call. Unconditionally deep-copying
all final tables would add memory work without evidence that normal concat
results violate mutation independence. Tests determine that contract directly.

## Scope and exclusions

Only molecular composition concat arguments. NumPy copy=False operations and
ViewerJSON dictionary conversion retain their unrelated semantics. No pandas-4
compatibility, full dependency admission or published-artifact qualification is claimed.

## Acceptance criteria

Real pandas-2/pandas-3 runs retain source tables, typed index offsets, chemical
assignments and covalent pairs; changes to output cannot mutate inputs and vice versa.
The public operation must emit no obsolete-copy deprecations. Existing merge/add
regressions continue to pass.

## Provenance

2026-10-13, Linux, existing Python-3.14.7 development environment. pandas 3.0.6
is read from the existing /tmp overlay solely for bounded compatibility validation.
Provider rationale: https://pandas.pydata.org/docs/reference/api/pandas.concat.html

## Resolution — 2026-10-13

Removed the eight obsolete concat keywords in public topology merge and five in
native Topology.add. Their supported signatures and scientific composition policies
are unchanged. The guard executes public merge and native add, checks deprecation
classes including actual pandas-3 Pandas4Warning, verifies original/source tables,
charges and offset covalent pairs, and mutates all six output/source hierarchy
tables independently in both directions. It does not assume that native add must
retain equivalent entities as separate rows.

Python 3.14.7, twelve workers, pytest-receptor: 76 composition tests pass separately
with development pandas 2.3.3 and the existing pandas 3.0.6 overlay. No obsolete-copy
warning is present; ordinary legacy H5MSM, box/drop-policy and unit-test warnings
retain their behavior. Commands:

```bash
python -m pytest -n 12 --receptor=llm \
  tests/form/molsysmt_Topology/test_composition_pandas_compatibility.py \
  tests/basic/merge tests/basic/add
# Same existing interpreter and selection, with the pre-existing pandas-3 package:
PYTHONPATH=/tmp/molsysmt-s5-pandas3 python -m pytest -n 12 --receptor=llm \
  tests/form/molsysmt_Topology/test_composition_pandas_compatibility.py \
  tests/basic/merge tests/basic/add
```

Ruff and developer-guide validation pass. No version floor or public artifact changes.
