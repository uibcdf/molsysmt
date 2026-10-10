---
summary: CHARMM CRD metadata delivery and native IDs violate adapter contracts
issue: uibcdf/molsysmt#364
status: resolved
opened: 2026-10-09
closed: 2026-10-09
severity: medium
verification: reproduced
area: [form, convert, attribute]
guard: tests/form/file_crd/test_get_file_crd.py
normative:
blocked_by: []
supersedes: []
---

# CHARMM CRD metadata and subset conversions

**Reported:** 2026-10-09, bounded pre-1.0 triage of uibcdf/molsysmt#139.
**Status:** Resolved; metadata delivery, native IDs and subset conversions repaired.

## What

The CRD adapter advertises nine topological attributes without compatible
getters or a usable pipe. For example:

```python
msm.get(molsys, element="atom", atom_index=True)
```

raises `NotWithThisFormError`. Its native Topology converter succeeds on bundled
POPC but stores NumPy integer atom/group/chain IDs. The three native converters
also ignore their atom selections, and Structures/MolSys ignore structure
selections, including a request for zero structures.

## How

The adapter initializer disables topological piping twice. Its native conversion
already delivers the metadata but assigns integer ID arrays and returns the full
object without extracting the requested subset.

- Declare the existing native Topology as the topological pipe; remove duplicate
  assignments that would overwrite it.
- Add a positional-only atom getter reusing the existing header-count tool.
- Normalize atom, group and chain IDs to string labels during table construction.
- Delegate subsets to existing native extraction. A combined MolSys is built on
  full axes before extracting topology and coordinates together, avoiding double
  selection or divergent atom ordering.
- Keep native topology/MolSys sorted atom order and coordinate-only Structures
  requested order, as in their existing contracts.

No new parser, public extraction utility, chemical store or optional engine is
introduced. Metadata interpretation and physical coordinate conversion reuse
existing tools and PyUnitWizard.

## Why

Clients cannot obtain declared metadata or trust selected output axes. Integer
IDs violate the native label invariant. Selecting topology and coordinates
independently after sorting only one axis could silently misassign positions;
combined native extraction prevents that mismatch.

## What is measured and what is assumed

The original bundled POPC conversion returns integer IDs for all three tables.
Two independent tiny fixed-width fixtures describe three atoms, two groups and
two chains, with analytical angstrom coordinates, in standard and extended CRD.
The initial test run has 32 failures and one pass: 20 missing-delivery cases,
six ignored atom-subset cases, four ignored empty structure-selection cases,
and two integer-ID cases. Both fixtures parse successfully; these are contract
failures, not malformed input.

The final CRD selection passes **47 tests and four doctests**. Controls cover
all nine restored attributes, upward group mappings, string IDs, nonconsecutive
and repeated query positions, metadata/coordinate alignment, selected conversion
axes, empty atom/structure selections, header-only access without topology
conversion and an angstrom/fs/degree application policy restored after use.
The combined FASTA/PIR/CRD run passes **93 cases**, without skips or warnings:

```bash
python -m pytest --receptor=llm -n 12 tests/form/file_crd tests/form/file_fasta tests/form/file_pir molsysmt/form/file_crd/get_topological_attributes.py molsysmt/form/file_crd/to_molsysmt_Topology.py molsysmt/form/file_crd/to_molsysmt_Structures.py molsysmt/form/file_crd/to_molsysmt_MolSys.py molsysmt/form/file_fasta/get_topological_attributes.py molsysmt/form/file_pir/get_topological_attributes.py
python devtools/scripts/validate_form_adapters.py
```

After #363 and this repair, the audit reports 60 remaining undelivered attributes
across three forms, down from 73 across six. All 96 adapters pass structural
checks and the delivery ratchet. These are dated observations, not completeness
claims or performance measurements.

## What was refuted

Simply enabling the pipe would expose integer native IDs and leave conversion
selection errors intact. Applying the same atom subset independently to topology
and coordinates would disagree on order. Existing native extraction provides
the required contract without copying a remapping implementation into the parser.
A dense or compiled representation is unnecessary for this bounded file adapter.

## Scope and exclusions

Existing advertised metadata and native subset conversions only. No generalized
CHARMM dialect expansion, bond inference, timing/box invention or force-field
assignment. This does not certify absent connectivity or complete chemical
states. Atom-name/group-name type interpretation is the existing heuristic,
not a new chemistry method. Broader #139 debt remains open.

## Acceptance criteria

Metadata queries retain source positions and units, native IDs are strings,
selected MolSys topology/coordinates align and empty selections remain empty.
Remove only the nine resolved CRD baseline bits. Keep corresponding User Guide,
Toolbox, Cookbook, course and public converter docstrings accurate.

## Resolution

The guard checks actual public queries/conversions and analytical coordinate
truth for both fixture variants; it cannot pass merely by adding method names.
Four converter/getter doctests use bundled local POPC. Documentation notebooks
receive prose-only edits, preserving code cells and saved outputs. This runtime
repair is bounded stabilization during the release pause: frozen producer refs,
artifacts, hashes and qualification results are unchanged; a replacement release
candidate will need its applicable qualification.

## Provenance

Linux shared development environment, Python 3.14.7, NumPy 2.4.6, pandas 2.3.3,
2026-10-09. Original source: `aa18b0e2a70802b9e4ede3e219484e52b9548c5e`.
Local receipts: `/tmp/molsysmt-364-before.xml`,
`/tmp/molsysmt-363-364-final.xml`, `/tmp/molsysmt-363-364-adapters.log`.

## Local completion gates

The 14 fast release checks pass, including dependency boundaries, form delivery,
report lifecycle and course structure. Ruff check and format verification pass
for the repository. This is source-scoped evidence; no full scientific matrix,
installed artifact qualification or publication decision is claimed.
