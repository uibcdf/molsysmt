---
summary: Dependency architecture guard patches a removed DepDigest loader alias
issue: uibcdf/molsysmt#342
status: resolved
opened: 2026-10-06
closed: 2026-10-06
severity: medium
verification: reproduced
area: [deps, tests]
guard: tests/test_dependencies_architecture.py::test_dependencies_architecture
normative:
blocked_by: []
supersedes: []
---

# Dependency architecture guard patches a removed loader alias

**Reported:** 2026-10-06, during #334 stabilization triage.
**Status:** Resolved; local qualification and remaining release limits are recorded below.

## What

The complete local Python 3.14 suite fails in `test_dependencies_architecture`
before registry filtering is exercised: released DepDigest 0.13.0 no longer
exports `depdigest.core.loader.is_installed`. The test patches that private alias.
The network-enabled scoped retry reproduces the same `AttributeError`.

## How

DepDigest's current loader calls a shared availability checker. The integration
guard now models missing Python specs at the real discovery boundary, clears the
public `is_installed` cache and runs the real loader/checker/decorator. It asserts
that absent MDTraj is filtered while the native form remains available, a missing
required library raises MolSysMT's diagnostic, and conditional dependencies are
checked only when selected. A `finally` restores discovery, cache and both package
configurations even on assertion failure. No provider or runtime code changes.

## Why

A stale private patch prevents the integration guard from checking the supported
provider behavior and can leak temporary registry configuration after failure.
A passing test must exercise actual filtering and errors, not emulate their result.

## What is measured and what is assumed

**Reproduced:** the initial complete suite and its 68-node retry fail at this
removed alias. Both corrected 271-case selections, under pandas 2.3.3 and 3.0.6,
execute this guard successfully. Counts and artifact identities are in the shared
receipt below. These are focused editable-source checks, not installed qualification.

## What was refuted

The failure does not show that DepDigest filters incorrectly: the patch fails
before the real behavior runs. Restoring the retired provider alias or creating
a fake attribute would conceal the integration error.

## Scope and exclusions

Test integration with the supported provider. No dependency floor or scientific
method changes. Absent optional backends in the complete suite remain #237
execution/profile debt; passing this guard does not supply those backends.

## Acceptance criteria and resolution

The addressable guard executes actual registry filtering, conditional checking
and missing-library diagnostics, with unconditional cleanup. Its assertions pass
in both pandas selections. Applicable Ruff and developer-guide gates must pass.

## Reproduction and provenance

The complete local run uses Python 3.14.7 with NumPy 2.4.6, pandas 2.3.3 and the
released providers retained in the S5 source receipt. The compatibility selection
changes only pandas to 3.0.6, preserving NumPy and those provider sources. All pytest
runs use `--receptor=llm -n 12` with BLAS/OpenMP threads limited to one per worker.
The [execution receipt](../../../devtools/data/stabilization_s5_execution_20261006.json)
retains actual exits, counts, failing/skipped nodes, log/JUnit digests, both pandas
selections and source checksums. Example reproduction:

```bash
python -m pytest --receptor=llm -n 12 \
  tests/test_dependencies_architecture.py \
  tests/element/group/test_get_group_type_slow_paths.py \
  tests/build/test_assign_autodock_atom_types.py \
  tests/form/file_pdbqt/test_real_vina_examples.py \
  tests/build/get_missing_bonds/test_peptide_candidates.py \
  tests/build/test_get_peptide_bond_candidates.py \
  tests/form/molsysmt_Topology/test_set_topological_attributes.py \
  tests/physchem/test_get_autodock_atom_types.py
```

Linux local editable development, 2026-10-06. This is not a green complete suite,
zero-skip installed-artifact certificate, eight-cell matrix or 1.0 release approval.
