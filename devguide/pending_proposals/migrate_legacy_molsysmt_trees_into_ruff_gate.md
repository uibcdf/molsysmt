---
summary: Migrate legacy MolSysMT trees into the full Ruff gate.
issue: uibcdf/molsysmt#212
status: active
opened: 2026-09-12
closed:
verification: measured
area: [ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Migrate legacy MolSysMT trees into the Ruff gate

**Reported:** 2026-09-12, during the MolSysSuite policy rollout.
**Status:** Active; the critical-rule gate remains active during migration.

## What

Remove the temporary Ruff path exclusions for maintained MolSysMT code, tests and
documentation. The shared baseline currently checks maintenance tooling and the
MolSysViewer add-on, while the legacy core remains protected by the narrower
`F821,F822,F823,B006,B023` gate.

## How

Migrate one owned directory at a time. For each slice, run `ruff check --fix` and
`ruff format`, review all changes for semantic effects, run its scientific tests,
and remove its path exclusion only when lint and format checks pass. Keep the
critical core gate until the shared baseline covers the entire core.

## Why

An immediate full-tree migration is too large to review safely within the policy
rollout. On 2026-09-12, `ruff check molsysmt` found 13,500 violations with the
shared baseline. The legacy source and generated/form-adapter material need
separate, bounded review.

## What is measured and what is assumed

Measured: `ruff check --no-cache molsysmt` reports 13,500 violations under Ruff
0.16.5. `ruff check --no-cache --select F821,F822,F823,B006,B023 molsysmt`
passes. No claim is made that every violation needs a manual edit.

## What was refuted

An immediate all-tree formatter pass was rejected because it would mix extensive
style churn with the policy integration and weaken review of scientific behavior.
Simply excluding the core without a separate critical-rule gate was rejected
because that would remove an existing protection.

## Scope and exclusions

This proposal covers only the remaining Ruff migration. It does not change
scientific APIs or decide whether historical/generated files should ever be
formatted. Any permanent exclusion requires a separate justification.

## Acceptance criteria

- Every maintained Python tree passes the shared `E4,E7,E9,F,I` baseline and
  `ruff format --check` with no temporary path exclusion.
- Repository-specific Bugbear checks remain active where intended.
- Relevant scientific tests pass after each migrated slice.
- The central exception linked to this issue is removed.

## Dependencies and risks

The migration follows `uibcdf/molsysmt#211`. Import sorting or unused-import
fixes can affect registration side effects, so each slice needs behavioral review.

## Provenance

Local checkout, Python 3.13, Ruff 0.16.5, 2026-09-12 to 2026-09-14.

## Audit update: 2026-09-22

With Ruff 0.16.5, `ruff check --no-cache --output-format json molsysmt`
reported 13,487 findings in 2,095 files. Of these, 12,091 findings in 1,421 files
are under `molsysmt/form`. The largest rule counts are `I001` (8,050), `F841`
(2,929), `E402` (1,115), and `F401` (910). `ruff format --check molsysmt`
reported 2,377 files needing formatting and 189 already formatted. The narrow
critical-rule check still passed.

The root `extend-exclude = ["molsysmt", ...]` is one exclusion for the whole
package, not one entry per child directory. Therefore, cleaning one directory and
removing its individual exclusion is not currently possible. A staged rollout can
first add explicit Ruff lint and format gates for each cleaned directory while
the root exclusion remains; the broad exclusion can be removed after coverage is
complete, or replaced with a reviewed set of narrower temporary exclusions.
Each gate must prove that Ruff selected the intended files, following the
zero-file test failure resolved in `uibcdf/molsysmt#232`.

The first bounded candidate is `molsysmt/attribute`: explicit lint reports six
`I001` findings across six files, and format check reports eight of nine Python
files needing formatting. Its 11 existing `tests/attribute` tests pass on this
checkout. This is a candidate, not a claim that import reordering is semantically
safe; review `__init__.py` exports and alias behavior after the change, and run
the dependency validator. Then add explicit CI checks for this path so that its
clean state cannot regress while the root exclusion remains.

The large `form` group needs smaller adapter-level batches, especially the getter
modules where hundreds of repeated `I001` and `F841` findings occur in a single
file. Import-order changes, wildcard exports, and apparently unused assignments
need behavioral review rather than a package-wide automatic fix.

The historical broad tooling request `uibcdf/molsysmt#113` says post-1.0, while
the current `devguide/release_gate.md` says `ruff check molsysmt` must pass and the
manual full-CI workflow runs that command. The release scheduling of this full
migration should be reconciled explicitly; it does not prevent a small, reviewed
slice from starting.

## First migrated slice: attribute

On 2026-09-22, the `molsysmt/attribute` package was linted and formatted. An
unreviewed import sort first moved the `bonds_are_required_to_get_attribute`
import before `get_argument_aliases` in `attribute/__init__.py`. Importing MolSysMT
then failed because the decorator on the former loaded argument normalization
while `get_argument_aliases` still resolved to its module rather than the exported
function. The original dependency order was restored with a documented local
`isort: skip` on that import. This is a measured example of why import sorting
needs behavioral review in this repository.

An explicit CI step now runs both `ruff check molsysmt/attribute` and
`ruff format --check molsysmt/attribute`. The parametrized test
`devtools/tests/test_ruff_clean.py::test_migrated_package_ruff_gate` compares
Ruff's selected files with every Python file under each migrated package and runs
both checks, so a zero-file or partial selection cannot pass unnoticed. The 11
`tests/attribute` cases, the three Ruff gate tests, and dependency validation
passed after the import-order correction. The general `molsysmt` exclusion remains
until more of the legacy package is migrated.

## Second migrated slice: lib

The baseline `tests/lib` suite passed all 45 cases before editing on 2026-09-22.
The `molsysmt/lib` tree had 29 `I001` findings across 29 files, with only five
files requiring formatting. After import sorting and formatting, full lint and
format checks pass for the tree, and the same 45 tests still pass. The CI step
and the parametrized file-selection test now cover `molsysmt/lib` alongside
`molsysmt/attribute`. No core scientific behavior was intentionally changed.

## Third migrated slice: string PDB text

On 2026-09-22, the `molsysmt/form/string_pdb_text` adapter was migrated after its
366 functional cases passed on the unedited baseline. Its 408 initial findings
comprised 387 `I001`, 12 `E402`, six `F401`, and three `F403`. Reviewing Ruff's
proposed diffs showed that `I001` sorts imports *inside* getters without hoisting
them to module scope. The 386 getter and ordinary-module import-order findings
and six unused imports were fixed. All lazy imports remain inside their getters.

The adapter's `__init__.py` retains its metadata-first initialization and
wildcard getter/setter exports. Its established import block has a bounded
`isort: off` marker, with line-local exceptions for 12 `E402` and three `F403`
findings. Changing this order or expanding the generated exports would be a
separate behavioral change, not a mechanical
lint fix. Before and after the migration, the package exposed the same 369
public names and 15 conversion routes. An AST comparison that ignored only
import statements found no other executable-statement differences across its
Python files.

The same 366 functional cases passed after the change. Full Ruff lint and format
checks, the migrated-file selection test, dependency validation, and the form
adapter structural audit also passed. The CI Ruff workflow now checks this adapter
explicitly. The full-core Ruff count fell from 13,452 to 13,044 findings; the
adapter contributes zero unsuppressed findings to that count.

## Fourth migrated slice: native MolSys form

On 2026-09-22, the `molsysmt/form/molsysmt_MolSys` adapter was migrated after
all 384 of its functional cases passed on the unedited baseline. Its 210 Ruff
findings included import ordering, unused imports, late imports in the form
initializer, intentional wildcard getter/setter exports, two duplicate imports,
and two wildcard imports of MolSysMT's private ArgDigest wrapper.

Ruff's proposed changes were reviewed by category before editing. Lazy imports
inside functions remain inside those functions. The two private-wrapper wildcard
imports were replaced with explicit `arg_digest` imports. The initializer kept
its metadata-first and export order, with a bounded `isort: off` block and
line-local `E402` and `F403` exceptions. Its duplicate `add_bonds` and
`remove_bonds` imports were reduced to one copy each.

A before/after export comparison caught a real compatibility effect that the
functional suite alone did not: removing unused imports from `set.py` dropped
the historical package-level `ArgumentError` and `np` names because the package
uses `from .set import *`. The initializer now preserves both names explicitly.
It exposes the same 525 public names, 34 conversion routes, and conversion-option
map as before. An AST comparison that ignored only imports found no other
executable-statement differences.

The same 384 functional cases passed after editing. Ruff lint and format checks
are clean for the adapter; the CI workflow and the migrated-file selection test
now include it. The full-core count fell from 13,044 to 12,834 findings, with
zero unsuppressed findings in this adapter.

## Fifth migrated slice: repeated getter assignments and seven adapters

On 2026-09-22, Ruff identified 2,878 `F841` findings in the generated
topological getters of `file_smi`, `openff_Molecule`, `openff_Topology`,
`string_smiles`, `file_bcif`, `file_bcif_gz`, and `string_pdb_id`. Every finding
was the same unused assignment of the result of
`bonds_are_required_to_get_attribute`. Ruff's unsafe fix was reviewed before
application: it retains the function call and removes only the assignment to
`bonds_required`. The combined baseline functional suites for all seven
adapters passed after this change. The full-core count fell to 9,956.

The seven adapters were then linted and formatted individually. Their lazy
imports remain inside the getters. The metadata-first package initialization
and wildcard getter/setter exports were retained with bounded `isort: off`
blocks and line-local `E402`/`F403` exceptions. Two duplicate `download`
imports in the BCIF package initializers were reduced to one each. The
original and migrated package export names, origin modules, and conversion
maps match for all seven adapters. Their functional suites, Ruff lint and
format checks, the form-adapter audit, and the dependency validator passed.
An AST comparison across the 141 changed form Python files found no
non-import differences after normalizing the reviewed `bonds_required`
assignments. The explicit CI checks and file-selection guard now cover all
seven adapters. The remaining full-core count is 7,567 findings; this is
progress on issue #212, not completion of the repository-wide gate.

## Sixth migrated slice: OpenMM, AlphaFold ID, and mmCIF containers

On 2026-09-22, `openmm_Modeller`, `openmm_Simulation`,
`string_alphafold_id`, and `mmcif_PdbxContainers_DataContainer` were
migrated. Their 1,838 initial findings were concentrated in import ordering,
unused imports, and metadata-first package initializers. Ruff's specific
findings were reviewed for each adapter. The one private ArgDigest wildcard
import in the Modeller converter and two getter wildcard imports in the mmCIF
converter were replaced with the exact names used. AlphaFold's two unused
local assignments were removed after inspecting Ruff's proposed diff; the
response read and decode call remains.

All four adapters pass their relevant functional suites before and after
editing. Their package export names, origin modules, conversion maps, and
Modeller's conversion-option map match the originals. The form-adapter audit,
explicit Ruff lint and format checks, and migrated-file selection test pass.
An AST comparison across the 101 changed form Python files found no other
non-import differences after normalizing the two reviewed AlphaFold
assignments. The full-core count fell from 7,567 to 5,729 findings.
