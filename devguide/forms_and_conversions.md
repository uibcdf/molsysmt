# Forms and Conversions

This document defines the current adapter and conversion contract. Historical
adapter implementation notes are archived under `archive/assessments/`.

## Form adapter contract

Form adapters live under `molsysmt/form/`. Each adapter module defines:

- `form_name`;
- `form_type`;
- `form_info`;
- `attributes` and `has_attribute`;
- applicable topological, structural, or general piping targets;
- `_convert_to`, mapping supported target form names to converter callables or
  lazy converter-module names.

Detailed file layout and dependency rules are defined in
`form_adapter_implementation.md`.

An adapter that exposes `extract` must accept the dispatcher contract:
`item`, `atom_indices`, `structure_indices`, `copy_if_all`, and
`skip_digestion`. A form that cannot represent one of the requested axes must
raise a MolSysMT catalog error naming the form; it must not leak a Python
signature error or silently ignore a non-`all` index. Sequence-only forms may
map `atom_indices` to their positional residue tokens at this boundary and keep
a `group_indices` alias for converters that operate explicitly at group level.

Extraction must preserve system-level metadata while subsetting every field on
the selected axis. Capability declarations, presence checks, getters, and form
detection must agree on those fields: an adapter cannot advertise per-atom
attributes while its detector rejects an object containing them.

## Discovery and dependencies

Adapters are discovered lazily. Optional dependency ownership is defined by
`molsysmt/_depdigest.py`; adapters must not introduce their own competing
dependency registry. Soft dependencies are imported inside guarded functions,
never unconditionally at module import time.

### How a form is known without importing its adapter

Laziness here is a property that has to be built, not assumed. A form's name used to live
inside its module as `form_name`, so learning it meant importing the adapter -- and the
registry needs every name before it can answer anything. Any question about forms therefore
imported all 89 adapters and the third-party libraries behind them: measured at 3.9 s and
1123 modules for a single `get_form` call on a string.

Each `molsysmt/form/<adapter>/` now carries a **`form.json`** declaring its identity: the
form name, the category (`file`, `string` or `class`), the file extension, and -- for forms
holding an instance of a class -- the `(top-level module, class name)` an item of that form
has. `molsysmt/form/catalogue.py` reads all of them with one `os.scandir`: **2.35 ms, once
per process, importing nothing**.

This metadata optimization covers detection, not complete conversion startup.
Target validation still derives `_dict_forms_lowercase` from DepDigest's
`LazyRegistry.keys()`, and first module lookup also initializes that registry by
importing all eligible adapters. Converter submodules remain independently lazy.
The current cold-conversion proposal is uibcdf/molsysmt#382; its generic provider
capability is requested as uibcdf/depdigest#34. No indexed registry extension has
been adopted. See [the reproduction and adoption criteria](pending_proposals/first_conversion_triggers_full_form_registry_loading.md).

Three consequences worth knowing before changing anything here:

- **The class key is compared as strings.** Recognising an `openmm.Topology` never imports
  OpenMM; only acting on it does. This is what lets `get_form`, `is_item`, `is_file` and
  `is_string` answer in single-digit microseconds.
- **A form's category is readable in its name**, and `form_type` matches that prefix for all
  89 forms. The indexes rely on it, and
  `tests/basic/test_get_form_battery.py::test_form_type_matches_the_name_prefix` enforces it.
- **`form.json` is generated**, by `devtools/scripts/generate_form_declarations.py --write`,
  which imports the adapters once, offline. Nothing at runtime does, and a declaration that
  stops matching its module fails the suite.

Adapters accepting multiple class names declare `item_class_keys` as string
pairs in their module metadata, including the primary class. The declaration
generator retains these aliases. They must not exist only in a hand-edited
`form.json`, where regeneration would erase them. Runtime catalogue recognition
and regeneration are guarded by
`devtools/tests/test_generate_form_declarations.py`.

`molsysmt/basic/get_form.py` resolves from those indexes and imports **one** adapter to
confirm: the index says which detector is worth asking, the detector still decides. Only
when no index can decide does it sweep, and then only the category that could apply -- an
object that is not a string can never be a file or a string form.

