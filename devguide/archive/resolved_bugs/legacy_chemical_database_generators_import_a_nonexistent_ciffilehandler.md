---
summary: Legacy chemical database generators import a nonexistent CIFFileHandler
issue: uibcdf/molsysmt#368
status: resolved
opened: 2026-10-10
closed: 2026-10-10
severity: low
verification: reproduced
area: [data, form]
guard: tests/data/databases/test_ccd_generators.py
normative:
blocked_by: []
supersedes: []
---

# Legacy chemical database generators depended on a nonexistent native CIF parser

**Reported:** 2026-10-10, final adapter-delivery audit for uibcdf/molsysmt#139.
**Status:** Resolved as bounded maintenance before 1.0; distributed database
assets are unchanged.

## What

The standalone regeneration scripts under `molsysmt/data/databases/amino_acids/`,
`ions/`, `saccharides/` and `small_molecules/` imported the nonexistent
`molsysmt.native.CIFFileHandler`. All four used its legacy `parse()` interface.
Their imports failed even for `--help`, preventing maintenance of the reference
tables. Loading the existing packaged databases was a separate route.

## How

The missing class's placeholder form registration was retired under #139, but
that runtime repair did not repair the scripts. Their expected category mapping
also differed from the existing coordinate converter, which returns the first
mmCIF container rather than traversing a complete chemical-component dictionary.
Legacy classification assumed quoted values, present type families, implicit
GROMACS paths and current-directory output. Ion supplements used a schema
incompatible with the current indexed ion readers.

## Why

Reference-data maintenance needs a reproducible route using all CCD blocks and
explicit sources. Restoring a public placeholder handler would not supply that
contract. The maintainer admitted bounded repairs including post-1.0 issues
after the original runtime audit; this is maintenance tooling, not a new
scientific feature or release-candidate qualification.

## Resolution

All four entry points delegate to a shared private tool in
`molsysmt/data/_make/_chemical_group_database.py`. It reuses the existing hard
dependency `mmcif.io.IoAdapter`, with parser exceptions enabled and strict
encoding, for the three relevant categories across all containers. Incomplete
category rows are rejected explicitly because the parser can return a final
incomplete row without raising a syntax exception.

Inputs and output directories are mandatory and explicit; optional RTP/JSON
sources are explicit too. Imports are inert, nonempty destinations are refused,
and parser scratch is managed. Canonical/alternate name graphs preserve source
atom order, missing aliases fall back, and malformed connectivity is rejected
before writing. The legacy family partition is retained, with unquoted type
handling and valid empty-family indexes. Supplemental ion records are normalized
to the current `atom_name`/indexed-`bonds` schema; incompatible positional graphs
are rejected.

Sorted bucket contents, fixed pickle/compression settings and zero gzip timestamps
produce repeatable bytes in the same environment. The completion manifest records
input/output hashes, generator/profile and producer versions and the allowlist.
The maintained [generation guide](../../chemical_group_database_generation.md)
defines commands, schemas, resource custody and review before asset replacement.

## What is measured and what is assumed

Before repair, the four CLI generation cases and four direct-script help cases
failed with the missing-handler import (**8 failures**). After repair:

```bash
python -m pytest tests/data/databases/test_ccd_generators.py --receptor=llm -n12
```

**39 passes**, Linux/Python 3.14.7, mmcif 1.1.1, 2026-10-10. The small CCD
fixture exercises multiple blocks, quoted/multiline values, singleton categories,
case-insensitive types and aliases. Existing group readers deliver the independently
expected bonds, including reordered external atom indices. Tests also cover
explicit RTP/JSON, installed ion aliases, gzip input, empty families, unsafe group
names, malformed graphs/rows, inert imports, preservation of caller outputs,
and byte/hash reproducibility. A bundled real MSE CCD record retains its
`CG`–`SE` and `SE`–`CE` connectivity.

The guard fails if any entry point again imports the nonexistent handler, selects
only the first component, breaks reader schemas or writes on malformed input.
These are contract tests, not scientific validation or performance measurements
of a full regenerated CCD database. All parser containers are materialized with
selected categories; bounded-memory full-CCD streaming is not claimed.

The changed Python files pass Ruff checks and formatting. The fast release gate
passes **14/14** (including dependency, devguide, course and public-API smoke
checks). No heavy source/installed matrix or release operation is executed.

## What was refuted

- The placeholder form could not implement the absent parser.
- Reusing the first-container coordinate conversion would omit CCD components.
- Silent parser error suppression could admit partial input; strict parsing and
  explicit row validation are required.
- Accepting every installed supplement without validation would copy two MET
  graphs with an undeclared OXT endpoint. That independent source-data defect
  remains tracked in uibcdf/molsysmt#380; invalid supplements are refused.

## Scope and exclusions

No distributed `.pkl.gz` files, group inventories, chemical-state stores,
scientific models or public runtime function signatures changed. No new dependency
or public parser form was introduced. No full CCD was downloaded or regenerated.
Output writes are not a directory transaction: an I/O failure may leave files in
its explicit destination without a completion manifest.

## Acceptance criteria

- All four entry points have a usable, documented CCD regeneration route.
- Real multi-container parsing and existing-reader delivery are contract-tested.
- Reproducibility, provenance, optional sources and malformed-input rejection are
  protected by an addressable guard.
- Corpus regeneration and unresolved MET chemistry remain separately scoped.

## Provenance

Original audit based on d47b528dabc0a68bf0ce90660b6c3a71701e674c; repair started
from 889b3b4fe0ddac4a24105b49a58d3321e8708045. Linux/Python 3.14.7 and mmcif
1.1.1 on 2026-10-10. Related runtime repair: uibcdf/molsysmt#139.
