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
and single ligand trees and write explicitly supplied data. Chemical preparation
and wider acceptance validation remain pending.

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
  with a valid torsion tree. Unsupported flexible-receptor and multi-model
  variants must fail explicitly until their semantics are specified.
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
