---
summary: PDB text detection imports optional Biopython in a clean installation.
issue: uibcdf/molsysmt#238
status: active
opened: 2026-09-23
closed:
severity: high
verification: reproduced
area: [form, packaging, deps]
guard:
normative:
blocked_by: []
supersedes: []
---

# PDB text detection imports optional Biopython in a clean installation

**Reported:** 2026-09-23, during a clean Conda installation of the local
Python 3.14 MolSysMT/MolSysViewer candidate pair.
**Status:** Reproduced; fixing the detector and adding a regression guard.

## What

A valid PDB text string cannot be classified when optional Biopython is
absent. `molsysmt.get_form(PDB_TEXT)` raises `ModuleNotFoundError: No module
named 'Bio'`; two installed-pair MolSysViewer integration tests fail before
loading the molecule.

## How

`molsysmt/basic/get_form.py` sweeps string-form detectors in catalogue order.
The unprefixed branch of
`molsysmt/form/string_amino_acids_1/is_form.py` imports
`Bio.SeqUtils.ProtParam.ProteinAnalysis` before the PDB-text detector can
answer. Biopython is a soft dependency and is correctly absent from the
minimal Conda pair, so that detector must not make core form discovery fail.

## Why

The public `get_form` and `convert` paths, and MolSysViewer's `load`, must
work on ordinary PDB text in a clean installation. A development environment
with Biopython installed masks the error. The failure affects a core input
form despite the pair resolving, importing, and passing its package validator.

## What is measured and what is assumed

- Measured: in a clean Linux/Python 3.14.7 Conda environment containing local
  `molsysmt=0.22.1` and `molsysviewer=0.23.2` artifacts, the installed-pair
  validator and all 99 installed Rust exports passed.
- Measured: `pytest --receptor=llm -n 2 -c /dev/null --noconftest
  --import-mode=importlib
  tests/integration/test_molsysmt_integration.py` executed against the
  installed packages and failed both PDB-text cases with `ArgumentError`.
  A direct `molsysmt.get_form(PDB_TEXT)` exposed the underlying missing-Bio
  import.
- Not yet measured: whether any other clean-install input form reaches the
  same detector failure. The guard must cover the general string sweep and
  unprefixed amino-acid detection without Biopython.

## What was refuted

- The failure is not a Conda solver or Python ABI problem: the exact pair
  installed, its package validator passed, and the Rust extension imported.
- A source-tree-shadowing explanation was tested by disabling pytest project
  configuration and conftests; the same two cases failed against installed
  packages.

## Scope and exclusions

Repair the core string-form detector without making Biopython a hard
dependency. Do not change Biopython-backed converters or declare the whole
Python 3.14 pair ready for release on the strength of this fix.

## Acceptance criteria

- Core `get_form` detects PDB text and an unprefixed one-letter amino-acid
  sequence when Biopython is unavailable.
- The two installed-pair MolSysViewer integration tests pass from a clean
  Conda environment without Biopython.
- The regression test fails if the detector again imports optional Bio.

## Provenance

Linux x86-64, Python 3.14.7, local candidate Conda packages built from
MolSysMT `b054012c9` and MolSysViewer `35fb2698` on 2026-09-23.
