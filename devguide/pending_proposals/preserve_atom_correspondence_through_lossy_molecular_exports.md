---
summary: Preserve atom correspondence through lossy molecular exports
issue: uibcdf/molsysmt#223
status: partial
opened: 2026-09-22
closed:
verification: reproduced
area: [form, convert]
guard:
normative:
blocked_by: []
supersedes: []
---

# Preserve atom correspondence through lossy molecular exports

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Partial. Typed-H projection, completed PDBQT maps, known-source pose
reading and typed stage composition are implemented. Explicit backend atom-name
projection and consumer adoption remain pending.

## What

Return an explicit mapping between source and exported atoms when a molecular form omits or merges atoms.

## How

Define a post-conversion mapping artifact with retained, omitted, and merged source atoms, reasons, charge aggregation, and source state identity; keep the source MolSys unchanged. For the PDBQT example, the selected atom-typing policy, rather than atom names, determines which hydrogens are retained or merged.

## Why

PDBQT hydrogen conventions and returned docking poses require atom identity beyond a preflight conversion-fidelity report.

## What is measured and what is assumed

**Inspected:** Inspected molsysmt/basic/conversion_report.py and current PDBQT proposal; Meeko documents hydrogen merging by atom type.
**Assumed:** The proposed contract is useful for the stated consumer; quantitative impact and complete chemical coverage need representative validation.

## What was refuted

Treating the existing preflight conversion report as the completed atom map was rejected because it does not record the resulting atom-level projection.

## Scope and exclusions

Reusable mapping contract and PDBQT exemplar; no universal atom matching between unrelated molecules.

## Acceptance criteria

- A loss-aware export yields a stable source-to-output and output-to-source mapping with reasons for omitted or merged atoms.
- Tests cover retained polar hydrogens, merged nonpolar hydrogens, charge aggregation, and unchanged source identity.
- Tests reject a name-based hydrogen projection when atom names and chemical types disagree.

## Dependencies and risks

Related tracked work: uibcdf/molsysmt#214
Cross-component implementation links: uibcdf/dockingmt#5, uibcdf/dockingmt#8.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.

## Preparation work ordering — 2026-10-03

The maintainer requested chemical preparation alongside real SDF/PDBQT
validation. Follow [the maintained sequence](../roadmap.md) and the consumer
profile review in uibcdf/dockingmt#33. Related template and fixed-state H
capabilities are owned by uibcdf/molsysmt#298 and uibcdf/molsysmt#300.
Prioritization does not establish implementation, scientific coverage or a new
blanket 1.0 gate. Keep this issue's acceptance criteria and general-tool owner
distinct from format parsing and DockingMT protocol decisions.

## Typed-H projection and completed export maps — 2026-10-22

**Implemented and contract-tested:** `build.merge_nonpolar_hydrogens` is a
form-agnostic public building operation. It consumes explicit AutoDock4 labels
and source charges, without assigning either or importing a chemical engine
for ready native inputs. Label H, not an atom-name/element heuristic, selects
terminal neutral nonisotopic H. HD remains indexed. The parent must be retained
by the same atom selection and have a known virtual-H inventory with zero
implicit H. Parent virtual explicit-H counts increase and further implicit-H
inference is disabled. The source is unchanged, and reduced analyses are cleared
after merging. Unsupported force-field settings are rejected instead of
pretending to derive a united-atom force field.

The optional `molsysmt.atom_projection@1` report uses compact arrays: retained
source/output indices, -1 for absent direct correspondence, separate merged
H/parent pairs, selected/excluded scope, source/output IDs/names, state label
and chemical digest, original structure indices and charge transfers/totals
with explicit elementary-charge units. Full-precision selected charge is
conserved within a reported floating-point tolerance; there is no rounding or
renormalization here. A merged H does not acquire its parent's coordinate.

Named charges become an explicitly derived aggregation assignment with the
original calculation report nested unchanged, including producer versions,
parameters and attribution. Named types are inherited with a derived binding
after the explicit chemical representation change. Copy/pickle and writer
validation preserve these distinctions; stale direct edits still fail.

