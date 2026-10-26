---
summary: Neighbor regression downloads an undeclared remote PDB fixture.
issue: uibcdf/molsysmt#469
status: resolved
opened: 2026-10-26
closed: 2026-10-26
severity: medium
verification: reproduced
area: [tests, data, structure]
guard: tests/structure/get_neighbors/test_get_neighbors_from_molsysmt_MolSys.py::test_get_neighbors_from_molsysmt_MolSys_8
normative:
blocked_by: []
supersedes: []
---

# Neighbor regression downloads an undeclared remote PDB fixture

## What

The eighth native MolSys neighbor regression downloads 5XJH without a network
marker. Its fixed sulfur atom-index pairs and distances should be an offline
geometry qualification, not a live archive availability test. The earlier
3,092-pass/one-failure campaign in the incoming issue remains a failed run.

## How

Replace only the remote identifier with the public bundled PETase 5XJH path.
Retain every original index and reference distance. Reject remote DNS lookup
inside the regression instead of swallowing downloader errors or skipping it.

Original archive inputs 5XJH, 6EQE, 6LU7 and 1K4C are bundled unchanged, shared
with the biological examples under uibcdf/molsysmt#468. Their byte lengths,
SHA-256, retrieval date, archive URLs and original authorship pages are recorded
in `molsysmt/data/pdb/course_sources.json`; CC0 data terms are independently
stated in `molsysmt/data/pdb/COURSE_SOURCES.md`. Software licensing is unchanged.
The explicit generator restores only matching bytes and refuses silent archive
refreshes. Routine course/tests never invoke its optional download route.

## Why

This preserves the actual scientific assertion while removing unrelated DNS
failures. A byte-pinned whole original source also preserves atom order, source
labels and metadata without inventing a reduced synthetic sulfur topology.
The original input revealed uibcdf/molsysmt#474; stripping its DBREF records
would have hidden a shared parser defect, so the parser was repaired first.

## Acceptance criteria

The unchanged original neighbor expectations pass using the bundled file with
DNS disabled. The public catalog exposes every new file with full descriptions.
Independent fixed-column coordinates, atom IDs, group IDs and chain IDs match
native conversion without altering source bytes. Regeneration preserves exact
bytes, rejects changed files and does not download implicitly. Re-execute the
automatically generated public demo-system catalog.

## Resolution — 2026-10-26

**Contract-tested:** `python -m pytest tests/data/test_course_pdb_sources.py
 tests/structure/get_neighbors --receptor=llm -n 12` passes **20 tests** in
7.66 seconds (exit 0), with nine expected legacy H5MSM warnings. The original
5XJH index pairs and distances are unchanged, and any remote DNS lookup now
fails the case. The six asset tests compare exact bytes, native coordinates and
source labels to independent fixed-column records, and exercise local restoration
and rejection of tampering/implicit download. An initial asset-test attempt used
a nonexistent group-table chain column (four test failures); the oracle now
uses the native atom-table chain indices. That test-authoring mistake did not
require changing native molecular data.

The catalog notebook was force-executed with `MSM_VIEWS_FROM_HTML_FILES=True
 MPLBACKEND=Agg python docs/execute_notebooks.py -q -n 12 -f
 docs/content/user/foundations/entrance/demo_systems.ipynb` (6.3 seconds).
All 491 notebook schema cases passed, the 14 fast release gates passed, and
Ruff check/format passed for the changed Python files. These are local source
checks, not full release, installed-pair or cross-platform qualification.

The original archive PDB sources total 1,488,213 bytes. Manifest hashes are
verified before restoration; coordinates, topology inference and neighbor
algorithms are not modified by this issue. The four separate course examples
remain tracked by uibcdf/molsysmt#468.