`tests/basic/test_get_form_battery.py` is the safety net: it builds a real item of every
form it can reach, asserts each is detected as exactly itself, and its census fails when a
form declared in `molsysmt/form/` is neither exercised nor recorded as unreachable with a
reason. A new adapter cannot enter the catalogue without someone deciding how it is
detected.

## Conversion resolution

The current one-to-one resolver in `molsysmt/basic/convert.py` supports:

1. a direct edge from the source adapter to the target adapter; or
2. a two-edge route through `molsysmt.MolSys` when both edges exist.

It does **not** perform a general shortest-path search over the conversion graph.
Multiple-input conversions use registered shortcuts and attribute-based assembly
logic, with a MolSys route where explicitly supported.

Do not document or rely on arbitrary multi-hop conversion. A broader graph
resolver would be a new architectural feature requiring deterministic routing,
lossiness and cost policies, cycle detection, dependency-aware edge selection,
and dedicated tests.

## Converter registration

Register a converter only when it is callable for the documented source and
target contract. A placeholder that raises `NotImplementedMethodError` must not
be present in `_convert_to`, because registration advertises an executable edge.

Converter values **are** strings naming the converter module and function, not callables.
`molsysmt.form.load_converter` resolves them when an edge is actually traversed, and it is
the single place that does so. Writing the callable instead reintroduces the eager import
the string exists to avoid, and `tests/test_form_plugin_conventions.py` fails on it.

That laziness is only real if the adapter's `__init__` does not import the converter
anyway. It used to: 456 eager imports across 83 adapters, 44 of them already dead -- the
`_convert_to` value had been a lazy string for some time while the import line above it
still loaded the module. The laziness was written down but never happened.

### Two rules that are easy to get wrong

**Import a converter from its own submodule, never as an adapter attribute.**

```python
from molsysmt.form.file_pdb.to_molsysmt_MolSys import to_molsysmt_MolSys   # the function
from molsysmt.form.file_pdb import to_molsysmt_MolSys                      # ambiguous
```

Importing `<adapter>.to_x` binds the *submodule* as an attribute of the adapter package,
shadowing the function of the same name. The second form therefore yields the function or
the module depending on whether some earlier conversion happened to load it -- a bug that
appears far from its cause. Enforced by
`test_converters_are_imported_from_their_own_submodule`.

**Call the sibling in your own directory, not the identically named converter elsewhere.**

A converter in `<adapter>/to_<target>.py` receives an `item` of **its own** form. When it
needs an intermediate form it must call the sibling that converts *from this form*, not the
matching name in the target's adapter, which converts *from that form*:

```python
# in molsysmt_MolSys/to_openmm_System.py
from .to_openmm_Topology import to_openmm_Topology                          # correct
from molsysmt.form.openmm_Topology.to_openmm_Topology import to_openmm_Topology  # wrong here
```

The names are identical, so the mistake reads as correct. One instance made
`molsysmt.MolSys -> openmm.System` and `-> openmm.Simulation` unreachable for a long time,
failing with a bare `TypeError` from inside a form module.
`devtools/scripts/audit_converter_routing.py` searches for it statically; a hit is a
candidate, not a verdict, since compatible forms may share a converter deliberately.

Converters must:

- preserve documented semantics or explicitly document intrinsic loss;
- normalize native element IDs to strings;
- preserve coordinate, box, and time units through PyUnitWizard boundaries;
- accept the standard selection and structure-index arguments that apply to the
  represented data;
- import optional libraries lazily under DepDigest control.

MolSysMT canonical lengths are in nm and time is in ps. Angles derived from box
geometry follow the API's radians convention; converters must not generally
standardize angular data to degrees.

## Attribute declarations and piping

`attributes.py` records the adapter capability contract used by dispatch. A
declared attribute must be deliverable through the public `get()` path for every
documented element scope. Delivery may be direct or may use the adapter's
declared piping target.

This is intentionally a public-delivery definition, not merely a statement that
the source object's Python class stores a field directly. If native presence must
be distinguished from converted delivery in the future, add explicit metadata;
do not overload one boolean with two contradictory meanings.

For attributes available from more than one element scope, every corresponding
getter must exist or the pipe target must provide it. For example, coordinates
declared for both atoms and the system must work for both explicit atom requests
and the default system request.

