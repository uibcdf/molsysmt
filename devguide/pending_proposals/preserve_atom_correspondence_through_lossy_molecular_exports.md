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
**Status:** Partial. A public typed-H projection and completed PDBQT export
map are implemented; generalized upstream generation-map composition and
consumer adoption remain pending.

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

**Bounds and remaining work:** reports refer to this prepared input. Earlier
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
