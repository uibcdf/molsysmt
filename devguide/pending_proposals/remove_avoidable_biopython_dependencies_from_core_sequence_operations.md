---
summary: Remove avoidable Biopython dependencies from core sequence operations
issue: uibcdf/molsysmt#243
status: partial
opened: 2026-09-24
closed:
verification: reproduced
area: [form, convert, build, deps]
guard:
normative:
blocked_by: []
supersedes: []
---

# Remove avoidable Biopython dependencies from core sequence operations

**Reported:** 2026-09-24, while preparing the native peptide builder as the
default route on Python 3.14.
**Status:** Partial; elementary conversion is native, broader audit remains.

## What

Keep simple peptide-sequence recognition and code conversion available without
Biopython, while retaining optional Biopython object adapters, relevant
sequence I/O, and Biopython as an independent comparison oracle. Audit every
remaining use of `Bio` and classify it by whether its capability truly needs
the external package.

## How

The current `string:amino_acids_1` detector already uses a local standard
alphabet. Its one-to-three-letter converter alone wraps
`Bio.SeqUtils.seq3` in `@dep_digest("Bio")`. The first increment centralized
MolSysMT's existing one- and three-letter residue table under
`molsysmt/element/group/amino_acid/codes.py`, reused it in this converter,
FASTA/PIR attribute getters, and the FASTA topology path, and tested
conversion with and without Biopython. The bundled amino-acid database
contains topology templates and variant names, not this code table; its data
files remain unchanged.
Keep the Biopython `Seq`, `SeqRecord`, and `PDBStructure` forms optional; do
not silently reimplement the complete FASTA/PIR or pairwise-alignment
contracts in the same patch. Review those routes separately for value,
semantic parity, and a clear missing-dependency error.

## Why

On Linux/Python 3.14.7 without Biopython, `msm.get_form("GG")` returns
`string:amino_acids_1` and native `build_peptide("AceAlaNme")` yields 22
atoms and three groups. Yet
`msm.convert("GG", to_form="string:amino_acids_3")` raises
`LibraryNotFoundError` for `Bio`. That one elementary conversion prevents
the native builder from accepting common one-letter inputs in a lean
installation. Biopython itself implements `seq3` by a small residue-code
lookup, whereas MolSysMT already has the inverse table and another duplicate
forward table in the FASTA topology adapter.

## What is measured and what is assumed

The three original behaviors above were run in the disposable lean
Linux/Python 3.14.7 environment `/tmp/molsys-pair-py314.D81IYq/env` on
2026-09-24. After the converter change and missing-dependency guard, its
seven focused tests yielded four passes and three Biopython-oracle skips in
7.98 seconds with 12 workers.
The dependency-rich Python 3.14.7 environment passed 168 selected peptide,
sequence-form, and FASTA tests in 19.85 seconds with 12 workers and
`--receptor=llm`; the selections include the Biopython comparison cases.
After centralizing the remaining FASTA/PIR attribute maps, 38 focused
amino-acid-code, sequence, FASTA, and PIR cases passed in 10.80 seconds. The
new simulated missing-Biopython test guards the same elementary conversion
and default builder even when Biopython happens to be installed in the test
environment.
The offline-safe `tests/build/` selection passed 371 cases in 68.07 seconds;
the separate extended LEaP comparison passed 40 cases in 17.31 seconds.
The converter and Biopython's `Bio/SeqUtils/__init__.py` and
`Bio/Data/IUPACData.py` were inspected on that date. The Biopython checkout
was `08fc09086`. The wider importance of making FASTA/PIR parsing or
alignment independent of Biopython is not yet measured.

## What was refuted

Core string recognition is not currently dependent on Biopython; replacing
the detector is not required for this first increment. Two new native
sequence classes are also not required to replace a table lookup. Their
possible future value is tracked in `uibcdf/molsysmt#242`. Eliminating all
Biopython support would remove useful external interoperability and an
independent sequence-code reference; that is not proposed.

## Scope and exclusions

The first increment covers the one-to-three-letter converter, table
deduplication, and tests. The subsequent audit covers FASTA/PIR paths,
`get_sequence_alignment`, and Biopython-native form adapters, but it must
preserve each feature's behavior or document why it remains optional. LEaP
is unrelated to the sequence-code dependency and remains an independent
topology/geometry oracle for `build_peptide`.

## Acceptance criteria

- One-letter to three-letter conversion and default native peptide building
  work without Biopython for supported standard residues; case behavior,
  ambiguous symbols, unknown symbols, and explicit prefixes have tests.
- A Biopython-present test compares the intended common code domain with
  `Bio.SeqUtils.seq3`; Biopython object conversions remain tested and optional.
- Every `Bio` import or dependency declaration is classified as essential
  interoperability, an optional advanced feature, or an avoidable core use.
- Any FASTA/PIR or alignment replacement is scoped and validated separately;
  this issue does not close merely because one converter changed.
- The dependency specification and user documentation agree with the final
  classification. An addressable test guards the core dependency boundary.

## Dependencies and risks

Changing the code table can alter treatment of lowercase, ambiguous codes,
unknown characters, and the termination marker. Preserve the established
public conversion behavior where valid and make structural-builder errors
explicit; do not turn an undefined residue into a fabricated atomic model.