Known delivery gaps are tracked under `pending_bugs/` and take precedence over
historical claims of complete adapter verification.

## Composite molecular systems and the structure axis

A molecular system may be given as several complementary items. Two consistency
contracts govern which item may deliver what, and neither depends on the order the
caller listed them in.

**Atom axis.** Complementary items must agree on `n_atoms`. They otherwise describe
different molecules, and `assess_molecular_system` raises
`StructuralInconsistencyError`. At most one item may provide a primary topology.

**Structure axis.** Items need *not* agree on `n_structures`: a topology file
holding a single reference conformation beside a trajectory file is an ordinary
composition, and `[pdb, xtc]` is the most common one in molecular dynamics. The
axis of the system is therefore defined, not required:

1. The **structure axis** is the largest structure count among the items carrying
   structural data. A form supplying no structures, such as PSF, neither defines
   nor constrains it.
2. A **structural** attribute may only be delivered by an item spanning that axis.
   Among the items that do span it, the ordinary tie-break applies: the last
   matching item wins.
3. An item below the axis holding zero or one structure is a **reference
   conformation**. Its structural series are not delivered, and the omission is
   reported with `StructuralAttributeOffAxisWarning`. Absence with a diagnostic is
   correct here; a series shorter than the system's own structure axis is not.
4. Two items each holding **more than one** structure, of different lengths, give
   no basis for choosing. That raises `StructuralInconsistencyError` naming
   `concatenate_structures`, which is the operation that does join structures on
   purpose.

The asymmetry between raising on the atom axis and reporting on the structure axis
is deliberate, not an exception: different atom counts mean different molecules,
while a reference conformation beside a trajectory is legitimate.

Implementations must not re-derive this rule locally. `_private/structure_axis.py`
owns it; `where_is_attribute` applies it to attribute resolution and `convert`
applies it to its own per-item attribute sets, which it resolves independently.
Operations built on those two, `Iterator` among them, inherit it and must not add a
second policy. The structure count of a single item must be read through
`item_n_structures`, never through the public `get`, which would re-enter attribute
resolution.

The precedence policy for **topological** attributes delivered by more than one
item is still positional and remains open: see open decision 1 of
`pending_proposals/attribute_centric_molecular_system_model.md`.

The user-facing explanation lives in the *Multiple items into one* section of
`docs/content/user/tools/basic/convert.ipynb`, which composes a PSF topology with a
DCD trajectory and states that the multi-structure item dictates the resulting
structure axis. The plan that produced it is
[`archive/resolved_proposals/docs/convert_tutorial_multi_form_structure_axis.md`](archive/resolved_proposals/docs/convert_tutorial_multi_form_structure_axis.md).

### Separate chemical and structural domains

A pair containing native `ChemicalStates` (or `ChemicalStatesDict`) and native
`Structures` converts to a topology-free `MolSys`, in either order. The caller
declares that both atom-index spaces correspond; matching cardinalities validate
the axes but do not independently verify molecular identity. Full source axes
must be compatible before any selection is applied.

The composition reuses native partial-domain assembly and `MolSys.extract`.
Unique atom indices retain their supplied order; nonconsecutive or repeated
structure indices retain theirs. Chemistry, bonds and structural series remap
together. All states and the reference index are preserved. Composition adds
no per-structure state assignment: a single state resolves implicitly, while
multiple states remain unassigned until the user declares an association.
Missing topology is preserved, rather than synthesizing an atom hierarchy.

The default result owns independent native domains. With `copy_if_all=False`
and both axes set to `'all'`, native inputs may be shared through a new MolSys
container. Dictionary chemistry is decoded to native storage. Selections always
produce independent remapped domains. No partial graph shortcut or competing
chemical store is introduced in scientific consumers. Ring tools use the same
public conversion with the full-domain sharing policy for a read-only context.

## Forms with partial source information

### Complementary partial native systems

Public conversion composes lists/tuples of complementary partial MolSys objects,
including materialized H5MSM 0.5 files, before selection. The input container is a
declaration of positional atom/frame correspondence; it is not authentication or
an atom-matching procedure. Classification inspects actual native domain presence
and H5MSM 0.5 axis metadata rather than assuming every file provides topology.
Readers still validate each file's own associations. Full-file conversion loads
arrays; metadata-only classification is not a streaming conversion contract.