Both native PDBQT writers add keyword-only `return_atom_map=False`; ordinary
returns and serialization policy are unchanged. True returns the output plus
a `molsysmt.atom_export@1` report recording the actual parsed written order,
serials, selected full-input indices, ordered ROOT and first atom, oriented
branches, tree, three-decimal charge loss and payload SHA-256. Composition with
the projection inverse map is direct array indexing, independent of coordinates.
Name width violations still fail; names may repeat because serial IDs carry
identity. Explicit name changes can be traced by comparing original projection
labels and written labels along these maps; no implicit truncation or renaming
is introduced. The API registry records two function-scoped additive signature
waivers with concrete guards, and the converter-argument domain is regenerated.

The independently implemented terminal charge-transfer contract was inspected
in Meeko 0.8.0 at `1eac18bd6d1111f35f9f1abaa8af502c2668d054`,
`meeko/molsetup.py::merge_terminal_atoms`. No implementation is copied or
executed. Detached result references and optional Ackredit record its role as
reference implementation; original charge calculations are not credited as
executing again. Existing native projection, chemical inventory, assignment
binding and PDBQT serialization tools are reused.

Primary evidence is `tests/build/test_merge_nonpolar_hydrogens.py`: independent
methanol has explicit selected/excluded/merged controls and misleading atom
names; named Gasteiger methanol matches the DockingMT numeric case. Original
1IEP and 5X72 ligand files retain their hashes and source-indexed coordinates,
with 69→40 and 39→25 atom reductions under the current typing profile. Those
real-file transfer controls use declared synthetic charges; they do not
reproduce published docking charges or certify scoring suitability. Tree-order
controls use nonconsecutive serial IDs and reversed ROOT order.

**Bounds at the first delivery checkpoint:** reports referred to this prepared input. Earlier
generated atoms need their own preparation history/map (including explicit
absence of a pre-generation source index); no source identity is invented.
There is no general map-composition/discovery engine or new map persistence
domain. MolecularMechanics remains outside H5MSM 0.5. Consumer qualification
and retirement of DockingMT's transform are still owned by uibcdf/dockingmt#49,
uibcdf/dockingmt#5 and uibcdf/dockingmt#33. MODEL-aware known-source reconstruction remains #226.

Qualification exposed uibcdf/molsysmt#430: the supported three-native-domain
route rejected object-backed charge arrays; numeric adapter delivery repairs
that slice. Explicit four-domain metadata routing remains pending in #430.
The new builder delegates composition rather than implementing a competing path.

The maintained user contract is
[the projection tutorial](../../docs/content/user/tools/build/merge_nonpolar_hydrogens.md).
User Guide, native PDBQT recipe, API docstrings and course Module 12 are updated.
This bounded implementation does not close the broader proposal or qualify
a release/installed artifact.

### Qualification checkpoint

The [source receipt](../../devtools/data/atom_projection_20261022.json) records
command, environment, executable-file hashes and scope. The final regression
selection passed **799 tests**, zero failures/skips, in 50.51 seconds with
12 workers and Pytest Receptor. The 39 warnings comprise 30 legacy H5MSM notices,
six MDAnalysis deprecations, two expected structural-drop notices and one
optional NumPy binary-size warning already recorded under #237.

The new builder's meaningful doctest passed (1.30 s); User Guide code blocks
execute as one tested workflow. Updated course Module 12 executed in 18.5 s.
Ruff check/format, 248 public docstrings, the API stability guard and all
14 fast gates pass. API/scientific-evidence generated views are refreshed;
this is not new scientific admission. No full or installed matrix was started.


## Known-source pose consumer delivered — 2026-10-22

