---
summary: Add PDBQT file and string forms with MolSys conversion
issue: uibcdf/molsysmt#214
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

# Add PDBQT file and string forms with MolSys conversion

**Reported:** 2026-09-22, from the DockingMT Vina integration discussion and inspection of the form registry.
**Status:** Partial. The maintainer brought the bounded adapter work forward
on 2026-10-02. Experimental native file/string adapters now read rigid receptors
and homogeneous MODEL ensembles with invariant ligand trees, and write explicitly
supplied data. Output-only presentation and final-byte caller remarks are now
implemented; consumer reception of that contract and wider supported-profile
acceptance remain pending. General preparation tools have separate owners.

## What

Add file:pdbqt and string:pdbqt forms with supported conversions in both
directions with molsysmt.MolSys. These are general molecular-system forms in
MolSysMT, even when a docking program is the first consumer. Track the
downstream use in uibcdf/dockingmt#3.

## How

- Register both forms through the normal lazy form catalog and dependency
  mapping. Provide working public conversion routes to and from MolSys; a
  file/string bridge may share one parser and writer internally.
- Define the first supported layouts: a rigid receptor and a single ligand
  with a valid torsion tree. Homogeneous MODEL ensembles use the structure axis; flexible-receptor and
  changing-identity variants must fail explicitly until their semantics are specified.
- Map only fields PDBQT carries: coordinates, atom identity, partial charge,
  AutoDock atom type, and available torsion information. Convert angstroms to
  MolSysMT nanometers and keep native element IDs as strings. Do not infer
  complete connectivity or bond orders from absent PDBQT data.
- Require writer inputs appropriate to the selected layout, including atom
  typing, charges, geometry, and ligand torsion data. Missing or inconsistent
  input must fail clearly; serialization must not silently perform chemical
  preparation. Use conversion reports and strict mode for representational loss.
- Define the selected PDBQT hydrogen policy explicitly. If a profile merges
  nonpolar hydrogen atoms, classify them by the declared chemical typing scheme,
  transfer their partial charges to the bonded parent, retain required polar
  hydrogens, and return the atom projection described in uibcdf/molsysmt#223.
  Atom names alone must never decide which hydrogens disappear.
- Declare attributes only where public getters actually deliver them, with
  instance-aware presence. Any parser/writer backend remains optional and
  lazy. This proposal does not require Meeko.

## Why

DockingMT's current Vina adapter supplies a receptor PDBQT file and a ligand
PDBQT file or string to Vina. A shared PDBQT form lets DockingMT use MolSysMT's
native molecular-system representation without embedding general file parsing
and writing in its docking layer. This is an architectural judgement based on
source inspection, not a performance claim.

## What is measured and what is assumed

**Inspected at filing:** molsysmt/form had no PDBQT form. Existing file and string forms
use registered conversion edges and capability declarations. DockingMT's
dockingmt/engines/vina.py supplies PDBQT inputs to Vina. No timing or
chemical-fidelity measurement was made.

**Assumed:** A useful first subset can be specified without treating every
PDBQT dialect as equivalent. The exact dialect fixtures need to be chosen
during implementation.

## What was refuted

Keeping PDBQT only inside DockingMT leaves a general file form unavailable to
other MolSysMT consumers. Converting directly into Vina's private engine state
does not provide a public file or string form contract.

## Scope and exclusions

This issue owns PDBQT recognition, parsing, writing, capability metadata,
conversion semantics, and fidelity tests. It does not own general charge
assignment, hydrogen placement, atom typing, or rotatable-bond perception;
those are separate preparation capabilities to specify later. It does not
own DockingMT protocol decisions or Vina execution. This is new form coverage. The maintainer brought the bounded adapter work
forward before 1.0 on 2026-10-02; the broader preparation model remains separately
tracked.

## Acceptance criteria

- Form discovery recognizes PDBQT files and explicit PDBQT strings; public
  conversion works in both directions between each form and MolSys.
