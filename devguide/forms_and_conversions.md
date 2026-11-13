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

The form registry uses DepDigest's `DeclaredRegistry` with
`load_policy="adapter"`, requiring published DepDigest >=0.15.1. Declarations
come from the host catalogue. Enumerating names and normalizing known target
names does not import adapters. A module lookup loads the requested adapter;
its own imports and the requested conversion can load further required modules.
Converter submodules remain independently lazy. Iterating registry values or
inspecting every adapter's callable capabilities intentionally loads adapters.

DepDigest owns module/failure caches, dependency visibility, diagnostics,
refresh and explicit discovery. The catalogue delegates module lookup to that
registry and keeps no competing implementation cache. Real import failures
propagate with their original cause; retry is explicit. Current configuration
can hide soft capabilities. All-capability inspection may expose an importable
adapter without its optional engine, but scientific execution still requires
the guarded engine. Case normalization and tolerated native target spellings
are resolved before asking whether a target is a molecular item.

Manual implementations, overrides and removals are respected by catalogue
lookup and dispatch. Uncatalogued identities are considered after built-in
detectors fail to match. Host admission still requires an explicit support tier;
registering an adapter does not certify its scientific criteria or conversions.
Undeclared filesystem plugins require explicit provider discovery.

Concurrent value lookups on the shared registry serialize through initialization
and use the same cached implementation or failure. Mutation, discovery,
retry/refresh and configuration changes require external exclusive coordination.
An initializer must not wait for another thread needing that registry; arbitrary
cycles between registries, imports and threads are outside the provider guarantee.
This loader contract does not make arbitrary molecular edits thread-safe.