#226 now implements `molsysmt.form.read_pdbqt_poses` with completed export maps,
all-model identity validation and explicit missing-atom policy. New writer maps
include `output_atom_ff_types` to validate a pose even with a topology-only known
source. This is an additive typed field, not a payload or mapping-axis change.
The bounded reader is documented in the
[User Guide](../../docs/content/user/tools/form/read_pdbqt_poses.md); its delivered
contract/evidence lives in the
[resolved #226 record](../archive/resolved_proposals/read_pdbqt_pose_ensembles_against_a_known_ligand_source.md).
Earlier generation-map composition and downstream adoption remain separate
pending #223 work.


## Native-provider composition repaired — 2026-10-22

#430 is resolved for explicit standalone native domains. Four-domain input
`[Topology, ChemicalStates, Structures, MolecularMechanics]` now joins the owning
native composition seam, preserves complete mechanics reports and validates full
axes before selection. Explicit ChemicalStates supplies chemistry rather than
list-order attribute overrides. See the
[resolved record](../archive/resolved_bugs/native_domain_composition_fails_on_charges_and_explicit_chemical_state_metadata.md).
This repair does not complete #223's upstream atom-map composition or receiving.


## Typed stage composition — 2026-10-23

`form.compose_atom_maps` now joins the existing terminal-attachment, fixed-state
hydrogen-addition, typed-H projection, PDBQT writer and known-source pose reports,
plus explicit `molsysmt.atom_map@1` declarations. It returns detached int64 direct
maps with -1 for absent origin/correspondence, a separate representative array
for fusion and generated-output indices. A generated atom never receives an
invented pre-generation index; a merged H never receives its parent's position.
Representatives can follow later fusion, and disappear if their recipient is
omitted. Original local merge/parent evidence remains in normalized stages.

The result is sparse by correspondence (one-dimensional axes, not atom-pair
matrices). Counts, inverse partial permutations, typed indices and available
adjacent labels are checked; intentional renaming needs an explicitly declared
identity-index stage. Reports are declarations, not authentication of origin or
chemical matching. Incremental composition flattens prior normalized stages and
checks their aggregate arrays/labels before joining another operation. JSON
array lists restore through the same public boundary.

A pose report is adapted from its known-source graph domain to its sequential
input **written PDBQT atom order**; the output is the reader's native order. This
is essential when the writer selected fewer atoms than the known source or
reordered ROOT. Its declared export SHA-256 binds the previous writer stage.
No structure-index composition, geometry recovery, atom matching or new charge
calculation is performed. Original structure selections remain stage metadata.

Normalized stages preserve producer/method/engine/parameters, references and
optional scientific attribution without crediting those calculations again.
Original charge totals, conservation/rounding bounds and local transfers carry
explicit elementary-charge units. Writer ROOT order, first ROOT atom and oriented
source branch pairs retain their stage-local source domain; the torsion tree
retains its written output axis and reuses the existing PDBQT tree validator.
Full original readiness/inventory reports and coordinates are not duplicated.
The result is a typed sidecar, not a molecular form or H5MSM schema extension.

Primary guard: `tests/form/test_compose_atom_maps.py`. It uses independent
expected arrays; actual terminal/H generation, charge aggregation, writer order
and pose pipelines; omission after a merge; incremental/JSON stages; explicit
rename evidence; malformed maps/creation/charge records; rooted branch direction;
empty and 100,000-atom array scopes; and a fresh-process optional-engine/Ackredit
loader rejection. The complete User Guide workflow executes and course Module 12
is synchronized. The final source selection passed **568 tests**, zero failures/skips, in 42.48 s
with 12 workers and Pytest Receptor. The 39 retained warnings are 29 legacy H5MSM,
six MDAnalysis mass deprecations, one previously recorded optional NumPy ABI-size
warning and three expected structural-attribute drops. One meaningful doctest,
all 250 public docstrings, Ruff, the signature guard and all 14 fast gates pass.
The final Module 12 executed in 18.5 s. The
[source receipt](../../devtools/data/atom_map_composition_20261023.json) records
commands, environment and executable hashes. This is source-level contract and
pipeline evidence, not a new installed artifact or complete chemical validation.

### Remaining provider and consumer slices

The backend atom-name projection requested in the 181L consumer comment remains
explicitly unfinished. `msm.set` can apply caller-selected names and this new tool
can record a declared rename, but it does not choose/apply a backend naming policy
or replace that consumer preparation operation. No implicit truncation or
collision-renaming was added. Existing PDBQT width/serial checks remain active.
This issue stays partial rather than claiming those added consumer criteria or
production adoption are complete. DockingMT receiving/removal stays owned by
uibcdf/dockingmt#49/#5/#33; a known full molecular permutation stays #369.