Require one topology, chemistry and Structures provider, distinct analysis names
and compatible full axes before selection. Native extraction then owns sorted
topology atom indices, ordered/repeated frame selection and interaction remapping.
Preserve declared state/frame assignments; do not synthesize an assignment from
the chemical reference state. Topology is copied for its single-owner binding,
even if full-axis `copy_if_all=False` shares structural arrays. This bounded route
rejects mechanics rather than losing it. Complete-system and legacy-form routes
retain their existing rules. Guard:
`tests/basic/convert/mult_to_one/test_convert_complementary_h5msm_domains.py`.

A source containing coordinates but no topology must not invent semantic
topology. Likewise, a topology-only form must not advertise structures. Where a
format contains only partial labels, a converter may construct only the topology
that can be justified from those labels and must document the inferred fields.

File handlers should accept the documented path-like representation at public
boundaries. Internal reader objects must not be assumed to retain a recoverable
filename after construction unless their actual API guarantees it.

### Contractual reduced trajectory forms

Tier 1 trajectory forms can have a deliberately structural contract. In
particular, DCD and XTC do not supply a molecular topology. Standalone
conversion may create an index-only native topology so that structural arrays
remain usable, but it must leave semantic atom IDs and chemical attributes
missing rather than fabricate them.

The contractual read scope is:

- `file:gro` and `molsysmt.GROFileHandler`: atom and group labels present in the
  file, coordinates, optional velocities, and orthogonal or triclinic box;
- `file:dcd` and `mdtraj.DCDTrajectoryFile`: coordinate frames, optional box,
  frame selection, atom selection, and source-frame indices as structure IDs;
- `file:xtc` and `mdtraj.XTCTrajectoryFile`: coordinates, box, time, frame
  selection, atom selection, and the stored XTC step as structure ID.
- `file:h5` and `mdtraj.HDF5TrajectoryFile`: embedded MDTraj topology,
  coordinates, optional velocities, box, time, temperature, and available
  kinetic and potential energies. This interoperability format is distinct
  from MolSysMT's native H5MSM persistence contract.

MDTraj reader adapters preserve the caller's file cursor during public getters
and native conversion. DCD coordinates cross the MDTraj boundary in angstroms;
XTC coordinates cross it in nanometers. Both are normalized through
PyUnitWizard and delivered in MolSysMT's canonical units.

This reduced contract does not claim that conversion back to an open reader
object can materialize arbitrary subsets without creating a new file. Writing,
append behavior, and reader-object subset materialization require separate
conversion edges and tests before they become contractual.

### Contractual MDAnalysis forms

`MDAnalysis.Universe`, `MDAnalysis.AtomGroup`, and `MDAnalysis.Topology` are
Tier 1 interoperability forms within an explicit, target-aware scope:

- `MDAnalysis.Topology` represents topology only. Atom subsets are
  materialized without structures; a structure request is rejected.
- `MDAnalysis.Universe` delivers its available topology together with
  coordinates, optional velocities, time, and orthogonal or triclinic box
  geometry. Random frame access and conversion restore the caller's active
  frame.
- `MDAnalysis.AtomGroup` is treated as a real subset. Converting or extracting
  it must not silently reintroduce atoms from its parent Universe, and further
  atom selections are relative to the AtomGroup.
- Native `atom_id`, `group_id`, and `chain_id` values retain source identity as
  strings; duplicate source IDs are not renumbered merely to make them unique.
- MDAnalysis residues and segments map to MolSysMT groups and chains. Components,
  molecules, and entities are rebuilt from the information available after
  import; they are not claimed to be native MDAnalysis hierarchy levels.
- Available covalent bonds and formal charges enter the native chemical-state
  seam. Opaque MDAnalysis bond-type objects are reported as an adapter
  limitation rather than guessed into a canonical chemical type.

Self-conversion to a Universe or AtomGroup materializes the requested atom and
frame subset in memory. MDAnalysis's `MemoryReader` represents a uniform time
axis; a selected irregular time axis is therefore rejected with an actionable
error instead of being silently regularized. Conversion to `molsysmt.MolSys`
retains irregular time arrays.

