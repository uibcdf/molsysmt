---
summary: Migrate legacy MolSysMT trees into the full Ruff gate.
issue: uibcdf/molsysmt#212
status: resolved
opened: 2026-09-12
closed: 2026-09-22
verification: measured
area: [ci]
guard: devtools/tests/test_ruff_clean.py
normative:
blocked_by: []
supersedes: []
---

# Migrate legacy MolSysMT trees into the Ruff gate

**Reported:** 2026-09-12, during the MolSysSuite policy rollout.
**Status:** Resolved; the full repository-wide Ruff gate is active.

## What

The temporary Ruff path exclusions for maintained MolSysMT code, tests and
documentation have been removed. Before migration, the shared baseline checked
only maintenance tooling and the MolSysViewer add-on, while the legacy core
had a narrower `F821,F822,F823,B006,B023` gate.

## How

Each owned directory was migrated separately. Ruff's suggested changes were
reviewed for semantic effects, followed by relevant scientific tests. The
critical core gate was retired once the shared baseline covered the full core.

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

This proposal covers Ruff migration. Incidental defects found during cleanup
received focused tests. No temporary Python path exclusion remains.

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

## Seventh migrated slice: PDBFixer, NGLView, and H5MSM forms

On 2026-09-22, `pdbfixer_PDBFixer`, `nglview_NGLWidget`, and `file_h5msm`
were migrated. Ruff reported 1,341 findings across these adapters, mostly
import ordering. The established package initializer order and wildcard
exports were retained with bounded, line-local exceptions. A duplicated
getter import in the H5MSM amino-acid converter was reduced to one copy.

The relevant functional suites passed before and after editing, including
the full `tests/form/file_h5msm` suite. All three packages retain their
public export names, origin modules, and conversion maps. Their Ruff lint
and format checks pass; the explicit CI gate and file-selection guard now
include them. An AST comparison across 69 changed form Python files found
no non-import differences. The local `181l.h5msm` modification remains
untouched and outside the migration commits. The full-core count is now
4,388 findings.

## Eighth migrated slice: 52 smaller form adapters

The remaining forms were grouped by their actual Ruff findings. Fifty-two
adapters had only `I001`, `E402`, `F401`, and `F403` findings, totaling 1,976
findings. A ten-adapter pilot first verified the treatment of metadata-first
initializers and late imports. The other 42 then used the same reviewed
pattern. Standard-library `types` imports could move above `form` metadata;
imports used after wrapper definitions kept line-local `E402` exceptions.

Comparing package exports exposed several unsafe automatic `F401` removals.
Some single-import files intentionally re-exported `attributes`, `add`, or
other adapter functions. Nine wrappers assembled callable bodies with `exec`
and passed converters through `locals()`, which Ruff cannot see as usage.
Those imports were restored explicitly, with local explanations where needed.
Historical package-level names re-exported through wildcard imports were
also preserved. All 52 adapters retain their original public names, origin
modules, conversion maps, and conversion-option maps.

The 52 adapters now pass Ruff lint and format checks. An AST comparison over
813 changed Python files found no non-import executable changes. The test
directories available for 30 of these adapters passed (with existing skips).
The explicit CI checks and file-selection test now read one manifest,
`devtools/ruff_migrated_paths.txt`, covering 70 migrated paths including
earlier slices. The full-core count is 2,412 findings.

## Ninth migrated slice: the complete form tree

On 2026-09-22, the remaining 21 adapter directories and the form package
modules were migrated. `ruff check --no-cache molsysmt/form` now passes, and
`ruff format --check molsysmt/form` reports all 1,690 Python files formatted.
The CI manifest now names the complete `molsysmt/form` subtree instead of
individual adapters; its file-selection test verifies recursive coverage.
The remaining full-core count is 1,361 findings, all outside `form`.

The cleanup exposed three existing defects: the OpenMM PDBFile to MDTraj
trajectory converter did not construct a valid trajectory from selected
coordinates; the three-letter amino-acid string copy adapter recursed into
itself; and the ViewerJSON export list named an absent `get` object. Focused
tests cover these corrections. Adapter exports and conversion maps were
compared with the pre-edit snapshot, with the absent ViewerJSON name as the
intentional exception. The available adapter test suites passed except for
four H5MSM tests that read the locally modified `181l.h5msm` fixture. The
expected getter shapes were separately verified against the committed fixture
extracted to a temporary file. The working fixture was not changed or staged.
The form-adapter, dependency, and developer-guide validators passed.

## Tenth migrated slice: private infrastructure

The complete `molsysmt/_private` tree now passes Ruff lint and format checks:
452 Python files are formatted. Most of the 531 initial findings were import
ordering and unused imports in argument digesters. Ruff's proposed removals
were reviewed before application; the digesters' 387 targeted tests passed.
The conversion-shortcut package now imports its five functions explicitly and
retains its historical `arg_digest` name. The SMonitor package imports all
exception and warning classes explicitly, preserving direct access to names
beyond its narrower `__all__`. A duplicate catalog key was removed; its first
value had always been overwritten by the second. The wider private test suite
passes when SMonitor tests are excluded, and the dependency validator passes.

The full private suite still has 15 failures in SMonitor warning reconstruction:
round-tripping a rendered warning repeats its hint. These are not introduced
by this slice: the warning classes' AST is unchanged from `HEAD`, the emitter
changes only import order and formatting, and removing the earlier duplicate
catalog entry leaves the effective value unchanged. The warning behavior needs
its own repair before the full test gate can be claimed to pass. The full-core
Ruff count is now 830 findings, all outside `form` and `_private`.

