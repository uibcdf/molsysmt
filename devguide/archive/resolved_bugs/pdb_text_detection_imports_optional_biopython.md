---
summary: PDB text detection imports optional Biopython in a clean installation.
issue: uibcdf/molsysmt#238
status: resolved
opened: 2026-09-23
closed: 2026-09-23
severity: high
verification: reproduced
area: [form, packaging, deps]
guard: tests/basic/test_get_form.py::test_string_detection_without_biopython
normative:
blocked_by: []
supersedes: []
---

# PDB text detection imports optional Biopython in a clean installation

**Reported:** 2026-09-23, during a clean Conda installation of the local
Python 3.14 MolSysMT/MolSysViewer candidate pair.
**Status:** Resolved by replacing the optional Biopython probe with an
equivalent standard-library count of canonical amino-acid letters.

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
- Measured: the guard failed in both parametrized cases before the change,
  then passed in both cases against the corrected installed `0.22.2` Conda
  artifact without Biopython. All 22 `tests/basic/test_get_form.py` cases
  passed against the corrected source.
- Measured: a second clean Linux/Python 3.14.7 environment installed exact
  local `molsysmt=0.22.2` and `molsysviewer=0.23.2` artifacts. The
  installed-pair validator and 99-export Rust validator passed. Without
  Biopython, `get_form` classified the four-atom PDB text, `convert` built a
  four-atom `MolSys`, and `MolSysView.load` retained four atoms.
- Not measured: other installed-package Viewer pytest modules in this
  environment. Its `tests/conftest.py` explicitly inserts the source tree
  into `sys.path`; disabling that conftest leaves its `_test_message_log`
  fixture absent. Thus the two original Viewer test functions cannot serve
  as installed-package evidence unchanged. `uibcdf/molsysviewer#82` owns
  the broader installed-package gate.

## What was refuted

- The failure is not a Conda solver or Python ABI problem: the exact pair
  installed, its package validator passed, and the Rust extension imported.
- A source-tree-shadowing explanation was tested by disabling pytest project
  configuration and conftests; the same two cases failed against installed
  packages.
- The remaining `_test_message_log` errors after the fix are test-harness
  failures, not PDB-loading failures: direct installed-package loading now
  succeeds. The original tests require the source-only autouse fixture.

## Scope and exclusions

Repair the core string-form detector without making Biopython a hard
dependency. Do not change Biopython-backed converters or declare the whole
Python 3.14 pair ready for release on the strength of this fix.

## Acceptance criteria

- Core `get_form` detects PDB text and an unprefixed one-letter amino-acid
  sequence when Biopython is unavailable.
- A clean installed-pair smoke loads PDB text through MolSysViewer without
  Biopython and preserves its atom count.
- The regression test fails if the detector again imports optional Bio.

## Provenance

Linux x86-64, Python 3.14.7, local candidate Conda packages built from
MolSysMT `b054012c9` (failing `0.22.1`) and `639892a6f` (passing `0.22.2`),
and MolSysViewer `35fb2698` (`0.23.2`) on 2026-09-23. The corrected installed
MolSysMT archive has SHA-256
`d7d421c831b92fba424c665f7adb209f41e9a4f175208acfc017172d132be353`;
the Viewer archive has SHA-256
`ea64e225001537b059791f610954f99d9d022b1221e6788e085469f992bad712`.
Both installed Conda records point to the indexed local channel with these
exact hashes, not to the remote staging label.
