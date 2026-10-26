---
summary: Execute every declared conversion edge in the test suite, not only audit it statically.
issue: uibcdf/molsysmt#181
status: partial
opened: 2026-08-19
closed:
verification: measured
area: [form, convert, tests]
guard:
normative:
blocked_by: []
supersedes: []
---

# Run the conversion graph, do not only describe it

**Reported:** 2026-08-19, from the post-mortem of
[`uibcdf/molsysmt#180`](https://github.com/uibcdf/molsysmt/issues/180): seven public
conversion routes were broken for eleven days with every audit green.
**Status:** partial. Resident-native, MDTraj/OpenMM, MDAnalysis Universe/AtomGroup/
Topology and bounded H5MSM/PDB/SDF/PDBQT execution profiles are implemented;
remaining external/file/network routes remain debt.

## What

Generate one smoke case per declared conversion edge, over a small shipped system,
asserting only that the conversion completes and returns an object of the declared form.

Not fidelity. Not shapes, units, indexing or `None` semantics — those are the subject of
[Conversion Fidelity and MolSysDict v1](conversion_fidelity_and_molsysdict_v1.md) and are
a much larger claim. This proposal asserts the weakest useful property: **the route
runs**.

## How

The graph is already discoverable. `audit_conversion_fidelity.py` builds it from each
adapter's `_convert_to` map, and the same traversal can emit parametrised cases instead
of a coverage report.

The hard parts are not the traversal:

- **Which system to use per source form.** A `file:prmtop` case needs a prmtop; an
  `openmm.Topology` case needs coordinates supplied, as
  [`uibcdf/molsysmt#180`](https://github.com/uibcdf/molsysmt/issues/180) showed. Some
  forms have no small shipped instance.
- **Soft dependencies.** Edges into `pdbfixer`, `parmed`, `MDAnalysis` and the rest must
  skip cleanly, not fail, when the dependency is absent.
- **Runtime.** `tests/form` already runs 6 772 tests in roughly 270 s on 14 workers.
  Adding up to 561 cases is not free, and some edges download or write files.

## Why

Measured on 2026-08-19:

| | |
|---|---|
| declared conversion edges | **561** |
| adapters declaring them | 92 |
| median edges per adapter | 5 |
| largest | `molsysmt_MolSys` 34, `file_pdb` 23, `string_pdb_id` 20 |
| `convert(` calls in `tests/` | 956 |
| distinct target forms named in `tests/` | 55 |

Coverage exists and is substantial. What does not exist is any statement about *which*
of the 561 edges it touches, so the answer to "is this route exercised?" is unknown
rather than yes or no.

**Both audits over this graph are static, and both say so.**
`audit_conversion_fidelity.py`: *"The compact baseline records accepted non-exhaustive
coverage debt; it is not a claim that those routes are fully verified."*
`validate_form_adapters.py`: *"This static reachability check does not prove correct
values, shapes, units, indexing, `None` semantics, conversion fidelity, decorator
correctness, or iterator output behavior."*

Neither is wrong. The gap is not a defect in either tool; it is that nothing closes it.

**What that cost.** In `e6b20c77c` (2026-08-08, 214 files, *"make a plugin's converters
lazy, and unambiguous to import"*), seven adapters acquired an import of the target
form's identity converter instead of their own. Seven public routes — `nglview.NGLWidget
-> openmm.Topology`, four out of `openmm.Topology`, two out of `string:alphafold_id` —
raised on every call. Both audits stayed green for eleven days.

A smoke case per edge would have failed on the introducing commit. It would also have
caught the two further defects found while fixing #180, neither of which needs fidelity
to detect: a `StringIO().read(text)` misuse raising `TypeError`, and an unguarded
`coordinates.shape[0]`.

## What is measured and what is assumed

Measured: every figure in the table above, by parsing the `_convert_to` dictionaries and
grepping `tests/`.

Assumed, explicitly: that most edges can be exercised from a shipped system. Not
checked — some forms may have no small instance, and that is precisely what a first
measurement pass should establish before any estimate is offered.

Not estimated: the effort. The 2026-08-19 conversation put a figure on a related idea
without measuring it and had to withdraw it; no figure is offered here.

## What was refuted

**A static check in `validate_form_adapters.py`, proposed as the guard for #180 and
withdrawn.** Two rules were tried. Flagging any absolute import of a converter that
shadows a local module produced 52 hits, most legitimate — `MDAnalysis_AtomGroup`
delegating to `MDAnalysis_Universe` is by design. Narrowing to *identity* converters
looked sharper and still flagged `file_h5msm` and `file_pdb`, whose target converters
deliberately accept a path; those routes were run and all succeed.

What separates the defect from the legitimate cases is whether the imported converter
tolerates a foreign item, which is behavioural and invisible to a static rule. That
failure is the argument for this proposal: the property in question only exists at run
time, so the check has to run.

## Scope and exclusions

In scope: one executable case per declared edge, asserting completion and returned form.

Out of scope:

- Fidelity of the converted content — [Conversion Fidelity and MolSysDict
  v1](conversion_fidelity_and_molsysdict_v1.md).
- Replacing either static audit. They answer a different question, cheaply, and should
  stay.
- Transitive routes. Only edges declared in a `_convert_to` map.

## Acceptance criteria

- Every declared edge is either exercised or explicitly listed as not exercisable, with
  the reason.
- The list may only shrink, in the idiom already used by
  `form_attribute_delivery_baseline.json` and `tier1_conversion_fidelity_baseline.json`.
- Missing soft dependencies skip; they do not fail.
- Introducing #180's defect again fails the suite.

## Provenance

MolSysMT at `bc42b2eaa`, 2026-08-19. Edge counts from the `_convert_to` dictionaries in
`molsysmt/form/*/__init__.py`; test counts from `tests/`; timing from
`pytest tests/form -n 14 --dist loadfile`.


## First executable profile — 2026-10-22

At baseline cdf7808e1, discovery reports 96 forms and 596 declared direct edges.
The new resident-native-v1 profile selects 41 edges among thirteen native and
dictionary forms. Each case executes the declared adapter with digestion enabled
and its public conversion route on fresh inputs. The two harness controls
reject callable exceptions and wrong output forms. The inventory audit is
explicitly non-executing and independent of capability visibility settings.

The other 555 edges are individually listed as accepted unexecuted debt for
this profile, with fixture/profile reasons. This is not a claim that no existing
adapter test exercises them, nor that they are impossible to execute. New routes
must be covered or explicitly accounted for; retired/newly covered debt fails
the audit until removed. The inventory has no automatic baseline rewrite route.

The first run found two genuine digest metadata defects, tracked and repaired
under uibcdf/molsysmt#418. Neither failing edge was skipped or removed from the
profile. Mirrored adapter regressions fail before the repair (four failed, two
passed) and preserve copy policy and foreign-form rejection after it.

```bash
python -m pytest tests/conversion_truth tests/form/molsysmt_MolecularMechanics tests/form/molsysmt_MolecularMechanicsDict devtools/tests/test_audit_conversion_execution.py --receptor=llm -n 12
```

Result: 194 passed, no skips, 17.77 seconds; four expected legacy H5MSM warnings.
Linux x86_64, Python 3.14.7, NumPy 2.4.6, pytest 9.1.1. Source development evidence,
not installed release qualification. The [operational guide](../conversion_execution.md)
records current commands, scope and expansion obligations. No fidelity or
scientific-accuracy guarantee follows from output-form smoke coverage.

Remaining work: source fixtures and executable profiles for external objects,
file/string formats and separately marked network identifiers, with honest
optional-dependency handling. #181 stays partial; #334 release coordination is
unchanged. The bounded block does not satisfy whole-graph execution acceptance.

Final combined regression on 2026-10-22 executes the scientific suite and registry
controls, conversion truth, mechanics adapters, inventory audit and real-takeaway
rendering controls: **587 passed**, zero skips/failures, 54.75 seconds, with twelve
workers and Pytest Receptor. Seven expected legacy H5MSM warnings remain. Command:

```bash
python -m pytest devtools/tests/test_validate_scientific_evidence.py devtools/tests/test_execute_scientific_evidence.py devtools/tests/test_audit_conversion_execution.py devtools/tests/test_course_takeaway_rendering.py tests/scientific_truth tests/conversion_truth tests/form/molsysmt_MolecularMechanics tests/form/molsysmt_MolecularMechanicsDict --receptor=llm -n 12
```

All fourteen fast release gates, full-package Ruff check and format verification
also pass. No new release matrix, artifact production or publication is implied.


## Resident MDTraj/OpenMM expansion — 2026-10-22

The next bounded profile extends both graph axes with `mdtraj.Topology`,
`mdtraj.Trajectory`, `openmm.Topology` and `openmm.Modeller`. The profile is now
`resident-native-engines-v2`: 70 declared edges (29 additional) and 526 explicitly
unexecuted edges, still within the 596-edge graph. Only newly covered edges were
removed from the debt inventory; no new exception or accepted failure was added.

External water inputs use each provider's own topology API and literal
three-atom coordinate arrays. Native inputs remain fresh four-atom systems.
Topology-only sources receive explicit unit-bearing coordinates for targets
that require geometry. Setup skips a provider-specific case only if the needed
optional package is genuinely unavailable; conversion exceptions propagate.
The direct/public reachability assertion is unchanged and does not certify
fidelity. The original thirteen-form native subset remains covered.

Execution found two broken cross-engine container routes and a nested topology
selection route, recorded under uibcdf/molsysmt#419. Investigating the otherwise
passing topology-to-trajectory route's unit-stripping warnings exposed silent
tenfold coordinate scaling for angstrom input, ignored atom selection and a
lost explicit cell, recorded under uibcdf/molsysmt#420. Neither defect was hidden
by excluding its edge. Mirrored conversion guards add physical values, selected
coordinates, source-order duplicate selection and box checks beyond the smoke
profile's weaker output-form promise.

The focused updated selection passes 100 cases without warnings. The independent
original #420 guards first produce six failures and two passing nanometer
controls; the original cross-engine guards produce eight failures. Nested subset
controls additionally reproduce two failures before correcting the source-form
import. These negative runs distinguish repaired runtime defects from broader
scientific or format-fidelity claims.

The conversion tutorial and Native Forms course module now explain full-source
coordinate axes, explicit units and the single-structure Modeller boundary.
Only Markdown source text changes: executable cells, saved outputs, execution
counts, notebook/cell metadata and cell IDs are identical to the baseline.
No full notebook re-execution is claimed for prose changes. The operational guide
is updated; #181 remains partial pending external/file/string/network profiles.

### Expanded qualification

The full relevant regression command and environment are retained in the
[receipt](../../devtools/data/conversion_execution_engines_20261022.json):
2,178 passed, zero skips/failures, 123.67 seconds. Ten existing dummy-PDB-cell
warnings and five legacy H5MSM notices remain. A separate final doctest passes.
The full documentation build exits 0 with 711 warnings and no errors, without
new warning families or a whole-site cleanup claim. All fourteen fast gates
and applicable Ruff check/format controls pass. MDTraj 1.11.1 and OpenMM 8.6.1
were already installed; no dependency version or installed environment changes.

The repaired defects are archived under their own issue identities. This
profile is a more useful execution baseline, not whole-graph completion:
526 edges still require profiles and fixtures, so #181 remains partial.


## H5MSM schema-aware expansion — 2026-10-22

The `resident-h5msm-v3` profile adds `file:h5msm` and
`molsysmt.H5MSMFileHandler` to the declared graph rectangle: 82 selected edges,
including 12 additional disk/handler edges, and 514 explicitly unexecuted edges
out of the unchanged 596-edge graph. Only these newly exercised edges are removed
from debt. The native/engine and disk modules partition the selected routes by
source/target form, using one inventory. Debt reasons now use profile-independent
wording to avoid rewriting them for each legitimate expansion.

Inspection confirms the intended version boundary: low-level registered adapters
use the legacy 0.4 schema, while public `convert` writes 0.5 and reads modular data
before resident dispatch. The handler deliberately supports only 0.3/0.4. The
profile tests those supported paths without claiming raw-adapter 0.5 parity or
changing the handler. Fresh rich native fixtures supply complete hierarchy,
coordinates, cells and time; temporary handler sources/results are closed under
explicit ownership and their HDF5 identifiers are checked.

Nineteen disk/schema cases pass: twelve direct/public edge witnesses, five public
modular-domain combinations, a joint geometry/analysis remap, and a negative
handler-target control. Modular cases retain domain absence, named parallel
observations, occurrence indices, source maps and evaluated-empty/unevaluated
coverage. The remap selects atom indices [2, 0] in source order and structure
indices [2, 0, 2], checking both quantities and result axes. No scientific-method
or exhaustive H5MSM-field fidelity claim follows.

Initial new-test failures were harness mistakes: source maps are object metadata,
whereas occurrence indices are exposed by the public query dictionary. The guards
were corrected to the actual public interfaces; no production behavior or expected
numeric values were changed. The final focused disk module passes 19 cases with
17 expected legacy-read warnings. No new runtime defect has been established in
this block. Existing H5MSM and interaction workflow regressions are run separately.

### H5MSM regression qualification

```bash
python -m pytest tests/conversion_truth tests/form/file_h5msm tests/form/molsysmt_H5MSMFileHandler tests/native/test_h5msm_file_handler.py tests/interactions/test_h5msm05.py tests/interactions/test_public_molsys_h5msm_workflow.py tests/interactions/test_software_provenance.py devtools/tests/test_audit_conversion_execution.py --receptor=llm -n 12
```

Result: **1,488 passed**, zero skips/failures, 31.57 seconds. The 654 warnings
are all expected legacy reads: 649 for 0.4 and five for 0.3, retaining the
migration guidance. Additional software-provenance controls verify the original
producer survives a different writer/reader; the new synthetic analysis also
retains an explicitly supplied producer marker, method, parameters, measurements
and units rather than inheriting the current installed version at read time.

The [receipt](../../devtools/data/conversion_execution_h5msm_20261022.json)
records scope, commands, versions and outcomes. The updated developer testing
page renders in a focused MyST/Sphinx project with zero diagnostics. No full-site
warning inventory, notebook execution, dependency changes or installed-pair
qualification is claimed. H5MSMFileHandler capability and all production code
remain unchanged. #181 remains partial; remaining routes include other external,
file/string and network profiles. Completing them all is not a newly imposed
pre-1.0 release requirement.

The final profile-only command (both execution modules and inventory controls)
passes 98 cases in 16.69 seconds, with no skips/failures and 17 expected 0.4
warnings. All fourteen fast gates pass. Whole-repository Ruff check and format
checks pass; the final whitespace-only formatting correction preserves the test
module AST exactly and does not change the retained outcomes.

## PDB file/text/handler expansion — 2026-10-22

The `resident-h5msm-pdb-v4` profile adds three PDB forms and 32 declared edges:
114 selected edges out of 596, leaving 482 individually listed unexecuted edges.
The literal local water input has two distinguishable structures and CONECT
records. Native and engine sources have explicit coordinates; topology-only
sources receive matching full-source quantities. Each edge executes directly
and through public `convert` with a fresh source/output, normal digestion and
explicit handler ownership. A separate guard checks the three executor modules
partition the selected graph exactly once.

After correcting two harness mistakes (the handler is exported by `native`,
and HETATM is a valid coordinate record), the initial profile reproduces four
runtime failures. They became uibcdf/molsysmt#422 (file destination argument),
uibcdf/molsysmt#423 (two wrong PDB export delegations), and uibcdf/molsysmt#424
(unsupported closed buffer passed to MDTraj). A subsequent resource probe
reproduces a separate successful-conversion scratch leak, uibcdf/molsysmt#425.
All are repaired with source adapters and existing native/PDB/MDTraj tools;
no new scientific method or chemical inference rule is introduced.

Mirrored regression tests compare destination bytes, atom names and positions
for nonconsecutive selections, native source ownership, equivalent nm/angstrom
inputs, retained multiple structures and explicit periodic cells. Scratch tests
check actual file and parent-directory retirement on return, reader exceptions
and KeyboardInterrupt, directly and publicly. Duplicate atom indices in native
chemistry are not newly supported; the tests use the existing unique subset
contract. Requested structure order and repetition are exercised in MDTraj.

The expanded regression passes **2,284 tests**, no skips/failures, 98.67 seconds
using 12 workers and Pytest Receptor (23 legacy H5MSM notices and one existing
cross-chain warning). The final focused profile/repair selection passes 175
cases in 18.15 seconds plus the separately run partition guard; six adapter
doctests also pass. The User Guide conversion/Cookbook pages and Common Core
Module 1 are re-executed successfully; the developer testing page renders with
zero diagnostics in a focused MyST/Sphinx project. The initial notebook attempt
was blocked at local socket creation by the sandbox; the authorized rerun passed.

The [receipt](../../devtools/data/conversion_execution_pdb_20261022.json) records
the commands, versions and bounds. #181 remains partial. No installed-pair,
whole-graph, full PDB-field or new scientific accuracy certification follows;
release selection/publication remain governed by #334.

### PDB CI signature follow-up

Ordinary CI run 39879357399 rejects the first PDB commit at its parent-signature
comparison: the destination alias had moved out of its original positional slot.
The follow-up restores the six original positional parameters and adds only
keyword-only `output_filename`. A function-specific intentional-addition waiver
names #422 and the executable contract guards; the validator is unchanged.
The destination regression/doctest selection passes eight cases, and comparisons
against both the rejected commit and the original pre-change API pass. This
corrects the initial CI failure without treating local fast gates as CI success.

## SDF/PDBQT execution expansion — 2026-10-22

The `resident-files-v5` profile adds `file:sdf`, `file:pdbqt` and
`string:pdbqt_text`: **133 selected edges out of 596**, leaving 463 individually
listed unexecuted edges. Nineteen additional edges have two witnesses each:
V2000/V3000 SDF or rigid/ligand PDBQT. All 38 cases execute their direct and
public routes with fresh local inputs and named destinations. The executor
partition guard includes the fourth module and checks no selected edge is lost
or counted twice.

Literal witnesses are reused from the existing independent format-contract
suites. Native writer sources are prepared through the current reader and are
explicitly not independent writer oracles. They provide complete SDF chemistry,
or declared AutoDock4 labels/charges and a separately retrieved ligand tree.
No preparation, typing, graph completion or unrequested tree loss is inferred.
Identity files retain their exact bytes. Supplementary checks compare literal
atom types, isotopes, formal charges, bond roles/orders, source serial strings,
nm positions and mechanics fields. A new-test expectation was corrected to the
actual `get` contract for wholly unknown formal charges: None, not a list of None.
This was a harness correction, not a chemical behavior change.

### Dependency-isolation defect found by execution

A fresh-interpreter sentinel retaining find_spec availability queries but
rejecting actual engine module creation found uibcdf/molsysmt#426: recognizing
explicit `pdbqt_text:` used the generic string sweep and reached the unrelated
RDKit SMILES parser. Conversion still succeeded after the caught ImportError;
a simple successful-output assertion would have missed the unwanted dependency.
The generic repair indexes declared prefixes in the form catalogue and still
confirms candidates through their actual registry-backed detectors. Extension
priority, rejected-candidate fallback, detector errors and dynamic registry
behavior remain guarded. No parser, public signature or scientific method changes.

The final sentinel executes every direct/public witness without attempts to load
RDKit, MDAnalysis, MDTraj, OpenMM or Vina. The full regression, including the
all-forms recognition battery, registry integration, real Vina example files,
independent RDKit/MDAnalysis readers, Vina parser acceptance, chemistry/unit
controls and AutoDock typing regressions, passes **1,015 tests**, zero
failures/skips, in 52.00 seconds with 12 workers and Pytest Receptor.

The [receipt](../../devtools/data/conversion_execution_docking_20261022.json)
records actual versions, commands and 47 warnings. These include the previously
unexplained ndarray-size warning retained under uibcdf/molsysmt#237 for the
installed-environment review; fresh provider imports still do not reproduce it.
The public get_form doctest and two affected User Guide/course notebooks pass;
the developer testing page renders with zero diagnostics in a focused project.
No full-site warning recount, format-scope expansion or installed-pair
qualification is claimed. #181 remains partial and #334 still owns release gates.

## SDF input variants extended — 2026-10-22

The same 19 docking-format edges now use four SDF variants (V2000, V3000,
legacy blank version and declared zero valence), or two PDBQT variants. This
produces 48 cases, each executed directly and publicly with fresh inputs. The
actual-loader isolation subprocess executes all 48 cases. Extra assertions check
retained H inventory and disabled implicit-H permission. The grammar extension
and independent original-file tests belong to uibcdf/molsysmt#215.

The graph profile remains `resident-files-v5`: 133 selected / 596 declared edges,
463 explicit coverage-debt edges. More witnesses strengthen covered routes;
they do not count as additional conversion edges or close #181.

## MDAnalysis Universe expansion — 2026-10-23

The `resident-files-v6` profile adds seven declared routes: Universe identity,
PDB, MDTraj, MolSys, Topology and Structures outputs, and PDB-to-Universe.
It now selects **140 of 596 edges**, with 456 individually listed coverage-debt
edges. Only the seven newly covered routes leave that debt inventory; no graph
edge is removed or added. Resident/PDB executors remain a disjoint partition.
Fresh provider-native water fixtures carry three atoms and two distinguishable
structures, explicit topology and cells, angstrom coordinates and degree angles.
MDAnalysis setup skips only if the optional provider is unavailable.

Execution found two argument-boundary defects under uibcdf/molsysmt#432: an
unvalidated boolean writer flag and an ndarray/list mismatch for direct selected
PDB output. Fourteen mirrored guards protect early rejection before writer or
destination changes, valid single/multiple-structure output and literal selected
coordinates. The original controls had eleven failures and three passes; the
repair restores ordinary validated delegation rather than bypassing digestion.

The combined regression passes **379 tests**, zero failures/skips, in 34.31 seconds
with twelve workers and Pytest Receptor. All 27 warnings are legacy H5MSM notices.
It includes the entire conversion-truth suite, MDAnalysis adapters, atom-map
composition, execution-inventory controls and argument contracts. The atom-map
digester formatting correction is included in this execution; earlier CI rejected
its formatting even though lint passed. Whole-checkout Ruff lint and formatting
now pass, as do the fourteen fast gates.

The [receipt](../../devtools/data/conversion_execution_mdanalysis_20261023.json)
records versions, commands and tested source hashes. #181 remains partial: this
is bounded route execution, not all-attribute fidelity or installed/release
qualification. #334's release pause and external-package gates remain unchanged.


## PDBQT handler execution extension — 2026-10-23

The profile is now `resident-files-v7`: 149 selected out of 605 declared edges,
with 456 individually listed unexecuted edges unchanged. Nine newly declared
PDBQT handler routes are executed, not added to accepted debt. The docking
executor owns file/text-to-handler and all seven handler outputs, while the
native executor excludes the technical handler to keep the partition disjoint.
Rigid and ligand witnesses exercise direct/public routes, literal values,
source text identity, tree-loss authorization and resource closure. The fresh
optional-engine guard includes every new route. These are bounded execution
and value controls, not large-file throughput or full conversion-graph coverage.
The [operational guide](../conversion_execution.md) owns the current commands;
#181 stays partial for the remaining routes.

### Validation receipt — 2026-10-23

The combined PDBQT/known-source poses/naming/atom-map/conversion execution,
argument/plugin and preparation-tool selection passed **661 tests** in
39.94 seconds with `--receptor=llm -n 12` (32 warnings: 25 legacy-H5MSM,
6 MDAnalysis mass deprecations and the known optional binary-size warning).
The final shaped-empty-ID follow-up is covered by the handler guard. The
four public-tool/reader doctests passed; the file-reader example also passed
again after using its own strict file namespace. Both maintained course modules
executed successfully. All 14 fast repository gates passed. No full scientific
or installed release matrix was run, and no large-file benchmark is claimed.

The machine-readable scope, source hashes and limitations are recorded in
[`pdbqt_handler_20261023.json`](../../devtools/data/pdbqt_handler_20261023.json).

## MDAnalysis AtomGroup and Topology extension — 2026-10-25

The `resident-files-v8` profile selects **157 of 606 declared edges**, leaving
449 explicitly listed unexecuted edges. The inventory immediately before this
extension was 150/606 with 456 deferred edges; the earlier 149/605 receipt records
its own dated graph. Only the seven newly selected routes are removed from debt:
the four AtomGroup outputs, the two MDAnalysis.Topology outputs and
PDB-to-MDAnalysis.Topology. No converter or declared route is changed.

The resident fixture returns a partial reordered AtomGroup with parent indices
`[2, 0]`, or a copied provider topology. The existing PDB executor supplies its
literal water record. Separate direct/public contracts test two local selection
orders against a four-atom, two-group Universe, selected structures `[2, 0]`,
retained bonds, source labels, native string IDs and nm geometry. They also check
that source coordinates and the source trajectory cursor are unchanged.

An initial test incorrectly expected native extraction to preserve the requested
atom order. Inspection confirmed that `Topology.extract()` sorts source atom
indices and the Universe-to-MolSys converter applies the same ordering to both
topology and coordinates. The corrected oracle explicitly checks this established
native contract as well as MDAnalysis's requested-order output. No ordering
semantics were changed, and no converter defect was confirmed in this extension.
PDB-to-provider topology additionally checks literal names, labels, group count
and CONECT bonds without comparing against another MolSysMT conversion.

The regression command in the [receipt](../../devtools/data/conversion_execution_mdanalysis_subsets_20261025.json)
passes **416 tests**, zero failures or skips, in 35.27 seconds with twelve workers
and Pytest Receptor. The 37 warnings are 28 legacy-H5MSM notices and nine provider
PDB default-field/cell notices. Whole-checkout Ruff lint and formatting and all
14 fast gates pass. The audit reports 157 planned routes; the parametrized runtime
tests provide the separate execution evidence. #181 remains partial. This is
bounded local source qualification, not an installed-pair, full-graph or release
qualification; #334's publication pause is unchanged.
