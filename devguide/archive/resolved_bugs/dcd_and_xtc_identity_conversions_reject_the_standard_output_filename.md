---
summary: DCD and XTC identity conversions reject the standard output filename
issue: uibcdf/molsysmt#502
status: resolved
opened: 2026-10-27
closed: 2026-10-27
severity: medium
verification: reproduced
area: [form, convert]
guard: tests/conversion_truth/test_declared_trajectory_edges.py::test_trajectory_identity_uses_owned_copy_and_rejects_source_alias
normative:
blocked_by: []
supersedes: []
---

# DCD/XTC file conversion argument and ownership failures

**Reported:** 2026-10-27, while executing the coordinate slice of #181.
**Status:** resolved; correction, compatibility and source-preservation guards pass.

## What

Both declared file identity converters use output_name, while public convert
and their own extraction functions use output_filename. The first twelve-edge
execution run fails the two file-identity cases with UnknownArgumentError and
passes ten others. Even using the legacy keyword delegates it to a function
that does not accept it. Omitted destinations can attempt a same-file copy.

## How

`to_file_dcd` and `to_file_xtc` have mismatched signature/delegation. Their
public optional-keyword admission also needs the maintained generated converter
argument table and local _conversion_opt_kwargs to allow an omitted destination.
The existing general copy_file helper already owns independent destination
validation, process-owned temporaries and failure cleanup; reuse it.

Inspection of the selected-writing branch additionally shows DCD opening output
before its input (unsafe for a same-path output), mutating the digested structure
list and indexing an atom subset on the structure axis. XTC subset extraction
raises NotImplementedError. These do not justify claiming supported subset-file
serialization. The bounded correction rejects those file-writing subsets before
writes, while retaining working selected native/H5MSM conversion.

## Why

Declared file identity routes should accept the common destination contract and
must not damage input data. Returning selected coordinates in a native object
is separate from implementing a trajectory writer and its header/time policy.

## What is measured and what is assumed

Initial command: `python -m pytest tests/conversion_truth/test_declared_trajectory_edges.py --receptor=llm -n 12`:
two failed, ten passed in 14.09 s. Subsequent directed tests confirm default
public admission requires the generated table and optional-keyword declaration.
No source-data corruption is executed on user files; unsafe old ordering follows
from source inspection. Regression guards require unchanged source/destination
bytes on refusal. A first test assertion assumed resident-native atom sorting;
the coordinate reader contract retains requested atom-list order and the oracle
is corrected accordingly. Another first test supplied an incomplete standard-unit
policy to a legacy H5MSM writer; the final test replaces length while retaining
all other standard dimensions. Neither test setup issue is claimed as a defect.

## Scope and exclusions

Standard output_filename with the original positional output_name alias retained;
whole-file copy/extract ownership; early subset-file
refusal; no new decoder, generic copy store or scientific algorithm. Existing
ArgDigest, file-destination helpers and optional MDTraj boundaries remain owned
by their original modules. No new attribution boundary or dependency is needed.
Open-reader cloning stays explicitly deferred under #181, not an expected failure
hidden in the newly selected twelve edges. Large-file writing, unusual DCD
variants, time conventions and header reconstruction remain unqualified.

## Acceptance criteria

Both direct and public file identities execute, default copies are independent,
explicit source aliases reject, whole bytes are retained, unsupported subset
writes leave both files unchanged, and native/H5MSM selected values/units remain
correct. Existing argument-generation, file-copy and conversion regressions pass.
Close with the addressable positive/ownership guard and exact qualification.

## Provenance

Linux/Python 3.14 shared development environment, MDTraj 1.11.1, source basis
f9ca3e1b0328d2463492f0969fec6805dfc7ca5b. No clean-installed, cross-platform,
performance, full-graph or release qualification is claimed.

## Signature decision

The signature guard rejected replacing the original positional output_name slot.
The final repair follows the existing PDB identity-converter precedent (#422):
retain all positional arguments/defaults and add only keyword-only output_filename.
Both aliases work separately; specifying both rejects before any write. The two
function-specific stability entries name #502 and the real positional/keyword
copy/conflict guard. This is not a waiver for arbitrary future signature changes.

## Resolution and qualification — 2026-10-27

Both direct/public file identity cases now execute successfully. The named guard
requires an independent default snapshot, byte equality, explicit no-copy identity
and source-alias refusal with unchanged source bytes. Other guards exercise the
legacy positional destination, both public keyword spellings, conflicting
keywords and refusal of unsupported subset-file serialization before writing.
Four doctests use actual bundled DCD/XTC files. The partition guard requires
execution of each selected route, not just a valid declaration.

The expanded regression passes 485 cases; the final focused/doctest run passes
38, including the additional positional cases. No skips or expected failures.
Fourteen fast gates, scoped Ruff, dependency and generated-argument controls
pass. The User Guide, two executed Cookbook blocks and Common Core course are
aligned; unchanged notebook code/output cells are preserved. See the
[qualification receipt](../../../devtools/data/conversion_execution_trajectories_20261027.json)
for exact commands, timings, source hashes, warnings and exclusions.
