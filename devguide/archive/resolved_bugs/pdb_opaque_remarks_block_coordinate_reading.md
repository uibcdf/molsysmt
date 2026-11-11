---
summary: Opaque PDB REMARK records block coordinate reading
issue: uibcdf/molsysmt#654
status: resolved
opened: 2026-11-10
closed: 2026-11-10
severity: medium
verification: reproduced
area: [form, native]
guard: tests/form/file_pdb/test_opaque_remarks.py
normative:
blocked_by: []
supersedes: []
---

# Opaque PDB comments block coordinate reading

## What

The original GHECOM export supplied by TopoMT fails through public
`get(coordinates=True)`. Its coordinate columns are readable, but the native
PDB parser applies `int` to every nonblank REMARK number field. GHECOM writes
`REMARK  COMMAND` and `REMARK  COMMENT` without numeric identifiers.
The parser also reads beyond the input when a REMARK block ends the file.

## How

The unchanged four-atom export is retained under
`tests/form/file_pdb/data/ghecom_20260817_assigned.pdb`, SHA-256
`6b5684afcfb42cd66738264ffcb6ab69a6934b0424741c1523a4c08ed20096cd`.
Its source is TopoMT commit `6ef0894f7c87b3865e729eb14d8c25e2332c4f20`,
provided in [#654](https://github.com/uibcdf/molsysmt/issues/654).
The fixture README records its original path. GHECOM's occupancy column is
provider-specific radius data; this review tests the declared coordinates.

All nine new regression cases fail on `50af447ad`: eight encounter invalid
integer fields and one reaches an out-of-bounds read. The checks cover nm and
angstrom policies, complete long comment text, numbered/opaque transitions,
CRLF input, separate comment blocks and end-of-file comments.

## Why

Opaque comments can be retained without inferring chemical or geometric
metadata. The selected behavior stores their complete payload in the native
PDB entry with `remarkNum=None`. Numbered records keep the standard message
field and grouping. Recognized REMARK 350 assembly declarations retain the
normalized reader's existing validation.

## Acceptance

The exact original export must yield the four declared coordinate triples
with length units and byte-identical input. The native handler must retain
all opaque comment payloads, including the long command. Preserve ordinary
numbered remarks and independently validated structured declarations.
Retain all failed attempts and qualify the native/parser/form routes before
closing. This adds comment tolerance to reading; it does not establish a PDB
writer roundtrip for GHECOM's provider-specific metadata.

## Resolution and validation — 2026-11-10

**Contract-tested:** the parser retains opaque remarks with a missing number
instead of inventing one or raising. It preserves separate blocks and stops
at end of input. The nine regression cases now pass; their original nine
failures remain in local JUnit evidence. Numbered remark behavior remains
unchanged for standard PDB records.

The following broader selection passes **623 cases**, including all nine
new guards, with zero failures/errors/skips:

```bash
python -m pytest --receptor=llm -n2 \
  tests/native/test_pdb_file_handler.py \
  tests/native/test_pdb_file_handler_extended.py \
  tests/form/file_pdb tests/form/file_pdb_gz tests/form/string_pdb_text
```

The existing `test_pdb_bioassembly_is_parsed_remapped_and_roundtripped` and
`test_pdb_report_exposes_malformed_charge_conect_and_bioassembly_records` in
`tests/conversion_truth/test_pdb_fidelity.py` also pass: **625 distinct passing
cases** overall. The one broader-session CrossChainCovalentBondsWarning is
retained; it does not concern opaque comment parsing.

Environment: Linux/Python 3.14.7, verified public PyUnitWizard 0.29.2 and the
reference ABI3 binary SHA-256
`4ffb82e4250a1862fff17dbe7725fb8f0770d613ffef2648370389a66983d345`.
The broader run used a bounded user systemd scope with two workers, CPU quota
200%, memory high/max 3/4 GiB and swap disabled for the scope. Host available
memory remained above 13 GiB at sampled checkpoints, with zero memory-pressure
averages. No shared-system process was stopped.

The handler docstring, Foundations, PDB Toolbox and preparation Cookbook, and
Common Core module 1 describe the retention boundary. Notebook changes affect
only one Markdown cell each; existing code, metadata and outputs are unchanged.
The two stored notebook schemas and the complete course structure pass their
validators. Focused Ruff and whitespace checks pass. This is source-level
parser receiving, not a new installed-candidate or scientific preparation claim.