The owning provider contracts are uibcdf/depdigest#34, #36 and #39. Consumer
adoption and bounded measurements are recorded under
[uibcdf/molsysmt#382](pending_proposals/first_conversion_triggers_full_form_registry_loading.md).

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

Complementary inputs regenerate positional atom/structure indices. These are not
scientific series copied from an off-axis reference and do not constitute lost
observations. Real off-axis time, velocities or other structural observables
still warn when no on-axis input can supply them. Incompatible trajectory counts
remain errors; this distinction changes no coordinate or atom correspondence.

### CIF primary observations

The shared mmCIF DataContainer converter supplies primary dimensionless occupancy
on the same `(n_structures, n_atoms)` axes as native coordinates. CIF/BinaryCIF
file adapters, including compressed forms, declare this attribute and route
queries through native Structures. Unknown `?`/`.` cells remain NaN; an entirely
unavailable primary field remains None. Zero is a measured value, not missing.
No occupancy is inferred from geometry or borrowed from another representation.

Alternate-site reduction is model-local. The import policy chooses maximum
known occupancy, then A among tied maxima, then source order. If all values
are unknown, it retains the first variant with unknown occupancy. All raw
variants remain available for explicit resolution; the import rule is distinct
from the half-occupancy tie rule of `build.solve_atoms_with_alternate_location`.
Coordinates, primary occupancy, B factors and model indices share one canonical
atom map. Group occurrences are model-local before extraction, so per-group bond
declarations apply independently. Generated global component-name ordinals do
not prevent matching models from forming one ensemble; inventory and component
membership comparisons still apply.

Conversion retains native sorted atom-extraction order; direct attribute queries
retain requested atom order/repetitions. Structure indices retain order and
repetitions in both. Native Topology extraction requires a flat unique in-range
atom subset, including an explicit full-length list; list length alone does not
establish complete coverage. Invalid lists raise ArgumentError before copying
or returning a source alias. `all` and a valid explicit complete set retain the
method's `copy_if_all` contract; use `permute_atoms` for an explicit atom order.

For `mdtraj.Topology`, explicit atom extraction retains source atom order and
the form's existing coalescing of repeated positions. Retained parents alone
are constructed, so local atom/group/chain indices are dense. Chain labels,
group sequence labels including zero, segment labels, serials, known/unknown
formal charges and bond type/order survive selection. The source is unchanged;
no chemical interpretation or coordinate calculation occurs. This external form
has no structure axis. Unrestricted extraction retains its copy/alias policy.
H5MSM stores the primary array and sparse alternatives
without inventing missing values. The owning regression is
`tests/form/mmcif_PdbxContainers_DataContainer/test_primary_occupancy.py`.

### Deposited CIF model labels

The shared DataContainer reader and structural getter retain exact
atom_site.pdbx_PDB_model_num spelling as string structure_id values, including
leading zeros. The existing structure axis remains ascending numeric model
order, independently of source row encounter order. Coordinates and labels
receive the same nonconsecutive/repeated structure-index selections. CIF,
BinaryCIF and their gzip routes share this interpretation; native extraction
and H5MSM retain the selected labels without replacing them by indices.

A wholly absent/unknown model column supplies no IDs. Its atom rows describe one
unlabeled structure; model boundaries are not guessed from repeated atom names.
Partly missing labels, noninteger/out-of-range model numbers and conflicting
spellings for one numeric model fail with FormatError before native output.
Different model inventories retain the established warning/separate-system
result, with each returned model carrying its own deposited ID. A label-only
getter does not certify inventory compatibility or infer a chemical state.
The private adapter helper shares only this declared model-axis interpretation;
ArgDigest public boundaries, units and connectivity policy remain unchanged.

Guard: `tests/form/mmcif_PdbxContainers_DataContainer/test_structure_ids.py`.

### Biological assembly generators

The mmCIF DataContainer converter, including CIF/BinaryCIF routes through it,
accumulates every `pdbx_struct_assembly_gen` row under its own assembly ID.
Source row order, expanded operation order, duplicates and ordered chain sets
are retained. Equal chain sets share a flat `chain_indices` sequence; different
sets use one sequence per operation. Native storage and H5MSM preserve those
scopes. `build.make_bioassembly` still refuses heterogeneous scopes explicitly;
storage support is not construction support. Translations retain length units.

The reader supports individual/list/range factors and products of two factors
with the existing right-to-left composition. Empty factors and products with
more than two factors fail conversion with a catalog `FormatError`; they cannot
silently produce an empty or partial assembly. This correction changes no public
signature or native schema. The regression module is
`tests/form/mmcif_PdbxContainers_DataContainer/test_bioassembly_generators.py`.

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

## Molecular-system verification failures

Form recognition and consistency evidence distinguish unsupported inputs from
operations whose verification could not finish. A detector returning False may
lead to NotSupportedFormError; ordinary public argument validation maps genuinely
unsupported input to ArgumentError with its original reason/cause. Incompatible
complementary atom axes still raise StructuralInconsistencyError.

An adapter initialization failure, unexpected detector error or failed domain/count
probe is unverified evidence. get_form and processing boundaries report the
existing public MolecularSystemVerificationError and retain the complete Python
__cause__ chain. The internal assessment uses kind=undetermined when form
recognition fails operationally, validation=unverified, only successfully recognized
form identities and the original exception reference. It does not declare the
source invalid or certify chemistry. The boolean is_a_molecular_system predicate
returns False whenever one valid consistent system has not been proved.

The private host _FormRegistry delegates declarations, visibility, loading,
failure caching, overrides, retry and concurrency to DepDigest. It translates a
known-entry KeyError with an original load cause into the domain verification
error; absent/hidden keys retain ordinary mapping behavior. Known failures remain
cached until explicit provider retry/refresh or a new process. There is no implicit
parser fallback, automatic retry or competing cache. The supported provider floor
already retains the cause; no dependency upgrade or provider patch is needed.

The item digester propagates operational errors and retains unsupported-input
causes. Allowed empty append targets avoid a detector probe; recognized cross-form
append targets retain their existing contract. Normal molecular-system digestion
does not duplicate the consistency probe. Public signatures, skip_digestion,
dependency visibility, application diagnostics and unit policy are unchanged.

Guard: `tests/_private/test_adapter_load_diagnostics.py`; existing registry,
classification and complementary-domain controls also remain applicable.

## Composite molecular systems and the structure axis

A molecular system may be given as several complementary items. Two consistency
contracts govern which item may deliver what, and neither depends on the order the
caller listed them in.

**Atom axis.** Complementary items must agree on `n_atoms`. They otherwise describe
different molecules. Assessment records that invalid evidence, and public
argument validation raises `StructuralInconsistencyError`. At most one item may
provide a primary topology.

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

### Resident native inventory reads

Native Topology and MolSys count/summary queries read declared molecule and
entity rows, including unused rows and atom-free inventories. Unknown parent
links remain unknown; reading cannot rebuild these tables or discard their
labels. Scalar parent queries preserve `None`, order and repeated positions.
Explicit reconstruction and foreign/dictionary conversion finalization retain
their own contracts; the resident-read guarantee is not a direct serialized
count shortcut. See [the native query contract](native_queries.md).

### Whole H5MSM stable inventory

A default whole conversion from one H5MSM 0.5 path to `molsysmt.Topology`
reads only its stored topology through the existing selected-layer reader.
It does not load coordinates, chemical states or interactions and does not infer
cross-layer correspondence. Static tables remain resident. Explicit selection,
structure scopes, reports, naming overrides, converter kwargs and composite
sources retain their existing routes. Requested-layer validation is distinct
from complete-file validation. The exact admission and guard are maintained in
[the scalability contract](SCALABILITY.md#whole-h5msm-topology-conversion).

### Complementary partial native systems

Public conversion composes lists/tuples of complementary partial MolSys objects,
including materialized H5MSM 0.5 or experimental 0.6 files, before selection. The input container is a
declaration of positional atom/structure correspondence; it is not authentication or
an atom-matching procedure. Classification inspects actual native domain presence
and modular H5MSM axis metadata rather than assuming every file provides topology.
Readers still validate each file's own associations. Full-file conversion loads
arrays; metadata-only classification is not a streaming conversion contract.

Require one topology, chemistry and Structures provider, distinct analysis names
and compatible full axes before selection. Native extraction then owns sorted
topology atom indices, ordered/repeated structure selection and interaction remapping.
Preserve declared state/structure assignments; do not synthesize an assignment from
the chemical reference state. Topology is copied for its single-owner binding,
even if full-axis `copy_if_all=False` shares structural arrays. This bounded route
accepts one stored mechanical provider with matching atom rows, preserving
original reports without recalculation. Repeated nonempty providers refuse. Complete-system and legacy-form routes
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

The MDTraj HDF5 structural iterator differs from its eager getters: it reads
one selected structure per provider call, decodes stored units through MDTraj,
and applies the active PyUnitWizard output policy. Missing optional series are
None. Coordinates/velocities preserve query atom order and repetitions;
structure_index retains the requested source positions. This positional axis
is not an authenticated structure ID. Its reusable result mapping, explicit
supported fields and cursor/handle ownership are described in
[scalability](SCALABILITY.md#mdtraj-hdf5-structure-iteration). Guard:
`tests/form/mdtraj_HDF5TrajectoryFile/test_iterator_contract.py`.

This reduced contract does not claim that conversion back to an open reader
object can materialize arbitrary subsets without creating a new file. Writing,
append behavior, and reader-object subset materialization require separate
conversion edges and tests before they become contractual.

### Group-name and analysis fidelity

Stored group-name declarations are stable-inventory metadata, separate from
labels and ChemicalStates. Native inventory, supported typed dictionaries and
H5MSM carry their versioned registry and group map. Conversion preflight reports
selected declarations that a target cannot retain, including prospective
`from_naming_scheme` supplied by the caller. Strict conversion rejects detected
loss before target creation; ordinary conversion keeps its permissive policy.
Unknown context is never inferred from a format or a native class.

Direct PDB/GRO native readers accept the explicit source convention before
initial group classification and native connectivity inference. PDB file/text/
handler MolSys and Topology routes share that boundary. The generic dispatcher
uses interpreted native inventory before a semantic selection; raw output
indices still retain the reader's established selection route. It never applies
an output atom subset before interpreting those source axes. Existing native
metadata declarations do not implicitly reclassify stored types. PDB history
retains source_naming_scheme as an original operation input. Unsupported external
OpenMM source interpretations use the shared preparation refusal, with the
existing explicit-raise versus optional-warning/history policy; no native
fallback or default convention is introduced. Pure Topology projections retain
stable inventory and naming metadata, not ChemicalStates graphs or histories.
The context-aware name-only projection requests inventory without implicit bond
reconstruction when that reader exposes a connectivity policy; explicit engine/
inference requests retain their normal semantics.

The selected native PDB profile composes the general
`build.infer_covalent_bonds` policy on source structure index 0, before output
extraction. Its `excluded_inference_policies` explicitly retains stored disulfide
and metal-coordination edges without adding proximity-derived ones. Groups
without an exact template have no geometric fallback. The typed selected source
group indices scope that exclusion; other groups' coverage and observed-H
limitations remain in their owning candidate reports. Stored edges keep their
evidence and are not chemically recertified. Missing/ambiguous/symmetry-specific
declarations are not replaced by nearby observed sites. Conflicting declared
sulfur partners remain stored and flagged in the original reader history.
The separate public disulfide detector produces geometric candidates, including
competing partners, without applying bonds. This bounded native policy does not
promise general ligand chemistry, water reconstruction, metal coordination or
oxidation-state assignment. The standalone inference tool retains all source
structures and its independently selected state/structure scope.

Named analyses omitted by a target are reported in the `interactions` scope,
including empty named results. Adding missing naming context uses the existing
invalidation policy on the independent molecular output; the report exposes
lost selected evaluated coverage, including evaluated-empty structures. Matching
context, unevaluated coverage and unselected structures do not invent this
invalidation loss. Source snapshots remain unchanged. Report scope does not
certify scientific methods, schema validity, dependencies or writer availability.
See [the owning #549 record](archive/resolved_bugs/reconcile_legacy_amino_acid_name_mappings_with_native_protonation_labels.md)
and the public conversion/preflight documentation for boundaries and evidence.

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

### Explicit CCD references and stable label correspondence

`physchem.get_chemical_template` constructs a coordinate-free native reference
from caller CCD bytes, a selected local file/catalogue/cache directory, or explicit
individual `source='rcsb'` acquisition. An offline miss never becomes a network
request. The streaming selector retains the selected decompressed block and
hashes the complete original resource. It respects CIF text fields, compression,
duplicate blocks and source replacement. Physical-line and retained-definition
buffers have separate estimated quarter-memory budgets; these do not bound the
parser, native object or process RSS.

The named `ccd_tables` projection requires no RDKit and retains unknown radical,
conjugation and interpretation scope. The default `ccd_canonical_descriptor`
selects an exact descriptor program, uses optional RDKit and reuses accurate CIP
primitives. Assignment requires graph/charge/aromatic/H compatibility and agreement
across every admissible mapping. Missing descriptors, incomplete declarations,
unsupported models and conflicts remain explicit. Truncated enumeration cannot
certify consensus. Aromatic triples/quadruples are outside this interpretation
profile, without a general claim that the source chemistry is impossible.
CCD case-insensitive order/aromatic/stereo codes are normalized according to the
dictionary; original source bytes retain the exact declarations.

Ordinary indexed H can be projected to stored heavy-atom counts, retaining both
atom/bond source maps. Lossy isotopic, charged, unknown-charge, isolated or
multiply linked H projections are refused; explicit atoms remain available.
Formal charges use the existing integer elementary-charge schema. The result
retains exact source bytes, revision/digests, descriptor choices/disagreements,
producer software and detached bibliography in the existing ChemicalStates
preparation-history envelope. H5MSM/typed dictionaries preserve original operation
axes; historical maps do not certify current indices after editing/extraction.
No ideal/model coordinates, protonation prediction or observed-system edits enter
construction. Optional attribution credits only executed software and consulted
definitions; descriptor program metadata is not runtime software credit.

`topology.get_atom_name_correspondence` reads stable names/elements through public
form-agnostic queries. It requires exact unique names and compatible elements in
explicit scopes, returning query/reference full source-index pairs. Repeated or
invalid indices and absent/ambiguous/incompatible names are refused; empty pairs
retain shape `(0, 2)` and int64 dtype. This is a label map, not graph matching or
chemical identity. Template application still performs its complete chemical
assessment. No chemical-state or coordinate context is required for this stable
inventory operation.

Both surfaces remain experimental. Their source contracts and deposited MK1/BTN
application controls do not establish bound-state correctness, docking acceptance,
an installed consumer pair or a new addon facade. See the
[reference tutorial](../docs/content/user/tools/physchem/chemical_templates.md),
[label contract](../docs/content/user/tools/topology/get_atom_name_correspondence.md)
and `tests/physchem/test_ccd_template_application.py`.

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

## OpenMM coordinate projections and runtime snapshots

`openmm.PDBFile` exposes all loaded coordinate models on the structure axis.
Direct coordinate queries retain requested atom/model order and repetitions;
the count query counts those selected entries. Its one topology box is repeated
for the selected models, not interpreted as independently measured model boxes.
Coordinates and boxes carry quantities and follow standard length policy.

Same-form PDB extraction retains source-sorted unique atoms and aligns every
selected model with that inventory. Model order/repetitions survive. Full
copies are independent; `copy_if_all=False` permits unrestricted source reuse.
Projection updates the reader's known position stores and numpy cache together
without PDB serialization, coordinate rounding or new bond inference. This
bounded OpenMM adapter coupling requires receiving when provider layout changes.
It does not deep-copy unselected coordinate models. At least one model is
required for a PDBFile projection; direct empty structure queries remain shaped.

Modeller extraction also uses source-sorted unique atoms, a separate topology
and two-dimensional positions for its single pose. It admits only `all` or `[0]`
on that structure axis. Copies do not share topology or coordinate data. A
PDBFile-to-Modeller conversion deliberately takes the first selected model
(model 0 by default), not a trajectory. PDB-to-MDTraj trajectory conversion
instead retains all requested models and the box, with MDTraj's nm/float32
coordinate representation. Native MolSys projections deduplicate inventory
and coordinates together; native Structures-only queries retain positional
request order. These projections do not establish heterogeneous-model identity.

An OpenMM Context is live and mutable; public coordinate assignment accepts
the shared single-structure selector and converts lengths explicitly to engine
nm. A captured State has no coordinate mutator: both public and direct setter
hooks refuse with `NotImplementedMethodError` and preserve the snapshot. Use a
Context or native Structures for editing. Neither coordinate access nor a
captured iterator supplies independent live-runtime copying; #592 retains that
separate contract. Source topology/chemistry transport still follows the native
domain rules above, without preparation, minimization or force-field inference.

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
labels, by default canonical positive integer string IDs within field width, and explicit
`typing_scheme='autodock4'`. A tree writes ligand layout; None requests rigid
layout. Validate exact selected atom-ID correspondence, a rooted partition and
branch roles before writing. Complete native graphs additionally validate cuts
and fragments through the public `chemical_states.get_rigid_fragments` tool. Tree
traversal may reorder atom lines; export maps preserve source correspondence.
`output_presentation` optionally changes output serials/names, per-atom group
and chain labels, and occupancy/B factors without changing the native inventory,
chemical assignments or hierarchy. Scalar values broadcast; vectors follow the
original input atom axis before extraction. Consecutive serials follow actual
written traversal. Explicit serial presentation permits arbitrary source IDs.
B-factor overrides require squared-length quantities. Only presentation fields
are accepted; charge/type overrides and field truncation are not supported.

Caller `remarks` are printable ASCII complete REMARK lines, limited to 4096
characters each and 64 KiB total; control/newline injection and the reserved
MOLSYSMT_ namespace are rejected. Provider provenance remains intact. Final
UTF-8 bytes, after both remark sets and presentation, determine the completed
`molsysmt.atom_export@1` hash and written labels. The inverse atom map comes from
actual serialization indices, never a lookup of output serials in source IDs.
Known-source pose reading validates original-source bindings separately from
the declared written axis; renamed/renumbered poses restore source labels.
Guard: `tests/form/file_pdbqt/test_output_presentation.py`.
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

### Prepared coordinate projection

`PDBQTFileHandler.project_coordinates`, `form.file_pdbqt.project_coordinates`
and `form.string_pdbqt_text.project_coordinates` share one experimental
format-owned kernel. Require explicit length quantities, complete bijective
coordinate-input/source atom pairs and one full coordinate block for each unique
selected source structure. No positional/name guess, stale omitted-H coordinate,
complete-graph requirement or chemical reassignment is permitted. Native copy,
atom-level set and canonical writing remain a supported alternative when their
documented formatting losses are acceptable.

Projection changes only the original atom coordinate columns. It retains charge
precision, typing, record kinds, serials, grouping, occupancy/B factors and tree
meaning. All source MODEL records are validated before selection. Original model
label lexemes are retained as string IDs; numerically duplicate labels remain
invalid. Coordinate fields are 8.3 angstrom, with measured per-structure rounding
error in the same unit. Application unit policy is never replaced.

Default remark policy refuses any source REMARK; explicit discard_remarks=True
removes every remark, including stale scores and global/inter-model annotations.
MODEL wrapper whitespace is canonical; extra inter-model blank lines and terminal
END may be omitted. The JSON-compatible molsysmt.pdbqt_coordinate_projection@1
report retains exact UTF-8 input/output SHA-256 and byte counts (without form
prefix), both atom-axis directions, source/output structure correspondence and
labels, converted coordinate-input digest encoding, units/precision, metadata
disposition, producing software version and optional caller-declared state
provenance. Neither hashes nor declarations authenticate molecular identity.

Indexed file output streams one model through PDBQTDocument.write_chunks and
commits only after successful generation and source revalidation. Source aliases
are refused for resident/indexed handlers and their copies. Coordinate input,
model buffers, reference/index data, report maps and full text output have
separate costs; configured estimates are buffer safeguards, not total RSS bounds.
No optional engine, new graph store, scoring workflow or compiled backend is
needed. Source grammar/field references remain those of the existing PDBQT
parser; no third-party algorithm is executed by this format edit.

User contract: [projection tutorial](../docs/content/user/tools/form/project_pdbqt_coordinates.md).
Guard: `tests/form/file_pdbqt/test_coordinate_projection.py`.

Mixed public queries preserve requested mechanical fields alongside topology
and structures. Reduced-domain pipes cover their own fields; the dispatcher
queries other requested domains on the original source, retaining the same
selected source atom-index order. It does not silently omit those result keys
or force charge/type data into Topology. Guard:
`tests/basic/get/test_mixed_mechanical_pipes.py`; resolved defect:
uibcdf/molsysmt#301.

## GRO bridge ownership and selected axes

The native GRO handler loads the first coordinate entry into a resident buffer.
Its whole-handler copy isolates mutable parsed arrays and stream ownership;
subsets or output-file serialization remain explicitly unsupported. Native
file-to-OpenMM bridges reuse native first-entry connectivity and extraction,
keeping labels, coordinates and box correspondence together. These bounds
are distinct from provider readers that expose concatenated structures.

OpenMM GRO-to-MolSys conversion assembles topology and geometry before one
native atom extraction, so selected coordinates follow native sorted source
atom order. Structure ordering/repetitions retain matching periodic boxes.

MDTraj GRO attribute queries leave the caller's stream untouched. Independent
read cursors share provider topology read-only; public copy owns a distinct
mutable topology and starts at the beginning of the same backing file. Copy
does not duplicate disk bytes or clone the original cursor. Reader cleanup
covers success, exceptions and interruption. Existing atom-count metadata is
read without trajectory allocation. Reaching the declared form is not a claim
that every attribute survives a conversion. Implementation/guards are owned by
uibcdf/molsysmt#476, uibcdf/molsysmt#477 and the execution scope in
[conversion execution](conversion_execution.md).

## XYZ coordinate edits

XYZ coordinate queries require `element='atom'`. `basic.get` defaults to
`element='system'`; XYZ has no system-coordinate getter and that request raises
`NotWithThisFormError`. This is an explicit supported-level boundary, not a
missing unit or an instruction to reshape values downstream. The direct public
route `msm.set(molsys, structure_indices=0, coordinates=quantity)` needs no
intermediate getter. The caller declares matching atom positions and chooses
the destination structures; neither route infers molecular correspondence.
See the [coordinate-delivery recipe](../docs/content/user/cookbook/delivering_coordinates.md)
and its public regression controls in
`tests/form/XYZ/test_public_coordinate_delivery.py`.

XYZ accepts length quantities of shape `(3,)`, `(n_atoms, 3)` and
`(n_structures, n_atoms, 3)`. Queries normalize the coordinate axis to rank three;
coordinate assignment and independent rigid transforms preserve the source's
original storage rank, unit and quantity library. A different application unit
policy does not reinterpret the destination's magnitude.

Rotation and translation compute on owned selected-coordinate values. Independent
results promote integer XYZ storage to float64 so fractional results survive;
existing floating storage retains its dtype. In-place floating or narrowing
updates to integer XYZ reject before publication. Construct floating coordinate
storage or request an independent transform. Ordinary `basic.copy()` retains the
original dtype and does not perform this geometric promotion. These guarantees
also cover complementary native-inventory/XYZ compositions. Floating computation
retains the limitations of its representable numerical precision.


## Two-domain native inventory and coordinate assembly

Public `convert([topology, structures])` admits explicit boolean `copy_if_all`
in either item order. The default/True path returns independent domains; Topology
always detaches. False can adopt unowned Structures for the all-axis request,
while the native Structures setter still detaches a domain with a live owner.
Selections return an independent subset. Inventory extraction sorts source atom
positions, so this shortcut canonicalizes the same atom population before both
native extractors. Structure order and repetitions remain separate and unchanged.
The pair declares index correspondence, not authenticated origin or chemistry;
missing ChemicalStates stays absent. Full-axis conflicts and malformed copy
options retain the existing public rejection. No whole-system intermediate
snapshot or new reconstruction algorithm is required.

## Trusted native object checkpoints

Native `MolSys` objects support Python's ordinary `pickle.dump`/`pickle.load`
object protocol. This is not a registered MolSysMT file form, a new API, or a
versioned molecular interchange schema. It is a bounded trusted checkpoint
route in a compatible Python/package/backend environment; keep exact source,
build and dependency identities. Only trusted files may be unpickled. Python
object serialization does not establish molecular-source authentication.

`tests/native/test_prepared_system_checkpoint.py` guards the prepared single-state
native scope: full, selected and nonpolar-H-merged methanol, multiple structures,
typed chemical history, explicit structure associations, mechanical parameters,
named charge/type provenance and sparse analyses. Fresh readers use another unit
policy, block RDKit/OpenMM/Ackredit, forbid assignment recalculation and reproduce
public one-structure-at-a-time PDBQT exports. Coordinate edits still invalidate
the restored analysis; stale charge/type/chemistry/association bindings remain
refused. These are data-fidelity controls, not validation of chemical models.

The checkpoint uses the existing native restoration/ownership hooks. It does
not reconstruct named assignments from a parameter projection or diagnostic
snapshot. Restoring a valid report does not rerun or recredit its calculation.
Stored model requests remain requests rather than certified parameterization.
Custom extension/engine objects and cross-release/platform compatibility are
not qualified by this scope. Serialization is whole-object/resident and does
not use the chunk executor or configure.max_ram_usage preflight.

H5MSM 0.5 and MolSysDict 0.2 refuse stored mechanics, including reports
without parameter values, present-empty tables/reports and unknown extensions.
One native presence helper inspects stored references without copying or scanning
per-atom values; the parameter projection cannot prove absence. The parameter-only
MolecularMechanicsDict omits complete named reports. Native pickle does not
replace a client's explicitly required H5MSM round trip or accept its entire
workflow. Public H5MSM writers now default to 1.0 and preserve the supported
experimental mechanical domain. Versions 0.5 and experimental 0.6 remain
explicitly selectable through `format_version`; the parameter-only dictionary
contract is unchanged. Stable-format freeze and installed-candidate receiving
remain under uibcdf/molsysmt#256 and #334. See the
[checkpoint guide](../docs/content/user/foundations/native_world/classes/molsysmt_MolSysDict.md#native-checkpoints).

## Public modular H5MSM operations

`h5msm.write`, `write_layers` and general `convert` default to 1.0, including
supported mechanics persistence. General reads support modular roots 0.5, 0.6
and 1.0; the legacy handler retains its separate 0.3/0.4 scope.
`read_axis_sizes` reads independent metadata endpoints without payload arrays.
The [1.0 public contract](../docs/content/user/tools/form/file/h5msm_10.md)
and [format owner](h5msm_format.md) define schema, identity, presence, query and
publication limits. Explicit 0.5 excludes stored mechanics; the
[explicit experimental 0.6 contract](../docs/content/user/tools/form/file/h5msm_06.md)
retains its version-specific limits.

File extraction preserves the source version; copies preserve bytes. Public
file-to-file conversion defaults to 1.0, preserving supported independent layers,
maps and scientific producers while recording source root metadata separately.
An explicitly requested older target refuses unsupported stored mechanics.
Topology-free, interaction-free append can retain a compatible mechanics layer
and extend an explicit structure/state map after validation. Other modifications
use resident editing and new output. Known assignments retain projection rules;
unknown/incomplete charge/type reports are transportable evidence but refuse
scientific use/remapping through SMonitor rather than acquiring new bindings.

Source `69f938947` qualifies these routes with 1,843 affected cases, fourteen
fast gates and fresh HTML. Three public fresh-reader preparations preserve
original producers, a different unit policy, selected PDBQT bytes and actual edit
invalidation without preparation engines. Scientific file projections dispatch
by root and retain explicitly requested mechanical context. These are bounded
source/contract/parity checks, not installed-client acceptance or a stable 1.0
schema declaration. See
[receiving](../devtools/data/public_mechanics_receiving_256_20261108.json).


## Nullable stable membership edits

Direct native atom group/chain, group molecule and molecule entity assignments
retain nullable Int64 storage after whole-column and selected edits. None entries
in aligned vectors denote unknown parents. A staged column prevents invalid
value types/lengths from partially publishing that edit. Public MolSys routes
reuse the Topology owner; neither creates a chemical assignment or coordinate
series. Full parent projections preserve the same stored nullable dtype and
explicit missing values in their supported paths. Unsupported chain-to-molecule
public assignment remains refused by its existing value boundary.

Known full chain assignments retain the existing reconstruction policy; unknown
chain membership preserves declared chain rows. This fix does not redesign
hierarchy inference, parent bounds, projected selection conflict policy,
interaction invalidation or multi-attribute transactions. Raw pandas writes
retain their own responsibility. Guards:
`tests/form/molsysmt_Topology/test_nullable_membership_assignment.py`.