This contract does not promise preservation of arbitrary user-added MDAnalysis
topology attributes, transformations, auxiliary readers, analysis caches, or
custom trajectory-reader state. Those features require separate evidence before
they can be advertised as contractual.

### Read-only chemical coverage assessment

`physchem.get_chemical_readiness` is an experimental form-agnostic stored-field
audit for one state and at most one structure. It accepts incomplete native
domains rather than invoking the complete-graph guard used for CIP and rings.
The versioned detached dictionary reports source indices, per-field coverage,
unsupported encodings, limited integrity conflicts and declared edge evidence.
Selections include incident bonds and report their crossing boundary. Native
state resolution remains authoritative; an ambiguous reference or absent
structure-state association leaves chemistry unassessed rather than selecting
the first state.

The audit creates no chemical store and performs no repair or perception.
Stored availability, connectivity completeness and edge evidence do not certify
valence, protonation, aromaticity, stereogenicity or docking readiness. Unknown
property origins stay unassessed. Explicit H atoms and stored virtual/implicit
H counts are separate observations. Coordinate finiteness uses explicit nm
conversion through PyUnitWizard, not a conformer-quality or periodicity test.
H5MSM 0.5 numeric selections reuse the bounded form iterator and read only the
selected coordinate frame/atom rows; independently combined layers need declared
identity atom-axis links. Rich string selection retains existing public
selection behavior. Native inspection adds no optional engine or attribution
boundary. See the [user contract](../docs/content/user/tools/physchem/get_chemical_readiness.md)
and `tests/physchem/test_get_chemical_readiness.py`.

### Exact residue template coverage

`build.get_residue_chemical_coverage` adds a read-only group report to the shared
stored-field audit. Numeric selections are source group indices; rich selections
resolve atoms and inspect their whole groups. Required atom-to-group membership
is validated without synthesizing hierarchy for coordinate-only or ungrouped
sources. Each selected group remains represented, including unsupported cofactors.

Exact amino-acid database names and curated MSE/SEP/TPO/MLY heavy templates define
the supported comparison scope. Sequence aliases never justify parent templates.
Unique atom names provide correspondence. Candidate H inventories are retained
without choosing protonation from a missing-H score. Missing terminal OXT, chemical
valence, environmental protonation, inter-group chemistry and repair placement
remain unassessed. Curated modified templates support declared order comparison;
legacy amino-acid variants do not provide reference orders. Unknown source edges
and orders cannot become covalent relationships or fabricated values.

Template provenance records packaged hashes and available upstream evidence;
property origins remain unknown unless declared. The nested chemical-readiness
report preserves its state, frame, units and bounded H5MSM access contract.
Template resources and bond-field lookups are reused within one assessment;
connectivity compares each group's partitioned records without repeatedly scanning
the whole selected bond table. No new optional provider or attribution boundary
is introduced. See the [user contract](../docs/content/user/tools/build/get_residue_chemical_coverage.md)
and `tests/build/test_get_residue_chemical_coverage.py`.

### Explicit chemical-template preparation

The experimental `physchem.assess_chemical_template` and
`physchem.apply_chemical_template` accept supported forms through the existing
chemical-domain conversion routes. Assessment reads no coordinates; native and
H5MSM 0.5 inputs reuse the shared chemistry reader. Explicit state selection is
independent for source and template. The exhaustive `(n_selected_atoms, 2)` map
contains full-input template indices then source indices, including explicit H.

Without a context map, the scope is one closed selected component, or fragments
of that component when explicitly completing its graph. The default
`connectivity_policy='require_same_graph'` requires the same stored covalent
edges and complete declared template assignments. Explicit
`complete_from_template` adds missing mapped covalent edges to an incomplete
source; unexpected edges and known conflicts still fail. A disjoint explicit
`context_atom_correspondence` allows a selection with external neighbors,
including a polymer group. It must cover all required neighbors and incident
stereo references; context mode supports only the same-graph policy.

Only absent supported assignments are filled. Context atoms and outside-only
bonds remain unchanged; without context, boundary relationships remain unassessed.
Aromatic/stereo encodings requiring normalization remain unassessed. No atom or
coordinate is generated, no protonation state chosen, and no template authenticated.
Whole-input connectivity completeness is justified by the exhaustive declared
template map, not by conversion success. Proper subsets and context applications
preserve global completeness and retain their scoped evidence in the report.

