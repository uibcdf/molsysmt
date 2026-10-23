---
summary: PDB file identity conversion rejects the standard output filename
issue: uibcdf/molsysmt#422
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: medium
verification: reproduced
area: [form, convert]
guard: tests/form/file_pdb/test_identity_conversion.py
normative:
blocked_by: []
supersedes: []
---

# PDB file identity conversion rejects the standard output filename

**Reported:** 2026-10-22, during the local PDB execution expansion of uibcdf/molsysmt#181.
**Status:** Resolved; direct/public routes and value or resource contracts pass.

## What

`file:pdb -> file:pdb` rejects `output_filename` with `UnknownArgumentError`. Its `output_name` fallback is also passed to an extractor that accepts only `output_filename`.

```bash
python -m pytest tests/conversion_truth/test_declared_pdb_edges.py --receptor=llm -n 12
```

The initial correctly constructed 32-edge profile gives four failures and
28 passes. Those failures comprise this report and the other PDB reports
uibcdf/molsysmt#422, uibcdf/molsysmt#423 and uibcdf/molsysmt#424.

## How

Use the canonical destination keyword throughout; preserve `output_name` as a keyword-only compatibility alias, reject conflicting destinations and declare the alias optional for public dispatch.

## Why

A local file copy through the documented public conversion dispatcher cannot complete.

## What is measured and what is assumed

Runtime failures are reproduced with tiny local sources, normal argument digestion
and installed providers. The profile stops at the first failing direct call;
separate mirrored regression tests exercise direct and public routes explicitly.
No full PDB-field or independent chemical accuracy certification is claimed.

## What was refuted

Missing optional packages are not the cause. MDTraj and OpenMM are installed.
Two initial harness mistakes (a nonexistent root-level handler export and rejecting
valid HETATM records) were corrected before the four runtime defects were counted.

## Scope and exclusions

Repair the registered route and preserve its documented selection and unit semantics.
No new parser, chemical inference policy, file format or release qualification.

## Acceptance criteria

- The affected direct and public conversions complete with valid local input.
- Values or file content, not only returned forms, are checked in `tests/form/file_pdb/test_identity_conversion.py`.
- The complete PDB execution profile passes without runtime-failure skips.

## Provenance

Linux x86_64, Python 3.14.7, MDTraj 1.11.1 and OpenMM 8.6.1,
2026-10-22, starting from source commit fe5036c1f4c145ec2eecf1627e80eb70fc995618.
Provider versions will be checked in the final execution receipt.

## Resolution and verification

The bounded PDB execution profile passes all 32 edges directly and publicly.
The final profile/repair run passes 175 cases (no skips/failures, 18.15 seconds),
plus one separate executor-partition control. The broader PDB/native topology/
Modeller/conversion regression passes 2,284 cases with no skips/failures in
98.67 seconds. Six changed-adapter doctests pass. Three affected User Guide/
course notebooks execute successfully; source-level evidence does not qualify
an installed release candidate.

The full commands, environment and limits are in the
[execution receipt](../../../devtools/data/conversion_execution_pdb_20261022.json).
The guard above executes the affected behavior; additional mirrored native and
Modeller tests compare atom names, selected positions, physical units and source
ownership. Resource guards check actual paths after return, errors and interruption.

## 2026-10-22 correction — retain the original positional signature

The ordinary CI run [39879357399](https://github.com/uibcdf/molsysmt/actions/runs/39879357399)
correctly rejected d7b03450f at the parent-signature gate: although both keyword
spellings and positional calls worked, the legacy positional parameter name had
been replaced by `output_filename`. The local 14 fast gates did not include this
parent comparison; their passing result was not a passing CI result.

The follow-up restores `output_name` in its original fourth positional slot and
adds `output_filename` only as a keyword-only parameter. This supersedes the
keyword-only-alias design stated above. A function-specific registry waiver
records the intentional additive keyword/restoration; no validator is weakened.
The regression module executes the full legacy positional call as well as both
keyword routes, and checks the preserved positional boundary. Parent comparisons
are run both against the failed commit and the original pre-change API. The
broader runtime results above remain applicable to the unchanged conversion body;
the destination contract and doctest are rerun for this follow-up.
