---
summary: Mutation and terminal repair claims bypass the bounded native placement contract
issue: uibcdf/molsysmt#341
status: resolved
opened: 2026-10-06
closed: 2026-10-06
severity: medium
verification: reproduced
area: [build, tests, docs]
guard: tests/build/mutate/test_mutate_engine_MolSysMT.py::test_mutate_val_to_trp_keeps_unsupported_inventory_explicit
normative:
blocked_by: []
supersedes: []
---

# Mutation and terminal repair claims bypass bounded native placement

**Reported:** 2026-10-06, fresh triage of the accepted automatic full-suite
producer during the #334 stabilization freeze.
**Status:** Resolved by caller documentation and exact inventory/pose guards for
the already accepted conservative reconstruction policy.

## What

Five current tests require full native side-chain reconstruction after the
bounded provider policy adopted in uibcdf/molsysmt#322. The mutation docstring
also promises chemically complete outputs and describes the PDBFixer algorithm
as though it were the default native implementation. Native mutation can return
a named target with its backbone and unresolved side chain, with an explicit
`UnassessedResidueWarning`. Terminal capping can complete OXT while leaving
unassessed nonterminal gaps. These states need truthful caller guidance.

Reproduce the historical selection, before the contract correction:

```bash
python -m pytest --receptor=llm -n 12 \
  tests/build/add_missing_hydrogens/test_fixed_state.py::test_missing_rdkit_has_no_fallback_and_general_tools_remain_available \
  tests/build/add_missing_terminal_cappings/test_add_missing_terminal_cappings_parity.py::test_parity_1brs_total_atom_count \
  tests/build/mutate/test_mutate_engine_MolSysMT.py::test_mutate_val_to_trp_atom_count \
  tests/build/mutate/test_mutate_engine_MolSysMT.py::test_mutate_trp_has_full_indole \
  tests/build/mutate/test_mutate_molsysmt_MolSys.py::test_mutate_molsysmt_MolSys_5 \
  tests/build/mutate/test_mutate_parity.py::test_parity_trp_sidechain_present_native \
  tests/test_argument_contract.py::test_the_converter_table_still_matches_the_converters
```

## How

`build.mutate` renames target groups, removes their non-backbone atoms and calls
`add_missing_heavy_atoms`. That tool rejects multi-atom side-chain gaps through
`build._residue_repair.assess_residue`. `add_missing_terminal_cappings` also calls
the same provider before adding terminal atoms. The native policy is working as
specified; the old caller assertions and unconditional reconstruction prose did
not follow the provider contract. The hydrogen absence and converter-table
failures from the older automatic source do not reproduce in this selection.

## Why

A user must not treat a sequence label or successful terminal completion as
proof of a complete mutant or validated coordinates. Stabilization tests must
protect the offered conservative profile without reintroducing the rejected
rigid side-chain reconstruction merely to match PDBFixer atom counts.

## What is measured and what is assumed

**Reproduced:** seven selected tests on unchanged `1fb36d4ee` produce five failures
and two passes in 23.20 s, with 29 reported warnings. H-bearing AlaValPro native
VAL-to-TRP has 30 atoms versus the original 40 and lacks its ten indole side-chain
heavy atoms. Native 1BRS terminal repair yields 5,156 atoms; PDBFixer yields 5,230.
The native run reports unassessed multi-atom gaps. These are execution timings,
not a performance benchmark or independent geometric validation.

**Inspected:** uibcdf/molsysmt#327 explicitly defers ambiguous standard-side-chain
reconstruction and prohibits re-enabling the old placer to satisfy inventory
parity. The #322 real-input guard already requires native abstention.

**Assumed:** generated positions from any optional reconstruction still require
independent scientific qualification. This checkpoint does not establish
rotamer quality, clash freedom or an energy minimum for either engine.

## What was refuted

- Five failures are not five new geometry defects: the stale tests request
  reconstruction outside the accepted native coverage.
- Suppressing warnings, skipping the controls or deleting inventory assertions
  would hide the caller boundary rather than protect it.
- The current missing-RDKit and converter-table controls pass; their old failures
  remain historical evidence rather than current reproduced defects.

## Scope and exclusions

Documentation and tests of existing mutation/capping delegation. No public
signature, runtime placement algorithm, dependency, new scientific method or
fallback changes. Larger side chains remain uibcdf/molsysmt#327; modified-residue
energy refinement remains uibcdf/molsysmt#249. The #334 scope freeze is preserved.

## Acceptance criteria

Native controls must assert exact unresolved inventories, observed backbone
and untouched-group coordinates, unchanged source tables/coordinates and the
unassessed diagnostic. Keep explicit PDBFixer full-indole/LEU inventory controls.
On 1BRS protect both the exact native supported subset and remaining inventory,
plus terminal completion for both engines. Update docstrings, Foundations,
Toolbox, Cookbook and the common course. Execute targeted tests with receptor
and twelve workers, both public doctests, and the applicable local gates.

## Provenance

Linux local development, 2026-10-06, Python 3.14.7, NumPy 2.4.6, pandas 2.3.3,
RDKit 2025.09.5 and released providers SMonitor 0.18.0, DepDigest 0.13.0,
ArgDigest 0.13.0 and PyUnitWizard 0.28.1. The isolated source pins and provenance
are retained in `devtools/data/stabilization_s5_sources_20261006.json`.
The explicit Python 3.14 interpreter and those installed source directories
preceded this checkout on `PYTHONPATH`. The original JUnit receipt is
`/tmp/molsysmt-s5-remaining-failures.xml` (ephemeral local evidence).

## Resolution and local validation

The native TRP guard asserts the exact ten missing heavy names, the reported
unassessed reason, retained coordinates for the observed backbone and untouched
groups, and unchanged input atom/group tables and coordinate arrays. Its heavy-only
companion retains the same inventory. The explicit PDBFixer TRP/LEU controls
still assert complete side-chain inventories. The 1BRS terminal guard pins the
four supported nonterminal repairs, all remaining native gaps and completed
terminal inventories for both engines. No placement code changed.

The corrected selection of mutation, capping and heavy-atom tests plus the two
passing historical controls executes 87 tests without failures or skips in
63.39 s, with 111 reported warnings. These include the intentionally unassessed
gaps, attribute-loss reports and two legacy-file diagnostics. Public mutation
and capping doctests execute two tests without failures or skips in 9.26 s,
with two reported atom-parameter drop warnings. Both runs use `--receptor=llm
-n 12` and the Python 3.14 interpreter/provider setup above.

The [retained receipt](../../../devtools/data/bounded_repair_callers_20261006.json)
contains exits, JUnit digests, reproduction nodes and source checksums. Foundations, Toolbox,
Cookbook and the common course now explain partial target inventories and
engine-specific coverage. All notebook executable cells and outputs remain
byte-equivalent as parsed cells. The current course validator passes all 156
notebooks. The legacy script under `docs/content/course/devtools` was also
accidentally invoked while probing its CLI and reports 156 noncompliant modules
against old headings/names; that failed historical audit is recorded explicitly
and is not called a passing documentation gate. Docstring fidelity and applicable
Ruff checks pass. Full source/artifact qualification remains separate under #334.