Application creates an independent MolSys, retaining stable atom identity,
structures/units/box and structure-state associations. Only the selected state is
replaced. Chemical changes conservatively invalidate named interactions on the
returned copy through its native lifecycle; an identical repeat preserves them.
Failed preflight changes neither input and carries a detached assessment in the
catalog-backed error. Chemical-state assignments remain in `ChemicalStates`.

The detached `molsysmt.chemical_template@1` report retains indexed assignments,
source/template states, correspondence, declared identity/version/checksum,
hydrogen policy, original producer version and elementary-charge units. Existing
edge evidence remains unchanged. Successful application also stores an independent
report envelope in the selected `ChemicalStates` preparation history. H5MSM 0.5
and `ChemicalStatesDict` preserve that history, including unchanged applications.
Extraction and later edits retain the original operation indices and producer;
historical indices do not describe the current atom/bond table. Successful
application credits executed MolSysMT through optional Ackredit; inspection and
failed application do not. Absence/provider failure cannot alter the science.

See the [public contract](../docs/content/user/tools/physchem/chemical_templates.md)
and `tests/physchem/test_chemical_template.py`. Declared aromatic-order normalization
and fixed-state H placement are separate implemented tools; neither runs implicitly
during template application. Broader chemistry and environment-dependent refinement
remain outside the frozen profile.

### Hierarchy selection delivery

After resolving atom selections, `basic.select` projects group/component/chain/
molecule/entity indices through public `basic.get`, including empty and nested
selections. A declared attribute can be delivered through conversion rather than
a direct form getter. Projection must honor that route instead of assuming a
`get_X_index_from_atom` callable exists. This reuses the existing source-axis
contract without inferring hierarchy. See `tests/basic/select/test_hierarchy_fallback.py`.

### Contractual chemical interoperability forms

`rdkit.Mol`, `openff.Molecule`, `openff.Topology`, `parmed.Structure`,
`string:smiles`, `file:smi`, `file:mol2`, and `file:psf` are Tier 1 within target-aware
chemical contracts:

- RDKit preserves supported native graph fields, atom and bond stereo,
  aromaticity, isotope, formal charge, conformers, namespaced identity, and
  complete supported partial-charge properties.
- OpenFF Molecule preserves conformers, complete partial charges, rich atom and
  bond chemistry, and E/Z reference atoms. OpenFF Topology combines molecule
  graphs and complete charges but does not invent a synchronized trajectory
  from independent per-molecule conformers.
- ParmEd Structure preserves coordinate frames, unit cells, B factors, source
  atom types, chemical bond fields, formal charge, and mechanical partial
  charge. Per-atom mechanics follow atom extraction.
- SMILES strings and SMI files are reduced graph forms without partial charges
  or structures. Invalid SMI records fail with their source line, and multiple
  records become disconnected components in one requested `rdkit.Mol` target.
- MOL2 uses ParmEd as an encapsulated parser while MolSysMT validates Tripos
  source tokens. It preserves serials, names, Tripos atom types, groups,
  coordinates, optional box, partial charges, bond IDs, aromatic `ar`, and
  fractional amide `am` order. Unsupported bond tokens and multi-record files
  fail explicitly.
- PSF uses OpenMM as its parser and preserves source string IDs, chemical atom
  types inferred by the parser, CHARMM force-field atom types, partial charges,
  hierarchy, and complete explicit covalent connectivity. Ordinary PSF
  connectivity does not encode chemical bond order, so no order is invented.
  PSF itself has no structures; coordinates supplied separately are composition
  input rather than attributes read from the file.

These contracts do not imply arbitrary property-block preservation or a
multi-record SDF/MOL2 model. Those require a separate post-1.0 schema decision.

### Experimental native SDF interoperability