## Eleventh migrated slice: basic operations and small scientific modules

The `basic`, `hbonds`, `molecular_dynamics`, `molecular_mechanics`, `physchem`,
and `topology` trees now pass Ruff lint and format checks, covering 99 Python
files. The 77 one-line conditionals in `basic/info.py` were expanded without
changing their conditions or assignments. The `basic` selector retains a local
variable used by its string expression evaluator; a line-level Ruff exception
documents that dynamic use. The Taichi availability check in `get_sasa` still
performs the import, now without binding an unused local name. Unused local
assignments and duplicate imports were removed after reviewing Ruff's diffs.

The `hbonds` and `molecular_mechanics` suites pass, and both molecular-dynamics
public run functions import successfully. The available `basic`, `topology`,
and `physchem` suites have failures in tests built from the locally modified
`181l.h5msm` fixture. A direct check using the committed fixture extracted to
`/tmp` confirmed 1,441 atoms, `contains(molsys) is True`, and boolean-mask
selection `[1, 3]`; the local fixture remains untouched. Those suites cannot
be treated as fully passing on this checkout. The full-core Ruff count is 576.

## Twelfth migrated slice: complete core package

The remaining `element`, `structure`, `build`, `third_party`, `native`, `data`,
`pbc`, `supported`, `configure`, and root modules now pass the full Ruff lint
and format baseline. `ruff check --no-cache molsysmt` passes, and
`ruff format --check molsysmt` reports 2,566 formatted files. The package is
no longer excluded from default Ruff discovery. The CI workflow checks lint
and format on every selected Python file, and its local selection test checks
all tracked Python source in the core. The earlier migrated-path manifest and
narrow critical-rule check are no longer needed.

Ruff's proposed removals were reviewed for imports that are public exports,
lazy imports, or variables referenced by dynamically evaluated selection
strings. The latter retain narrowly scoped `F841` exceptions. Focused tests
for corrected `Simulation.set_parameters` and unsupported-choice error paths
pass. The complete `native` and `pbc` suites pass; the suites for `build`,
`element`, `structure`, and `third_party` still have failures that read the
locally modified `181l.h5msm` fixture. The dependency and form-adapter
validators pass. Outside the core, an explicit Ruff scan found 1,219 lint
findings and 577 unformatted files in the currently excluded trees, mostly in
`tests`. The repository-wide gate remains an active task under this issue.

## Thirteenth migrated slice: repository-wide Python gate

The remaining Python files in `tests`, `devtools/tests`, `docs`, `benchmarks`,
and the archived Rust pilot scripts were migrated. Ruff's import and unused
name suggestions were reviewed before applying them. The tests keep local
names resolved by selection strings, and optional-dependency probes retain
their import behavior. Two distinct tests that had the same Python name now
both collect; two pairs of identical duplicated H5MSM tests were reduced to
one copy per module. The hydrophobicity smoke test now verifies every computed
definition, and the neighbor-list test checks the distance unit it previously
retrieved without asserting. Delayed imports required by path setup and
optional-dependency skips carry line-level `E402` exceptions.

The old `.gitignore` pattern `lib/` also hid 18 tracked `tests/lib` Python
files from default Ruff discovery. An explicit exception now exposes that
directory. The Ruff selection test compares default discovery against all
tracked `.py` and `.pyi` files in the repository, so this coverage gap fails
the gate if it recurs. No Python tree remains in Ruff's temporary exclusion
list. `ruff check --no-cache .` passes, and `ruff format --check .` reports
3,361 formatted files. The GitHub workflow runs both commands whenever any
Python file or Ruff configuration changes.

Targeted functional tests passed across `tests/lib`, `tests/element`, PBC,
hydrophobicity, neighbors, OpenMM pinning, structure-index boundaries,
form adapters, and `devtools/tests`. Full `tests/` collection passed. The
restored `181l.h5msm` fixture passed the demo-asset validator, allowing
scientific suites that read it to be exercised again. The fixture's earlier
zero-atom overwrite is tracked separately under issue #216.

## Resolution

The temporary Python directory exclusions are gone. The repository default
`ruff check --no-cache .` passes with Ruff 0.16.5, and
`ruff format --check .` reports 3,361 formatted files. The
[Ruff CI run](https://github.com/uibcdf/molsysmt/actions/runs/35788061365)
passed on the published migration commit. The per-file `F401` allowance for
package initializers remains part of the shared baseline; no Python directory
is outside the gate.

The guard is `devtools/tests/test_ruff_clean.py`. Its first test compares Ruff's
default file selection against every tracked `.py` and `.pyi` file; its second
test runs lint and format on that selection. This guards against a clean result
caused by excluding the files that need checking. It also catches the former
`tests/lib` blind spot caused by `.gitignore`.

With Pytest Receptor's `llm` profile and 12 workers, a broad run covering
2,265 tests in `basic`, `build`, `structure`, `physchem`, `topology`,
`third_party`, `lib`, `element`, `native`, `pbc`, `supported`, development
tooling, and targeted form adapters finished with 2,262 passes and three
skips. The full `tests/` collection also passed. This does not claim that
every test in the repository was executed. The previously modified 181L
fixture was restored and passed the demo-asset validator under separate issue
`uibcdf/molsysmt#216`; the unsafe H5MSM extraction path remains tracked under
`uibcdf/molsysmt#235`.
