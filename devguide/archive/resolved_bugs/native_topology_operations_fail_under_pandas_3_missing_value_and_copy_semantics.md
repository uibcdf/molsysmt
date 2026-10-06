---
summary: Native topology operations fail under pandas 3 missing-value and copy semantics
issue: uibcdf/molsysmt#343
status: resolved
opened: 2026-10-06
closed: 2026-10-06
severity: high
verification: reproduced
area: [attribute, form, deps]
guard: tests/form/molsysmt_Topology/test_set_topological_attributes.py
normative:
blocked_by: []
supersedes: []
---

# Native topology operations fail under pandas 3

**Reported:** 2026-10-06, during #334 stabilization triage.
**Status:** Resolved; local qualification and remaining release limits are recorded below.

## What

A focused Python 3.14/pandas 3.0.6 selection reproduces 16 failures among 261
cases in existing native PDBQT, peptide-candidate and topology workflows.
The public pandas requirement admits this version. Unknown group names reach
boolean membership checks as `pd.NA`; partial missing chain assignment fails in
an `int64` column; grouped setters write into read-only NumPy views; and one
scientific result aborts under warnings-as-errors on a deprecated concat argument.

## How

The shared group-name classifier now retains unknown names as `unknown` before
chemical name membership checks. No name or chemistry is invented. Partial atom
chain updates normalize the column to the native nullable `Int64` schema.

The four affected grouped setters request writable arrays explicitly with
`to_numpy(copy=True)`, instead of copying a Series whose NumPy export is still
read-only under pandas 3. The canonical bond-table concatenation stops supplying
the deprecated `copy` keyword. Existing independence guards remain applicable.

An intermediate correction leaves two failures: default nullable NumPy export
turns the missing chains into distinct floating NaNs and the known chain into a
float, which misreports membership and blocks an otherwise valid group.
Atom/group chain-index getters now explicitly export object values with unknown
membership represented by `None`; known positions remain integers. Their
docstrings state those existing semantics. No peptide criterion is changed.

## Why

These are supported-input correctness defects, rather than new chemistry or
reconstruction capabilities. Version-dependent missing membership can incorrectly
suppress a peptide candidate or prevent loading a stored docking result. A copy
must be writable when a setter uses it for controlled updates.

## What is measured and what is assumed

**Reproduced:** initial selection: 16 failed, 245 passed, no skips, 18.76 s,
133 warnings. Intermediate selection including the integration and new missing-name
guards: two failed, 269 passed, no skips, 19.11 s, 21 warnings. Final pandas 3
selection: 271 passed, no failures/skips, 17.90 s, 21 warnings. Same final selection
on pandas 2.3.3: 271 passed, no failures/skips, 18.57 s, 11 warnings.

The final pandas 3 warnings include eleven legacy-file diagnostics and ten existing
concat-copy deprecations in native `add`. No global warning-free claim is made.
Timings describe these tests, not a benchmark. No new dependency was added:
pandas 3 was installed only in a temporary test target.

## What was refuted

- A copied pandas Series does not guarantee a writable exported NumPy array.
- Nullable column storage alone does not preserve public index types: its default
  export can turn known integers into floats and absence into repeated NaNs.
- Filtering the warning or weakening the peptide/PDBQT assertions would hide
  the original errors. Existing independent inventories/selection expectations stay.

## Scope and exclusions

Existing scalar name inference, membership setters/getters and canonical bond
concatenation. No schema, public signature, unit, scientific cutoff, method or
input-chemistry expansion. Full pandas 3 suite/artifact qualification remains #237
and #334 work. Residual native-add warnings are visible in the receipt.

## Acceptance criteria and resolution

The topology setter module guards the writable-array paths and existing membership
assignments. Additional guards in `tests/build/get_missing_bonds/test_peptide_candidates.py`,
`tests/build/test_get_peptide_bond_candidates.py`,
`tests/element/group/test_get_group_type_slow_paths.py`,
`tests/build/test_assign_autodock_atom_types.py` and the real-Vina PDBQT module
protect unknown membership, missing-name inference and scientific/persistence
results. All pass under both pandas versions without weakening their expectations.
Applicable Ruff, docstring and developer-guide gates must pass.

The additional native composition/rich-bond selection passes 51 cases without
skips under pandas 3 in 11.49 s. It checks source-independent copying, state
storage, extraction and bond operations; eighteen existing native-add concat
warnings remain visible. The fourteen fast gates, changed-file Ruff/format and
public docstring validator pass. These checks do not qualify every pandas 3 route.

## Reproduction and provenance

The complete local run uses Python 3.14.7 with NumPy 2.4.6, pandas 2.3.3 and the
released providers retained in the S5 source receipt. The compatibility selection
changes only pandas to 3.0.6, preserving NumPy and those provider sources. All pytest
runs use `--receptor=llm -n 12` with BLAS/OpenMP threads limited to one per worker.
The [execution receipt](../../../devtools/data/stabilization_s5_execution_20261006.json)
retains actual exits, counts, failing/skipped nodes, log/JUnit digests, both pandas
selections and source checksums. Example reproduction:

```bash
python -m pytest --receptor=llm -n 12 \
  tests/test_dependencies_architecture.py \
  tests/element/group/test_get_group_type_slow_paths.py \
  tests/build/test_assign_autodock_atom_types.py \
  tests/form/file_pdbqt/test_real_vina_examples.py \
  tests/build/get_missing_bonds/test_peptide_candidates.py \
  tests/build/test_get_peptide_bond_candidates.py \
  tests/form/molsysmt_Topology/test_set_topological_attributes.py \
  tests/physchem/test_get_autodock_atom_types.py
```

Linux local editable development, 2026-10-06. This is not a green complete suite,
zero-skip installed-artifact certificate, eight-cell matrix or 1.0 release approval.