`file:sdf` is Tier 3 and reads/writes one V2000 or V3000 connection table with
no RDKit runtime dependency. Source atom and bond serials become string IDs;
all explicitly drawn hydrogens remain atoms. Coordinates are interpreted as
angstroms and converted through PyUnitWizard into native nanometers. Writing
extracts values explicitly in angstroms even under a different application unit
policy. Reading records explicit charge, isotope, supported radical counts,
ordinary covalent orders and aromatic type 4; it does not assign implicit
hydrogens, sanitize valence, perceive aromaticity from Kekule orders or assign
CIP labels from coordinates by default. An explicit keyword-only
`stereo_engine='rdkit'` opts into the optional scientific provider for supported
tetrahedral and double-bond stereo; the native parser still validates the graph
and retains the atom axis. `physchem.get_cip_stereochemistry` owns accurate
Hanson 2018 CIP analysis, including pseudoasymmetry. It is form-agnostic and
read-only, with full-graph ranking before output selection.

V3000 coordination type 9 maps to `bond_type='dative'`, with the first source
endpoint as donor and the second as acceptor. This is the adapter's explicit
orientation convention, consistent with RDKit; it is not chemical donor
perception. Native dative bonds default to `joins_components=False`. No covalent
order is invented for type 9. Writing requires V3000 and both roles, then orders
the serialized endpoints by those roles rather than by native sorted storage.
V2000 type 9 is rejected as an unsupported extension. The reader accepts the
COORD/DATIVE display options, but native conversion reports losing `DISP` style;
identity copies retain the original bytes. Type 10 hydrogen relationships and
multi-endpoint coordination remain unsupported.

The default subset rejects active stereo flags. Both routes reject queries, valence overrides,
reaction maps, Sgroups, singlet spin, unsupported bond types and unknown CTAB
extensions. The chemical state owns explicit chemistry; the format reader does
not create an alternative chemical store. Unsupported data never becomes a
fabricated default. The optional provider supports 2D wedges and supported 3D
representations, stores R/S or r/s in ChemicalStates, and preserves cis/trans
with source reference atoms on double bonds. Absolute E/Z is a separate CIP
analysis output, not a claim about the reference pair. Unsupported enhanced,
non-tetrahedral and uninterpretable parity-only stereo remain errors. The writer
verifies serialized configurations before touching the destination. A verified
stereo route is accounted for in `convert(..., return_report=True)`;
`get_conversion_report` has no converter-option arguments and describes the
ordinary default route. These bounded limits keep uibcdf/molsysmt#215 open
pending the broader representative-source validation.
Documented inactive zero values of V3000 atom/bond flags are accepted, without
creating query, stereo or hydrogen assignments. Unknown and repeated fields
still fail, even with zero values.

An SDF writer needs a complete graph, explicit formal-charge and radical-count
vectors, one chemical state and exactly one selected structure. It validates
the full payload before opening the destination. `ctfile_version='V3000'`
removes the V2000 limit of 999 atoms or bonds and fixed coordinate widths.
Native atom aromaticity must agree with the explicit aromatic bond types that
the format can carry; unencodable or contradictory assignments fail explicitly.
Atom selections follow native MolSys extraction order (ascending source atom
indices when topology is present); bonds and coordinates follow that same map.
Writing assigns sequential one-based serials and cannot preserve arbitrary
native IDs/names, hierarchy, interactions, mechanics or extra structural fields.
Reports identify non-default component-joining assignments and separate numeric
dative orders that cannot survive SDF serialization; strict mode rejects them.

SD property blocks have no general native schema yet. Conversion into native
objects rejects them unless `discard_properties=True` explicitly authorizes
their loss. `return_report=True` identifies this loss; `strict=True` rejects it
even when discarding was requested. Full-axis SDF identity conversion and
`copy(..., output_filename=...)` preserve the original bytes and properties.
For literal `selection='all'` and `structure_indices='all'`, the identity route
checks only the single-record envelope (header/count fields, `M  END`, `$$$$`),
not CTAB chemistry or property grammar. Source valence overrides, legacy
versionless records and other unsupported chemical encodings can therefore be
copied unchanged without an optional provider. Its exhaustive `exact` report
certifies byte preservation, not chemical validity or native readability.
Malformed envelopes fail before destination mutation. Explicit index lists
and native/attribute routes remain subject to native interpretation.
Subset file output requires an explicit path and the native supported subset.
SDF reports remain non-exhaustive for cross-form conversion. Multi-record files
and unselected multi-frame output fail instead of taking the first entry.

