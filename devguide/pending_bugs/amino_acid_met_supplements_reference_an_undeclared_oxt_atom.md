---
summary: Amino-acid MET supplements reference an undeclared OXT atom
issue: uibcdf/molsysmt#380
status: open
opened: 2026-10-10
closed:
severity: low
verification: reproduced
area: [data]
guard:
normative:
blocked_by: []
supersedes: []
---

# MET supplemental connectivity contains an undeclared atom

**Reported:** 2026-10-10, validation of the restored generators under
uibcdf/molsysmt#368.
**Status:** Open; the generator rejects this input before writing. The intended
MET naming/terminal variants still need review.

## What

Both MET variants in
[`molsysmt/data/databases/amino_acids/extra.json`](../../molsysmt/data/databases/amino_acids/extra.json)
contain the bond `C`–`OXT`, but neither atom inventory includes `OXT`.
The bundled MET record also retains these inconsistent variants at positions
4 and 5. The amino-acid reader filters bonds whose endpoints are not among the
requested atoms, so this observation does not by itself demonstrate a runtime
exception or identify the chemically intended terminal variant.

## How

The generator validates that every bond endpoint belongs to its variant's atom
inventory. Explicitly supplying this legacy amino-acid supplement to the
restored route produces `ValueError: Group MET: each bond must join two declared
atoms.` No output directory is created.

```bash
python -m molsysmt.data.databases.amino_acids.make_amino_acids_db --ccd tests/data/databases/data/mini_ccd.cif --extra molsysmt/data/databases/amino_acids/extra.json --output-dir generated/met-supplement-check
```

## Why

The source cannot be incorporated into a structurally valid regenerated
reference table until the intended variants are established. Accepting the dangling
endpoint would perpetuate inconsistent reference data. The generator must not
infer whether to add an atom or delete a bond.

## What is measured and what is assumed

Inspected all eight supplemental amino-acid entries: the two MET variants are
the ones with bond endpoints outside their inventories. Loading the bundled
MET record confirms the corresponding two dangling endpoints there.
The restored generator reproduces rejection on Linux/Python 3.14.7 with mmcif
1.1.1. A synthetic equivalent in
`tests/data/databases/test_ccd_generators.py::test_invalid_amino_acid_supplement_is_rejected_before_writing`
protects rejection, not resolution of this data defect.

## What was refuted

This is not an mmCIF parse failure: the inconsistency is present in JSON and in
the previously generated pickle. The ion supplements pass the same structural
validation. Removing validation would hide the defect rather than repair it.

## Scope and exclusions

Review the intended MET atom-name/terminal variants and correct the owning
JSON source. Follow the maintained
[generation workflow](../chemical_group_database_generation.md) when replacing
affected bundled records. Do not regenerate the complete CCD corpus solely
for this correction or silently change chemical-state assignments.

## Acceptance criteria

- Establish the intended connectivity from a documented chemical reference.
- Repair the source and affected bundled data using a reproducible generation
  route, preserving unaffected variants and records.
- Add a guard checking all supplemental endpoint inventories and a specific
  expected MET graph; verify reader delivery for the corrected variants.
- Explicitly qualify any membership or terminal-chemistry changes.

## Provenance

Source inspection and real-parser rejection on 2026-10-10, Linux/Python 3.14.7,
mmcif 1.1.1. Packaged source baseline: 889b3b4fe0ddac4a24105b49a58d3321e8708045.
