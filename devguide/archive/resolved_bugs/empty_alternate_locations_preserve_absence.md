---
summary: Empty alternate-location queries preserve absence and the structure axis.
issue: uibcdf/molsysmt#112
status: resolved
opened: 2026-10-05
closed: 2026-10-05
severity: low
verification: inspected
area: [attribute, basic]
guard: tests/basic/get/test_alternate_location_indices.py::test_empty_alternate_location_from_pdb_and_h5msm_is_none
normative:
blocked_by: []
supersedes: []
---

# Empty alternate locations preserve absence

**Reported:** Historical #112, reviewed during S1 on 2026-10-05.
**Status:** Resolved by existing reader behavior and additional public regression coverage.

## What

The original report asks for `None` instead of `[{}]` when
`msm.get(molsys, alternate_location=True)` has no alternate-site information.
The current native PDB reader already sets the attribute to `None` when all
parsed structure maps are empty. Native getters return `None` for an absent
attribute; no runtime correction was needed during this review.

## How

`form/molsysmt_PDBFileHandler/to_molsysmt_MolSys.py::_build_structures_from_content`
normalizes total absence, and the native Structures getter preserves it.
The new public guard reads a no-alternate PDB, converts it to MolSys and H5MSM
0.5, and asserts `None` at the file/object/persistence boundaries. It would fail
if an empty per-structure map again replaced absent PDB evidence.

## Why

Absence differs from a selected structure with no sites when an attribute is
stored for other structures. Existing sparse-query tests intentionally preserve
`[{}]` for that structure and `[]` for an empty structure selection. Collapsing
all empty query results to `None` would discard this distinction and the requested
structure axis. The current convention is explained in the
[chemical-template cookbook](../../../docs/content/user/cookbook/applying_chemical_templates.md).

## Verification and limits

On source `0efb14144`, the bundled Barnase-Barstar H5MSM returns `None`, as
requested. Its bundled PDB counterpart contains alternate sites for 62 atom
indices and correctly returns them; the 1BRS BCIF source contains sites for two
indices. These are different stored datasets, not a requirement to erase real
sites or infer lossless equivalence between them.

The existing 35-test naming/alternate baseline passes on Linux/Python 3.14.7.
The new guard and associated alternate/GRO selection pass in the 34-test
focused run. This is **Contract-tested** absence and sparse-query behavior,
not chemical-conformation validation or exhaustive external-form parity.

## Resolution

Retain the current absence convention, add a PDB/H5MSM regression guard and
clarify the distinction in the extraction course and maintained structures
contract. No public output shape is changed in this stabilization checkpoint.