Contract and optional differential evidence:
`tests/form/file_sdf/test_native_contract.py`, `test_coordination.py` and
`test_reference_corpus.py` in that directory. The committed synthetic corpus
tests 17 molecular graphs in 46 supported source encodings without a runtime
toolkit; three valence-override records exercise required rejection. Generation
instructions and producer version are stored with the corpus. This is bounded
compatibility evidence rather than chemical perception or stereo coverage.
BIOVIA's
[CTFile Formats 2020](https://discover.3ds.com/sites/default/files/2020-08/biovia_ctfileformats_2020.pdf)
defines the syntax and precedence. RDKit's reader is a reference implementation,
not an additional required dependency or a claim of full compatibility.

## Validation obligations

For every supported conversion edge, tests should cover:

- direct execution through `msm.convert`;
- representative selection and structure slicing;
- ID, shape, dtype, and unit invariants;
- lossless round-trip parity where the formats can represent equivalent data;
- explicit expectations for intentionally lossy formats;
- missing optional dependency behavior;
- lazy-import behavior for soft dependencies.

The adapter linter checks structural conformance. It is not evidence of semantic
parity or scientific correctness.

## Native AutoDock4 PDBQT subset

The experimental `file:pdbqt` and explicit `string:pdbqt_text` forms support a
rigid receptor and a single balanced ligand torsion tree. Prefix strings with
`pdbqt_text:`. No third-party parser or preparation package is required.
The adapters retain every source hydrogen, explicit mechanical labels/charges,
stable atom names/IDs and supported hierarchy/structural fields. Length and
area boundaries explicitly use angstrom and angstrom squared through PyUnitWizard.
AutoDock labels decode to chemical element `atom_type`; they remain separate
`atom_ff_type` data. Formal charges and aromaticity are not inferred.

Only BRANCH edges are declared covalent evidence, with unknown order.
Connectivity is always partial. Native domains have no general torsion store;
public format `get_torsion_tree` returns a detached typed/indexed dictionary
(`molsysmt.pdbqt-torsion-tree@1`), separate from native molecular data. Full
MolSys conversion requires explicit `discard_torsion_tree=True` for ROOT inputs.
Reduced domains project their own supported fields and omit format metadata.
General attribute queries use reduced-domain routes and direct mechanics getters.

Native writing requires one selected structure, supported explicit charges and
labels, canonical positive integer string IDs within field width, and explicit
`typing_scheme='autodock4'`. A tree writes ligand layout; None requests rigid
layout. Validate exact selected atom-ID correspondence, a rooted partition and
branch roles before writing. Complete native graphs additionally validate cuts
and fragments through the public `topology.get_rigid_fragments` tool. Tree
traversal may reorder atom lines while serial IDs preserve correspondence.
Serialization uses the format's fixed precision; preparation and hydrogen
merging never occur implicitly. All validation precedes destination mutation.

File/string identity bridges preserve the original payload and support strict
mode. Native conversions report known tree/remark/kind losses; native writers
report loss of full chemistry and other unsupported domains. Reports remain
conservative, not exhaustive for native output. Explicitly authorizing tree
omission does not waive strict loss checks. Rigid atom subsets are supported;
tree projection requires explicit remapping. Extended dialects, flexible
receptors and multi-model ensembles remain separate proposals. These adapters do
not implicitly assign AutoDock labels, merge hydrogen atoms or classify rotatable
bonds. Explicit general tools provide named charge/type assignment and graph-based
torsion candidates; hydrogen merging/maps remain separately tracked in #223.
MolecularMechanics stays excluded from H5MSM 0.5: its public MolSys writer rejects
nonempty mechanics before creating a file. Labels/charges are not silently omitted.

User contract: [prepared PDBQT recipe](../docs/content/user/cookbook/native_pdbqt.md).
Implementation and acceptance debt: uibcdf/molsysmt#214.

Mixed public queries preserve requested mechanical fields alongside topology
and structures. Reduced-domain pipes cover their own fields; the dispatcher
queries other requested domains on the original source, retaining the same
selected source atom-index order. It does not silently omit those result keys
or force charge/type data into Topology. Guard:
`tests/basic/get/test_mixed_mechanical_pipes.py`; resolved defect:
uibcdf/molsysmt#301.
