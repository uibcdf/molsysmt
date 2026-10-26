---
summary: PDB split DBREF parsing reads a nonexistent chain_id field.
issue: uibcdf/molsysmt#474
status: resolved
opened: 2026-10-26
closed: 2026-10-26
severity: medium
verification: reproduced
area: [form, native]
guard: tests/native/test_pdb_split_dbref.py
normative:
blocked_by: []
supersedes: []
---

# PDB split DBREF parsing reads a nonexistent chain_id field

**Reported:** 2026-10-26, while obtaining original local PDB inputs for
uibcdf/molsysmt#468 and uibcdf/molsysmt#469.

## What

Public native reading of the original RCSB 5XJH and 6EQE files fails at the
split DBREF1/DBREF2 metadata records with AttributeError. The existing record
stores chainId, but the paired-record check reads chain_id. These ordinary
files use a long UniProt accession represented by the standard two-line form.

## How

Use the existing external chainId field consistently in the parser's pairing
check. Keep the original source records, long accession, ranges and chain
label. Missing or mismatched second records must retain FileContentError;
metadata must not be stripped to bypass the defect.

## Why

This is a shared format reader defect preceding coordinates and bond inference.
It blocks deterministic geometry fixtures and the original PETase course
source. Changing a neighbor calculation or consumer cannot repair this parser.

## Acceptance criteria

Minimal fixed-column valid pairs retain exact metadata across text, list,
stream and public file-handler paths. Public MolSys conversion preserves string
IDs and coordinates without source mutation. Missing DBREF2 and wrong-chain
pairs raise FileContentError, not AttributeError. Read the original downloaded
5XJH/6EQE sources unchanged when qualifying their offline fixtures.

## Source evidence

RCSB PDB sources: https://files.rcsb.org/download/5XJH.pdb and
https://files.rcsb.org/download/6EQE.pdb. Original bytes, URLs and hashes are
retained in the related offline-fixture receipt. No provenance or physical
preparation is inferred from these metadata.

## Resolution — 2026-10-26

The paired-record check now reads the existing external `chainId` field. No
record schema, coordinate, connectivity inference or public signature changed.

**Contract-tested:** the focused guard reproduces eight failures and four
passing malformed-input controls before the repair. All 12 pass afterwards;
together with both existing PDB handler modules, **74 tests pass** using
`python -m pytest tests/native/test_pdb_split_dbref.py
 tests/native/test_pdb_file_handler.py
 tests/native/test_pdb_file_handler_extended.py --receptor=llm -n 12`
(4.77 seconds, exit 0). The guard checks literal metadata, string identifiers,
nanometer coordinates, unchanged source text and typed malformed-pair errors.

The unchanged original 5XJH neighbor regression was also executed with only its
input redirected to the byte-identical downloaded PDB: its original atom-index
pairs and all original reference distances pass. Bundling and offline lookup
remain owned by uibcdf/molsysmt#469; course repairs remain owned by
uibcdf/molsysmt#468. This parser repair does not close either consumer issue.
