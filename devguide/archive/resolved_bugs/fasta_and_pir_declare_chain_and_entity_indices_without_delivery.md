---
summary: FASTA and PIR declare chain and entity indices without delivery
issue: uibcdf/molsysmt#363
status: resolved
opened: 2026-10-09
closed: 2026-10-09
severity: medium
verification: reproduced
area: [form, attribute]
guard: tests/form/file_fasta/test_positional_queries.py
normative:
blocked_by: []
supersedes: []
---

# FASTA and PIR positional queries

**Reported:** 2026-10-09, bounded pre-1.0 triage of uibcdf/molsysmt#139.
**Status:** Resolved; four advertised positional attributes are delivered.

## What

Both sequence-file adapters advertise `chain_index` and `entity_index`, but public
queries fail with `NotWithThisFormError`, even for a two-record file:

```python
msm.get(molsys, element="chain", chain_index=True)
msm.get(molsys, element="entity", entity_index=True)
```

## How

The corresponding `get_*_index_from_*` methods are absent in
`molsysmt/form/file_fasta/get_topological_attributes.py` and its PIR counterpart.
Both adapters already count records and deliver the corresponding string IDs.
Four positional getters now reuse those count tools for unrestricted queries and
preserve explicit source positions. Public validation and the existing optional
Biopython dependency remain in place. No atom topology is constructed.

## Why

A client planning against declared capabilities cannot inspect these positional
axes. Positions must remain independent of ID labels and cannot be renumbered
when querying a subset.

## What is measured and what is assumed

Before implementation, all 18 cases in
`tests/form/file_fasta/test_positional_queries.py` fail: missing public delivery
or missing direct getters. After implementation, the FASTA/PIR test directories
pass 38 cases. Controls cover both formats, chain/entity axes, all/reordered/
repeated/empty selections, dictionary alignment with IDs, ndarray and None input,
and empty files. Public docstring examples also use temporary local files.

Commands use the shared Python 3.14 environment and Pytest Receptor:

```bash
python -m pytest --receptor=llm -n 12 tests/form/file_fasta tests/form/file_pir
python -m pytest --receptor=llm -n 12 molsysmt/form/file_fasta/get_topological_attributes.py molsysmt/form/file_pir/get_topological_attributes.py
```

## What was refuted

No new sequence model or atom-level conversion is required: existing record
counts define the positional axes. IDs are labels, not substitutes for indices.
The first implementation misspelled the entity-count delegate; unrestricted and
empty-file controls caught it before publication and the delegate is corrected.

## Scope and exclusions

Four existing advertised attributes only. No new chemistry, sequence parser,
form tier or selection grammar; broader adapter debt remains under #139.

## Acceptance criteria

Public list and dictionary queries deliver source positions, preserve order and
repetitions, and return typed empty lists. Direct getters accept ndarray and None
arguments. Remove only these four baseline bits. Keep User Guide, Toolbox,
Cookbook and course prose synchronized without changing notebook code/outputs.

## Provenance

Linux, shared development environment, Python 3.14.7, Biopython 1.88,
2026-10-09. Original source checkpoint: `aa18b0e2a70802b9e4ede3e219484e52b9548c5e`.
Local JUnit receipts: `/tmp/molsysmt-363-before.xml`,
`/tmp/molsysmt-363-after.xml`, `/tmp/molsysmt-363-364-final.xml`.

## Resolution

Both format adapters pass 38 public contract/regression tests and four new
doctests. The final combined #363/#364 run passes 93 cases without skips or
warnings. User Guide, Toolbox, Cookbook and Common Core Module 08 prose reflect
the delivered positional axes; notebook code cells and saved outputs are
unchanged. Only the two resolved FASTA/PIR masks (four bits) are removed from the
accepted delivery baseline. The owning general #139 remains open.

## Local completion gates

The 14 fast release checks pass, including dependency boundaries, form delivery,
report lifecycle and course structure. Ruff check and format verification pass
for the repository. This is source-scoped evidence; no full scientific matrix,
installed artifact qualification or publication decision is claimed.