- Representative rigid-receptor and flexible single-ligand fixtures parse and
  serialize with correct atom alignment, coordinates, units, supported charges,
  types, and torsion records. Tests compare equivalent supported content
  across file, string, and MolSys routes.
- Missing writer inputs and unsupported layouts fail with actionable errors.
  Lost attributes are not claimed as preserved by capability declarations or
  reports; strict mode rejects known loss.
- Tests exercise the declared hydrogen policy on ligand and rigid-receptor
  fixtures, including polar H retention, charge aggregation for merged H,
  source-to-PDBQT atom mapping, and an unchanged source MolSys.
- Tests cover selection and structure-index behavior where meaningful,
  optional dependency behavior, and public API routes. Docstrings, User Guide,
  Cookbook, and applicable course material describe the supported subset.
- The durable contract is incorporated into
  [forms_and_conversions.md](../forms_and_conversions.md) before closure.

## Dependencies and risks

The ligand writer needs a specified torsion-tree input contract. If MolSys
cannot carry it, resolve that general representation separately before
claiming flexible-ligand output (uibcdf/molsysmt#224). PDBQT atom types are
not necessarily general force-field atom types; their mapping must be explicit
(uibcdf/molsysmt#222). Hydrogen projection and mapping are tracked in
uibcdf/molsysmt#223. Flexible receptors and multi-model pose output remain
separate in uibcdf/molsysmt#225 and uibcdf/molsysmt#226. The downstream
consumer is tracked in uibcdf/dockingmt#3.

## Current representation boundary (2026-10-03)

Source inspection distinguishes AutoDock atom types from chemical element
symbols (`atom_type`), and declared BRANCH torsion edges from complete covalent
connectivity. PDBQT contains no complete bond-order inventory. Parsing must not
claim a complete graph, fabricate charges, or store torsion records in an
unrelated native field. Ordinary chemical-symbol normalization is reusable
under uibcdf/molsysmt#296; general explicit typing/profile and rigid-fragment
capabilities remain owned by uibcdf/molsysmt#222 and #224. No PDBQT form has
been delivered by the CIP/SDF stage.



## Implementation checkpoint — 2026-10-03

**Implemented / Contract-tested:** `file:pdbqt` and explicit
`string:pdbqt_text` (`pdbqt_text:` prefix), native MolSys and reduced-domain
projections, declared AutoDock4 charge/type parsing, fixed-column writing,
partial BRANCH connectivity, source serial IDs, residue/chain fields,
coordinates/occupancy/B factors, typed declared tree access, native writer
validation, selected rigid projections, conservative reports and strict mode.
File/string identity routes retain payload, line endings, tree and remarks,
including explicit complete index selections. A full native ligand conversion
requires explicit authorization to omit the tree. No general native torsion
store was introduced. The public format `get_torsion_tree` dictionary is bound
to source atom IDs and indices and can be supplied to the writer separately.

The writer requires explicit `typing_scheme='autodock4'`, supplied types and
partial charges, one structure and valid field widths/IDs. Tree consistency is
validated before destination mutation. For a complete native graph, it calls
the public `topology.get_rigid_fragments` tool to verify branch cuts and fragment
memberships. Geometry is explicitly serialized in angstrom, B factors in
angstrom squared and charges in elementary charge, irrespective of session
unit policy. Every present hydrogen is retained; hydrogen merging, charge
aggregation, chemical typing and torsion perception are deliberately separate
preparation capabilities. Tree traversal may reorder atom lines; stable source
serial IDs carry the correspondence. Source MolSys domains are not modified.

Known source metadata and full native chemistry/domain losses are reported.
Strict mode cannot be bypassed by `discard_torsion_tree=True`. The bounded
native writer audit remains conservative, not exhaustive. Arbitrary remarks,
record kinds, full connectivity and chemistry cannot be claimed to survive a
native projection. MolecularMechanics remains excluded from H5MSM 0.5, so
that format does not preserve PDBQT charges/type labels for later writing.

**References inspected:** AutoDock4.2.6 manual, Vina parse_pdbqt.cpp and atom
constants, and Meeko's documented PDBQT grammar. An existing Vina basic-docking
ligand (40 atoms, seven branches) was read and serialized as a source check;
its data are not added as a dependency or copied into bundled systems.
Independent MDAnalysis comparisons cover atom IDs, coordinates, charges and
labels on committed hand-written rigid/ligand fixtures. These are bounded
format parity checks, not validation of a preparation algorithm.

**Guards:** `tests/form/file_pdbqt/test_native_contract.py` covers identity and
native routes, tree roles/indices, ROOT-only and nested/sibling layouts, source
immutability, all-H retention, explicit selections and frame bounds, malformed
records, extended-dialect rejection, invalid writer input/tree before file
mutation, full-graph agreement, strict losses and a non-default unit policy.
No speed or memory benchmark has been performed.

**Pending before closure:** curated prepared receptor/ligand coverage and
supported-profile review with DockingMT; broader writer completeness/report
validation; an explicit decision on the general native torsion/preparation
model. AutoDock chemical assignment (#222), charge models (#221), nonpolar-H
projection/aggregation (#223), rotatable-bond perception (#224), flexible
receptors (#225) and pose ensembles (#226) remain separate work. The current
all-H-preserving profile does not satisfy the acceptance checks for a future
merging profile; no claim of such preparation is made.

## Verification summary — 2026-10-03

The combined atom-type/PDBQT/SDF/conversion-report/plugin regression passed
415 tests in 80.23 seconds. This includes the two new public tool doctests.
The final focused selection passed 73 tests in 9.27 seconds, including
follow-up mechanical getter index bounds and a tree writer with an atom domain
but no evaluated chemical state. Its count overlaps the combined selection
and is not additive.
Ruff, API stability, docstrings, form delivery, dependency imports/contracts,
developer-guide and maintained course-structure gates passed. Sphinx HTML
compiled with existing repository warnings and no new PDBQT/tool reference
warnings. The maintained devtools course-structure validator passes.

**Combined-query follow-up:** The final integration inspection exposed a
general get dispatcher defect: it grouped topology/structure requests but
omitted mechanical attributes from mixed results. Resolved under
uibcdf/molsysmt#301 with a central dispatcher fix and a source-value/selection
regression guard. The subsequent PDBQT and existing-query selection passed
292 tests in 37.21 seconds, including reduced and shared native pipes. This
selection overlaps earlier counts and must not be added to them.

## Consumer review and next validation — 2026-10-03

The maintainer requested review of related pending capabilities and chemical
preparation alongside real-input validation. uibcdf/dockingmt#33 asks the
consumer to test the delivered adapters at `eb0549b50` and review its actual
required profile. The ordered provider work is maintained in
[the roadmap](../roadmap.md#current-sdfpdbqt-and-chemical-preparation-sequence--2026-10-03),
with preparation retaining its separate owners (#217/#218/#298/#300 and
#221/#222/#223/#224). Do not close those capabilities through parser acceptance.

Start the real-input matrix with pinned 1IEP, 1S63 and both 5X72 stereoisomers
already curated by DockingMT and a conventional rigid receptor. In particular,
1S63 has a reference-only hydrogen and a published aryl–nitrile branch absent
from the compared RDKit Strict policy. Test those differences explicitly rather
than deriving correspondence from equal counts. Compare branch bonds/fragment
sets, actual source serial-ID and index axes, supported charge/type values,
precision, source preservation and deliberate rejection controls. Record hashes
and independent reader/engine versions before extending fidelity claims. This
checkpoint is an inspected plan and consumer request; it contains no additional
executed validation or scientific preparation result.

## Original Vina corpus checkpoint — 2026-10-03

**Contract-tested and bounded reference comparison:** the four ligand records
and the 2,702-atom rigid 1IEP receptor are now committed, byte-unmodified, in
`tests/form/data/vina_examples`, with licensing, source hashes and a literal
manifest. `tests/form/file_pdbqt/test_real_vina_examples.py` checks public getters,
nm/pm unit policies, partial chemical connectivity, exact source identity,
supplied typing/charges, branches/fragments, source immutability and independent
MDAnalysis parsing. All five native outputs are accepted by Vina 1.2.7's parser;
this is parsing, not docking, affinity validation or preparation.

`tests/topology/test_rigid_fragments_real_vina_examples.py` verifies explicit
source-bond cuts against the published ligand trees. Coordinate-based atom
projection is limited to these pinned, already aligned sources, requires unique
same-element matches within 0.002 angstrom and explicitly accounts for 1S63's
one reference-only H. Its aryl–nitrile branch (source indices 26/27) is preserved
as declared, without adopting that torsion as a universal chemical policy.

The combined relevant regression passed 418 tests in 104.48 seconds. Environment,
command and warning details are recorded in
[the #302 resolution](../archive/resolved_bugs/sdf_identity_copies_require_native_chemical_interpretation.md).
This extends adapter evidence without resolving #221/#222/#223/#224 preparation
policy or claiming automatic chemical typing, charge assignment or H merging.
The subsequent bounded consumer evidence and current stabilization review follow;
broader acceptance remains pending and this issue stays partial.

## Frozen-profile stabilization — 2026-10-05

The S3 review at `fe0b813d7267f4c5a0728264094441e62c910e1b` reruns the
native and original-Vina PDBQT controls as part of the 1,094-case preparation/form
selection, without failures or skips. The [execution ledger](../release_1_0_status.md#s3-preparationform-qualification--2026-10-05)
and [artifact](../../devtools/data/preparation_profiles_20261005.json) own the
command, fixture hashes, dependency/producer identity, warnings and full scope.
Independent MDAnalysis reading and Vina parser acceptance execute; neither
certifies preparation or docking accuracy.

Published uibcdf/dockingmt#33 contains accepted prepared-input and subsequent
fragment/readiness/charge/H integration slices. These historical observations
are inspected, not rerun on this source. Broader consumer policy, dialects,
projection and chemistry remain separate. Named charge/type assignment and
native graph torsion candidates are now implemented general tools, called
explicitly outside the adapters. The updated recipe reflects them and H5MSM
0.5's rejection of nonempty MolecularMechanics. The bounded profile ships
experimentally; remaining extensions stay post-1.0 and this issue remains partial.

## Resident handler and ensemble iteration — 2026-10-23

Implemented and contract-tested: the technical native form
`molsysmt.PDBQTFileHandler`, with public class import
`from molsysmt.native import PDBQTFileHandler`. File/text adapters can create a
handler, and its seven declared direct routes preserve the existing explicit
native tree-loss boundary. It retains the original document, opaque remarks,
MODEL IDs, trees and explicit mechanical labels without inventing chemistry.
All model bodies are validated up front; only one parsed reference body is
retained. Copies have independent close ownership and may share the snapshot.

`StructuresIterator` now exists in the handler, file and explicit-text form
modules. The existing public facade delegates to them without changes to the
principal Iterator. Selected coordinate buffers are block-sized; metadata-only
Topology/MolecularMechanics conversions do not allocate the full ensemble.
The resident source text and up-front full-document validation remain explicit
limitations. Disk-backed indexing and large-file qualification are owned by
[the #434 record](../archive/resolved_proposals/indexed_large_pdbqt_structure_iteration.md).
That resident checkpoint was partial; the indexed checkpoint below records its
subsequent completion.

API organization follows operation ownership: `build.project_atom_names` with
`target_form`, `basic.compose_atom_maps` (also `msm.compose_atom_maps`), and
`form.file_pdbqt.read_poses` / `form.string_pdbqt_text.read_poses`. A handler also
has `read_poses` for known-source coordinate import. These experimental API
moves retain no legacy top-level `form` aliases; no scientific method changed.

Guards are `tests/native/test_pdbqt_file_handler.py`,
`tests/form/file_pdbqt/test_known_source_poses.py`, and the disjoint conversion
execution profile in `tests/conversion_truth/`. The handler User Guide examples
execute in the first guard; the two maintained course modules are re-executed
as part of the same checkpoint. Wider dialect/preparation policy and consumer
adoption remain separate; #214 remains partial.

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

## Indexed storage checkpoint — 2026-10-23

The bounded uncompressed file profile is now implemented and qualified under
uibcdf/molsysmt#434. File getters and per-form structure iterators use indexed
owners; the public handler offers explicit resident/indexed storage, source
consistency checks, shared leases and bounded atomic file output. The dated
benchmark is maintained in [PDBQT storage](../benchmarking/pdbqt.md).
Full validation remains an opening cost; text/full requested outputs and the
known-source mapped metadata retain their documented eager scope. This does
not broaden chemical interpretation or close the remaining #214 scope.


## Consumer presentation and final-byte review — 2026-10-26

The latest DockingMT comments clarify that native chemical reduction, prepared
charge/type transfer and ordinary PDBQT writing are already usable. Consumer
ligand/receptor controls include Vina admission and report successful installed
source reception. Those consumer results are reported evidence, not rerun in
this review. The remaining request is output presentation and caller remarks,
not a replacement parser, preparation engine or implementation of delivered
uibcdf/molsysmt#223.

**Inspected:** the native text adapter currently exposes only `typing_scheme`,
`torsion_tree` and `return_atom_map`. The private writer preserves source atom IDs
as PDBQT serials and preserves absent group/chain fields. It writes its own
truthful original/derived assignment remarks before completing the export map,
but has no caller-remark or output-only label/serial policy. This explains the
consumer's remaining boundary; preservation of the native source is not itself
a writer defect. Changing source IDs by copy/set changes the intermediate map
axis and cannot be treated as output formatting on the original preparation.

The next bounded design should expose explicit optional output presentation on
the native string/file routes: serial policy, names, per-atom group/chain labels
and optional occupancy/B-factor values. These belong to the serialized view and
must not invent group membership, modify native molecular IDs or replace
chemical/mechanical stores. An independent validated caller-remark input should
exclude record/newline injection and coexist with provider provenance. No API
names are fixed by this review.

Validate every override before producing output, preserve the declared rooted
tree and source-axis bindings, and form the completed map/hash from the final
actual bytes after all remarks and presentation. Test reordered tree output,
nonconsecutive source IDs, composed preparation/export maps, zero-group sources,
field-width failures and unchanged destinations/sources, both native file/text
routes, and nondefault length/charge policies. Coordinate and chemical preparation
remain unchanged. This is a proposed implementation block under the existing
#214 theme; no writer code or contract is changed by this review.

The existing `molsysmt.atom_export@1` payload already distinguishes
`source_atom_ids` and `output_atom_ids`. Its current writer derives output-to-source
indices by looking up written serials among source IDs. Once presentation can
choose different serials, that implementation must derive correspondence from
the actual serialization traversal/explicit index mapping instead. Keeping source
IDs untouched and using this existing mapping contract is preferable to a
consumer-side relabel/copy/rebind workaround. No schema change is assumed here.

## Output-presentation implementation — 2026-10-26

**Implemented / Contract-tested:** native `to_file_pdbqt` and
`to_string_pdbqt_text`, also through public `convert`, accept keyword-only
`output_presentation` and `remarks`. Presentation owns output serials/names,
per-atom group/chain labels and optional occupancy/B factors. Scalars broadcast;
vectors use the original input atom axis before native sorted extraction.
Consecutive serials follow actual rooted write traversal, including a child
endpoint written before the other members of its fragment. An explicit serial
policy supports arbitrary original source labels. Source hierarchy, IDs,
chemical state and charge/type assignments are unchanged.

The writer validates field widths, serial uniqueness/bounds, finite real optional
values and squared-length B-factor quantities before destination mutation.
Caller lines must be printable ASCII complete REMARKs, at most 4096 characters
each and 64 KiB total. Newline/control injection and the reserved MOLSYSMT_
namespace fail. Original/derived provider provenance remains intact. UTF-8 file
writing disables newline translation, and completed export maps/hash describe
final actual bytes after all remarks/presentation. The existing atom-export
schema suffices; no competing chemistry store or map-rebinding workaround exists.

The inverse map now comes from actual traversal indices, independent of output
serials. The known-source reader formerly assumed output names/IDs equalled
source labels. It now validates the chemically bound original source separately
from the declared written labels, while continuing to require every pose's
exact written order, names, elements, charges, types and tree. Returned atoms
retain original source labels. Projection/export/pose composition is tested
with both declared data and real named charge/type assignments. No matching,
chemical perception, implicit hydrogen merging or source authentication is added.

The format-specific validation helper remains private. Public preparation,
naming and map-composition tools retain their independent contracts. Optional
structural columns are converted once per export, rather than once per atom;
this checkpoint claims no measured speedup or peak-memory result.

**Guard:** `tests/form/file_pdbqt/test_output_presentation.py` exercises both
direct/public and file/text routes, source-axis selections, reordered tree
serials, zero-group/chain sources, arbitrary/duplicate source IDs, valid default
preservation and explicit optional clearing, bad fields/units/remarks with an
unchanged existing destination, known-source pose restoration, composed H
projection, intact provider provenance and final-byte hashes. All five pinned
Vina records cover chemistry/geometry preservation and actual Vina parser
admission. These are format checks, not docking or preparation certification.

The User Guide Foundations, MolSys conversion tutorial, pose-reader tutorial,
prepared-PDBQT Cookbook, converter/reader docstrings and course Module 12 reflect
the boundary. [Forms and conversions](../forms_and_conversions.md) owns its
durable developer rules.

**State:** the bounded provider implementation for the latest consumer request
is delivered in this checkpoint. #214 remains partial pending DockingMT review
of that new public presentation contract and the wider supported-profile
acceptance already tracked here. Prior consumer reports describe the older
provider and cannot qualify these new options. No installed consumer reception,
release artifact, docking accuracy or broadened dialect is claimed.

### Presentation validation receipt — 2026-10-26

The relevant PDBQT/handler/pose/preparation/naming/map/argument/conversion and
raw notebook-schema selection passed **905 tests** in 41.17 seconds with
`--receptor=llm -n 12`, without skips. Ten warnings are the known six MDAnalysis
mass deprecations, three intentional legacy-H5MSM warnings and one optional
binary-size warning. The final quantity-vector selection follow-up passed its
two overlapping cases in 4.93 seconds. The current new presentation guard has
50 cases, including five actual Vina parser receptions.

Four converter/pose-reader docstrings passed all **41 doctest examples**.
The two maintained notebooks executed successfully. The five pinned Vina
records retain byte-identical default output against the pre-change writer,
including the 2,702-atom receptor; their payload hashes are recorded in the
receipt. Ruff, 251-function docstring validation and all **14 fast gates** pass.
The incremental Sphinx HTML build completes without errors, with 26 warnings
from existing course heading conventions and excluded documentation pages;
this is not a warning-free full documentation qualification.

Machine-readable commands, environment, source hashes, default-byte parity and
limits: [PDBQT presentation receipt](../../devtools/data/pdbqt_presentation_20261026.json).
No full-suite, installed-consumer or release-matrix pass is implied.
