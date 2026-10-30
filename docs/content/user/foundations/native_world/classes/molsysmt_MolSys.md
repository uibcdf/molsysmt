(user-foundations-native-world-classes-molsysmt-molsys)=
# MolSys

## Brief Inspection

`repr(molsys)` summarizes stored dimensions and domain presence. It does not
render coordinates or tables, traverse chemical graphs, validate associations,
copy data or load structures from disk. `None` denotes an undeclared axis/domain;
zero denotes an empty declared axis/collection. Named analyses are counted
without printing their names. The summary's text is for people, not serialization
or a stable parsing interface. Use native properties or `msm.info()` for data.

The same convention covers the native containers, dictionary wrappers and file
handlers. A `Structures` summary uses stored array shapes; an absent atom-aligned
series leaves its atom count unknown. A topology reports only stable inventory; its summary never resolves chemistry. An interaction view counts selected occurrences
and evaluated structures, while its stored-relation count describes the shared
backing table. Neither summary resolves ambiguity or certifies scientific readiness.

`molsysmt.MolSys` is the primary native molecular system container in MolSysMT. It can combine topology, chemical states, a 3D structures sequence or ensemble, named interaction results, and molecular mechanics data.

Each named `Interactions` analysis uses positional integer atom and structure
indices. Its public construction and query methods validate those arguments;
fractional numbers and booleans cannot silently designate another position.
Validation also applies after invalidation or partial recalculation. The
`skip_digestion` option is reserved for inputs already checked against the
complete contract. See {ref}`user-tools-interactions-result`.

---

## Inherited Construction

Subclasses of `MolSys`, `Topology` and `ChemicalStates` can inherit their native
constructors, including from another module. They accept the same count arguments
and retain the base class's validation rules. Construct them normally;
`skip_digestion=True` is reserved for already validated internal delegation.
Native copying preserves supported subclass attributes and slots, but does not
register a new molecular-system form or guarantee subclass-specific operations.

## Overview and Role

As a user, `molsysmt.MolSys` is the central object returned when loading, converting, or processing molecular systems. By composing dedicated sub-containers, `MolSys` ensures strict separation of concerns while providing a unified gateway for selections, spatial queries, and form transformations.

Some native operations edit a `MolSys` in place; `extract` returns an independent subset. A partial `MolSys` retains only the information domains that were available in its source.

The general `msm.remove` tool returns an independent subset by default, even
when nothing is removed. Explicit `in_place=True` keeps the MolSys identity,
replaces its domains together and returns `None`. Previously held domains and
analysis views remain snapshots; obtain current domains again from the edited
system. An attached Topology or Structures cannot be resized on its own.
Named analyses follow extraction's index projection and retain their original
evaluated scope; removal does not recalculate them. See {ref}`Tutorial_Remove`.

If you hold chemical states and structures separately, use
`msm.convert([chemical_states, structures], to_form='molsysmt.MolSys')`.
The chemistry may also be a `ChemicalStatesDict`. The pair declares matching
atom-index correspondence and produces a topology-free system; index selections
remap both domains together. The reference state is preserved, but several
states are not automatically assigned to structures. See {ref}`Tutorial_Convert`.

You can also compose standalone native `Topology`, `ChemicalStates`, `Structures`
and `MolecularMechanics` providers. A supplied `ChemicalStates` owns chemistry;
no Topology fallback creates chemistry when that domain is absent. Listing
these domains declares positional correspondence, not common origin. Full atom
axes must agree before selection; repeated explicit providers fail. Mechanical
values, settings and original producer reports are retained without recalculating
charges or legitimizing stale assignments. A list of partial `MolSys` inputs
retains its separate, bounded contract; it does not transfer mechanics.

An explicit `ChemicalStates` or `ChemicalStatesDict` can also accompany native
inventory and one coordinate-only source, such as a DCD file. Only the requested
structures are read before composing the shared atom axis; atom extraction then
remaps inventory, every state and coordinates together. A foreign source with
its own inventory or chemistry is not silently treated as coordinates by this
route. Missing structure-to-state assignments remain unknown.

The default native composition result is independent. `copy_if_all=False` avoids
the final snapshot for a full-axis request, but domains with a live molecular
owner still detach according to their native ownership rules. Unowned structures
and supplied mechanics can be shared explicitly. Index selections use existing
extraction: Topology-backed atom subsets are sorted; a chemical/structural-only
system retains the requested atom order. Several chemical states do not acquire
an automatic structure association. H5MSM 0.5 still rejects nonempty mechanics.

---



Direct `MolSys.add` and `Topology.add` calls also validate `keep_ids` as a boolean, including its default `True`. Leave `skip_digestion=False` for ordinary public calls; trusted delegation is not required to use these methods.

## Restricting Chemical Domains

An atom selection restricts every stored chemical state while preserving state
order, the reference and structure-to-state associations. With complete stored
connectivity, components describe the retained induced graph. Removing the middle
atom of a three-atom path therefore leaves two components. Both can still belong
to the same stable molecule: molecular identity and covalent connectivity are
separate domains.

For complete graphs, component labels survive only when the full original atom set is unchanged.
New or cut components receive local string IDs and unknown names/types. With
partial or unavailable connectivity, extraction instead restricts the declared
memberships; it does not invent a complete partition from the visible edges.
Those rows still describe restricted source declarations. Cutting a retained
component downgrades a complete declaration to partial.

Stereo references follow their corresponding bond endpoints when atom order
changes. Removing a defining stereo neighbor clears the now-incomplete bond
stereo annotation. Historical preparation records retain their original index
scope. A complete induced graph is not a prepared standalone chemical fragment:
extraction does not add caps or hydrogens, perceive aromaticity, choose a chemical
state or recalculate interactions. See {ref}`Tutorial_Extract` and
{ref}`Cookbook_Group_Free_Hierarchy` for executed examples.

## Native Queries

`get()` and `info()` share the basic-tool query and table contracts, using known
native providers for explicit index requests. They validate input by default.
`Topology`, `Structures`, `ChemicalStates`, `Interactions` and `MolSysBuilder`
offer the same pattern for the attributes available in their own domains.
Selection expressions retain the existing selector. No query builds or converts
the native system merely to locate its data.

Use keyword arguments to mirror the free functions. Native `get()` accepts
`chemical_state` by keyword; native `info()` accepts `structure_indices`,
`output_type` and `mask` by keyword. Existing MolSys positional calls retain
their meaning. `to_form()` continues to use the registered target converter.
Leave `skip_digestion=False` for user input. The executed examples are in
{ref}`Tutorial_Get` and {ref}`Tutorial_Info`.

A partial MolSys can be summarized without topology. Missing domains are not
invented. `Interactions.get()` exposes its declared molecular axes; occurrence
selection and bounded export retain their specialized sparse methods.

(user-foundations-resident-copying)=
## Native Copying

Native convenience methods and Python copy hooks retain the current concrete
supported type, ordinary extension state, graph aliases and cycles. Public
`copy()` methods validate `skip_digestion`; leave it `False` for user calls.
Copying preserves stored data and does not infer chemistry, normalize tables,
decode a payload or certify a schema.

| Object | `copy()` and `copy.deepcopy()` | Python `copy.copy()` |
| :--- | :--- | :--- |
| `MolSys`, `Structures`, `MolSysBuilder` | Eager geometry by default; `copy(deep=False)` shares protected coordinate/box blocks. Other mutable fields detach. | Independent state over protected geometry blocks. |
| `Topology`, `ChemicalStates`, `MolecularMechanics` | Independent canonical tables and metadata, copied eagerly. No `deep` argument. | The same independent molecular-data contract. |
| `Interactions` | Independent analysis handles, metadata and array headers; immutable sparse bytes may remain shared. No `deep` argument. | The same independent sparse-result contract. |
| `MolSysDict`, `TopologyDict`, `ChemicalStatesDict`, `InteractionsDict`, `ViewerJSON` | Independent wrapper and mutable payload, without decoding. No `deep` argument. | Independent wrapper and mutable payload, with the same graph memo rules. |

The wrapped interchange payloads retain their own schemas. Preserving ordinary
Python extensions in a resident copy does not add persistent schema fields.
Copying a wrapper
does not add MolSys owner bindings or convert it to a native molecular domain.
Plain Python dictionary forms, including `StructuresDict` and
`MolecularMechanicsDict`, retain Python's shallow `dict.copy()`/`copy.copy()`
semantics. Use `msm.copy(data)` for an independent registered-form snapshot.
`Simulation` settings and live file/resource handlers retain their separate
reference/resource contracts.

File paths have a separate copy boundary: `msm.copy(source_filename)` creates
an independent temporary in a private system-temporary directory owned by the
current Python process. It retains the stored format, suffix and bytes, including
a legacy H5MSM version. Paths remain usable through the session, independently of
Python string lifetimes. Normal-exit cleanup is best effort; abrupt termination
or locked files can leave leftovers. An explicit `output_filename` creates a
persistent caller-owned copy which MolSysMT never automatically removes.
Composite sources receive separate copies of their file members. Copying does
not add a format's missing write capabilities; convert to a native MolSys when
needed for subsequent transformations. See {ref}`Cookbook_Copying_Disk_Systems`.


(user-foundations-molsys-copying)=
## Independent Copies

`molsys.copy()` and `copy.deepcopy(molsys)` copy coordinate and box bytes eagerly.
`molsys.copy(deep=False)` and `copy.copy(molsys)` instead share protected geometry
blocks until an edit replaces affected blocks. Both modes create independent
native domains, canonical tables, other mutable series and named-analysis handles.
The universal `msm.copy(molsys)` keeps the eager default. Assigning
`molsys_A = molsys` still refers to the same live system.

Each copied topology belongs to its copied system and remains independent of
the copied chemical collection at `molsys_A.chemical_states`. Structure-to-state
assignments, missing domains, local/source index maps, producer versions and
occurrence indices survive unchanged. Copying does not reconstruct the system,
remap interactions, infer chemistry or pack a lazy analysis. Immutable sparse
numeric bytes can remain shared in both modes. Existing query caches and mutable
metadata still need independent storage; a deferred copy is not cost-free.

```python
molsys_A = molsys.copy(deep=False)
assert molsys_A.topology is not molsys.topology
assert molsys_A.chemical_states is not molsys.chemical_states
```

Edit copied coordinates through `msm.set(molsys_A, ...)` or
`molsys_A.structures.set_coordinates(...)` to invalidate the affected structures
in every named analysis on that copy. The attached domain's `set_box()` and
full `coordinates`/`box` assignments also notify its owner. The original's
geometry, coverage and previous query snapshots remain unchanged. Standalone
domain copies have no owner. Assigning an already attached `Structures` to
another system creates an independent domain wrapper with deferred geometry
allocation, preserving the original owner. Assigning another system's
`ChemicalStates` likewise creates independent chemical tables and retains one
authority shared by the destination's topology and chemical domain. Standalone
chemical copies/pickles omit their weak owner link; system copies/restoration
rebind it. Unobserved chemistry/table edits and
whole-domain replacement still require explicit owner invalidation. Use
`MolSys` extraction/append operations to change axes with attached analyses.
See {ref}`Changing coordinates <user-tools-interactions-coordinate-edits>`.

Tables are copied eagerly; this is not table copy-on-write. Use their canonical
molecular columns rather than storing arbitrary mutable Python objects inside
cells. Such objects and table metadata follow pandas' own copy protocols and
are outside this qualified molecular-data boundary. Repeated references to a canonical table follow the containing graph's memo;
this does not preserve every shared-buffer relationship between distinct views.
Subclass slots retain their values and aliases, including separate parent and
child storage with the same name. Standalone copies omit the old owner even
when that link is stored in a slot. External resources must supply their own
copy support; a failed copy does not transfer the source's native ownership.
Resident extension support does not add persistent schema fields.
ChemicalStates's default pickle hook refuses ambiguous slot names with stored values rather
than silently dropping one value; such subclasses need a serialization hook. Plain dictionary forms retain Python dictionary
copy semantics; they do not acquire MolSys domain ownership.

Loading one H5MSM 0.5 file into one `MolSys` already creates an independent
resident system. Public `msm.convert(filename, to_form='molsysmt.MolSys')`
uses that fresh system without taking another eager snapshot by default.
Repeated loads remain independent, and explicit `copy_if_all=True` still
requests the extra snapshot. Converting an existing resident `MolSys` keeps
its independent-copy default. This does not make file conversion a lazy or
selective coordinate reader.

## Internal Attributes

The native container exposes these domains:

| Attribute | Internal Object Class | Description |
| :--- | :--- | :--- |
| **`topology`** | `molsysmt.Topology` | Stable atom, group, molecule, entity and chain inventories; no chemical connectivity facade. |
| **`structures`** | `molsysmt.Structures` | Structural container holding 3D coordinates `(n_structures, n_atoms, 3)`, periodic box matrices `(n_structures, 3, 3)`, and structure timestamps. |
| **`chemical_states`** | `molsysmt.ChemicalStates` | State-dependent covalent bonds and atom-level chemical assignments. |
| **`interactions`** | Named `molsysmt.Interactions` results | Sparse observations with declared atom and structure index domains. |
| **`molecular_mechanics`** | `molsysmt.MolecularMechanics` | Forcefield parameters, partial charges, atom masses, and non-bonded interaction rules. |

An H5MSM 0.5 file may load as a partial `MolSys` without topology. If it
contains only named interactions, those results supply the atom and structure
index domains. `extract(atom_indices=[...], structure_indices=[...])` remaps
the present domains and keeps the selected structure order. An axis with no
declared domain cannot be selected explicitly.

A system with topology and chemical states can also select atoms while
`structures is None`; extraction keeps the coordinates absent and remaps the
available chemistry. With topology, atom subsets use sorted source indices.
Without a Structures domain, named analyses may still declare a structure-index
domain; otherwise an explicit structure selection raises `ValueError`.
Public H5MSM 0.5 reads and writes preserve this combination, including several
named analyses and evaluated structures without observations. The stored axis
associations declare correspondence; they do not supply missing coordinates,
periodic boxes or per-structure chemical-state assignments. See
{ref}`H5MSM 0.5 <user-tools-form-h5msm-05>`.
Complementary partial systems or matching H5MSM 0.5 files can be consolidated
with `msm.convert([molsys_A, molsys_B])` before selecting atoms/structures.
The list declares positional correspondence; each native domain has one provider
and analysis names are distinct. Full-axis conflicts fail before extraction.
Topology is copied to preserve its input owner's binding, while full-axis
`copy_if_all=False` can share structural arrays. See {ref}`Tutorial_Convert`.

Both hydrogen-bond detectors and the disulfide candidate detector can return an
independent `molsysmt.Interactions` analysis with
`output_type="molsysmt.Interactions"`. Attach it under a name by assigning
`molsys.interactions = {**molsys.interactions, "analysis_name": analysis}`.
This retains previous named results and checks that all analyses match the
system's atom and structure axes.

An analysis owns sparse relations and occurrences. A query retains selected row
indices and shares the analysis's numeric storage. Its experimental `to_page()`
projection copies a bounded set of observations and their referenced participant
definitions; it preserves complete-analysis occurrence indices. Coverage and
source maps remain shared read-only data. Query indexes, structure metadata and page
copies have distinct memory costs. See
{ref}`Inspecting bounded pages <user-tools-interactions-pages>`.

Atom queries distinguish observations involving a selection, entirely within it,
or across its boundary. The public names are `involving_selection`,
`within_selection` and `across_selection_boundary`; `between_selections` connects
two explicit disjoint sets. All constituent atoms of each participant count,
including the hydrogen in a hydrogen bond and every atom in a ring. These
filters select stored evidence and preserve its original scientific search scope.

This assignment declares that the analysis's local atom and structure indices
correspond to the system. MolSysMT checks compatible axes and valid results;
you are responsible for the correspondence of independently loaded data.
Source labels and maps retain provenance without authenticating that origin.
Chemical recognition and geometric criteria are separate parts of an analysis.
Named hydrogen-bond, π–π, cation–π, halogen and hydrophobic profiles carry
their pinned method references;
a geometric profile on declared participants need not reproduce the reference
package's feature discovery. Different definitions remain separate named analyses.
The method reference describes the reproduced definition, while the producer
describes the software that actually generated these observations.
Each analysis's `software` dictionary records its producer versions; saving
or loading the system preserves those versions rather than substituting
the version installed by the reader. An empty dictionary means unknown.
Detector-produced analyses also keep bibliographic records and contextual
roles in `analysis.parameters["attribution"]`, once per named analysis.
These records accompany the system through H5MSM and extraction. Optional
Ackredit sessions collect references from completed calculations; opening a
saved system does not claim those calculations were performed again.
Optional attribution failures preserve completed science under strict warning
filters. Failed diagnostic delivery uses a fallback log with its code, operation
and both error reasons; it does not change the scientific exception policy.
Method names identify authors or criteria, and profiles identify the reproduced
recognition/geometry conventions. See
{ref}`Methods and attribution <user-tools-interactions-attribution>`.
See
{doc}`the interaction result guide <../../../tools/interactions/result>`
for participant roles, evaluated coverage, and experimental detector limits.

---

## Charge Interpretation

Formal charges describe a selected chemical state. Force-field partial charges
are molecular mechanics parameters. Residue descriptors or protonation assumptions
are named interpretations and do not replace either stored source automatically.

The experimental {func}`molsysmt.physchem.get_partial_charges` calculates an
explicit Gasteiger-Marsili or named force-field model on the full chemical graph.
{func}`molsysmt.build.assign_partial_charges` attaches one validated single-state
assignment to a detached MolSys, preserving source atoms, IDs, coordinates and
analyses. Native mechanical values use elementary charge; provenance records
original producer versions and projected source indices. PDBQT checks stored
assignment consistency and records a bounded summary before export rounding.
These mechanical values and reports are excluded from H5MSM 0.5. See
{ref}`Tutorial_Partial_Charge_Assignment` and {ref}`cookbook-assigning-partial-charges`.
Manual native writes through `msm.set(..., partial_charge=...)` accept finite
vectors or charge quantities, preserve formal charges and retain missing values
for unassigned atoms. Setter values follow an explicit index selection's order.

The experimental {func}`molsysmt.physchem.get_charge_centers` tool produces
sparse chemical features for one state, with whole-center atom membership,
distance-reference atoms, unitful charges, original input indices and evidence.
A molecule of zero net charge can contain separate local charged centers.
Those features precede geometric detection and are distinct from the occurrence
analyses stored in `interactions`.

The experimental `msm.interactions.ionic.get_ionic_interactions()` calculation
uses those features and an explicit geometric cutoff to produce an analysis.
You attach it under a chosen name by assigning
`molsys.interactions = {**molsys.interactions, 'ionic': analysis}`. It records
geometric proximity between opposite formal-charge centers, not an interaction
energy or a recorded bond. See {ref}`Tutorial_Get_ionic_interactions`.

The experimental `msm.interactions.pi_pi.get_pi_pi_interactions()` calculation
uses declared aromatic ring chemistry and least-squares planes. Explicit cutoffs
define parallel or edge-to-face observations; planarity alone does not establish
aromaticity. It returns another independently named analysis, with the same
source-index, coverage, producer-version and persistence contracts. Store both
families in `molsys.interactions` under different names. See
{ref}`Tutorial_Get_pi_pi_interactions` and {ref}`Cookbook_Saving_pi_pi_interactions`.

---

The cation–π detector defaults to the attributed ProLIF 2.2.2 definition and returns
another named analysis. Its original method reference is separate from the producing
MolSysMT/RDKit versions. The custom centroid/angle/offset proposal has a different
participant and geometric definition; no scientific superiority is established.
See {ref}`Tutorial_Get_cation_pi_interactions` and
{ref}`Cookbook_Saving_cation_pi_interactions`.

The experimental halogen detector adds an independent named analysis with four
roles: donor, halogen, acceptor and acceptor reference. Every eligible reference
neighbor remains identifiable. Chemical recognition can be inspected separately
through the general site tool. See {ref}`Tutorial_Get_halogen_bond_sites`,
{ref}`Tutorial_Get_halogen_bonds` and {ref}`Cookbook_Saving_halogen_bonds`.

Hydrophobic observations use a separately named atomic chemical interpretation
and a distance criterion. Their two roles identify canonical source-index order,
not ligand and protein sides. They are distinct from residue hydrophobicity
values or interaction energies. You can calculate a disjoint interface, attach
under a name and preserve its original scope and references in H5MSM 0.5. See
{ref}`Tutorial_Get_hydrophobic_sites`, {ref}`Tutorial_Get_hydrophobic_interactions`
and {ref}`Cookbook_Saving_hydrophobic_interactions`.

ChemicalStates distinguishes implicit hydrogen counts, bracket-declared atom-level
explicit hydrogen counts (`n_explicit_hydrogens`), and real indexed H atoms. Native
and H5MSM round trips preserve the annotations without adding coordinate rows.

{ref}`Explicit template preparation <Tutorial_Chemical_Templates>` can fill missing
assignments in a selected state. With explicit `complete_from_template` policy,
it can also add missing declared covalent edges to an incomplete graph. Components
are then rebuilt in that state. Indices can change; whole-input completion
regenerates IDs, while scoped completion retains IDs for unchanged atom sets.
Names/types are retained for unchanged memberships and missing for merged/split sets;
stable atom order, group/molecule inventory, other states and structures stay
intact. This returns an independent MolSys, invalidates its named interaction
observations when chemistry changes, and supplies a detached bond-index map.
With an explicit closed-component `selection`, you can also fill assignments
inside the original atom domain. Its map uses full-system indices, and a proper
subset leaves global connectivity completeness unchanged. Other components stay
outside that assessment. H5MSM retains the scoped values and the conservative
global flag. The selected ChemicalStates record retains template-application
history, accessible with `molsys.chemical_states.get_preparation_history()` and
preserved by H5MSM 0.5. An explicit atom stereo label `unspecified` is a
stored declaration, distinct from missing/unknown metadata; it does not certify
achirality. Template transfer preserves explicit agreements and rejects conflicts.
Strict correspondence checks still require potentially stereogenic sites to be
assigned independently. Each historical envelope declares the original operation's
indices and output dimensions; it is not a certificate for current assignments.
Copy, extraction, reordering, merging and later edits retain that original
evidence without rewriting it. Returned history values are independent copies.

State-aware connectivity queries also keep the atom axis intact. The bond graph
and covalent-block tools accept an explicit state or resolve one from selected
structures. Missing or mixed associations raise. A selected graph contains only
bonds whose two endpoints are retained; omitted atoms cannot connect its blocks.
The label-array output uses -1 outside the selection. This inspects stored
connectivity without promoting partial chemical coverage to complete.
Successful fixed-state H generation and terminal attachment also retain historical
reports, including original source structure counts and evaluated indices.
`append_preparation_history(records)` archives caller-selected records in append
order without applying chemistry, aligning axes or verifying source authenticity.
Stored external relationships are unassessed, so a protein cut is not silently
treated as a complete molecule by the default closed-component operation.
An explicit {ref}`context map <Tutorial_Context_Chemical_Template>` lets a
selected atom scope use a larger declared complete template. It checks all
incident edges, fills selected atom/boundary bond fields and preserves outside
atoms and outside-only bonds. It does not add edges, invent cut termini or elevate
global completeness. Historical context maps persist with their original axes;
full-graph recognizers still require preparation beyond a partial receptor scope.
See {ref}`Updating a selected component
<Tutorial_Selected_Chemical_Template>`.

The {ref}`mapped-H reinsertion recipe <cookbook-component-hydrogen-reinsertion>`
composes public extraction, fixed-state H generation, terminal attachment and
`msm.set()` to retain the original atom axis. Indexed H replace their parents'
materialized virtual counts. The one-state, one-structure route preserves existing
coordinates and unrelated chemical assignments, retains global completeness,
and invalidates analyses after expansion. Strict attribute policy rejects loss;
intersection reports it. The recipe explicitly imports the isolated H-generation
record into destination history, retaining its original component domain alongside
the full-complex attachment record. H5MSM saves both without copying coordinates
into the reports. This history does not certify environmental H orientation.

The original system remains unchanged. Template transfer does not select
protonation, create missing atoms or supply hydrogen coordinates.

The {ref}`peptide-template factory <Tutorial_Get_Peptide_Chemical_Template>` builds
a separate reference MolSys with explicit residue/terminal/link chemistry and
stored H counts. Its synthetic indices/IDs do not identify atoms in an observed
system. A caller-declared map establishes that correspondence before template
transfer. The reference has no coordinates or specified stereochemistry; it is
not a modeled pose or an independently certified biological chain. The template's
chemical state retains its construction report and full declaration, including
the original assembly version. Application records the caller-supplied declaration;
archive reference history explicitly if it should accompany the observed system.

The {ref}`aromatic normalization tool <Tutorial_Normalize_Aromatic_Bond_Orders>`
can canonicalize already declared aromatic bond orders on a copy, preserving
connectivity completeness and all atom assignments. It does not perceive
aromaticity. Its returned copy retains an independent original-order report in
chemical-state history, including unchanged operations; H5MSM preserves the report.
Changing the representation invalidates named interactions on the copy.

Separately prepared components can form a new analysis system through
`msm.merge()`. This concatenates their atom axes and declared chemistry; completeness
describes only the included graph. Preserve extraction maps to the original
system and mark generated H with unknown source indices. Atom IDs are labels
and may repeat across input components. The original partial complex remains
unchanged. Merge concatenates preparation histories in source order, with
each original operation domain intact. Normalization and peptide-factory evidence
retain their original domains too; archived reference records do not map themselves
onto the current system or certify its chemistry.
See {ref}`Composing a prepared interface <cookbook-prepared-interface>` for a
bounded receptor/ligand example with named interaction persistence. Local H
placement does not establish an environment-optimized pose.

The explicit {ref}`fixed-state H operation <Tutorial_Fixed_State_Hydrogens>`
can materialize those counts on a prepared isolated component. Declared aromatic bonds may
use fractional order 1.5 without an integer order; nonaromatic bonds still need
supported integer orders. The operation preserves the original atom indices,
pose and aromatic state on its returned copy.

## Evidence Updates

Editing coordinates or periodic boxes with `msm.set(molsys, ...)` removes
observations and evaluated coverage for the selected structures in every named
analysis. Even a previously evaluated structure with zero observations becomes
unevaluated after its geometry changes. Other structures and previously held
result/query snapshots remain intact. Recalculate the changed structures before
claiming new observations or evaluated-empty coverage.

Empty atom/structure selections and identifier/time changes do not
invalidate analyses. With attached results, full geometry assignment preserves
the structure axis; use extraction or append operations to change that axis.
Invalidation shares read-only observation columns and changes structure validity
without duplicating the surviving observations. Complete-column access,
remapping or export may materialize active columns later. After recalculating
selected structures on the original axes and scope, use
`current.replace_structures(fresh)` and attach its result under the same name.
Compatible recalculations may use different coordinate block sizes or execution
policies. Each analysis keeps their structure membership and details in
`execution_records`, including evaluated-empty structures; scientific parameters,
producer versions and atom scope must still agree. Saving the full system in
H5MSM writes these analyses from their active blocks without packing all their
observations. Remapping or typed dictionary conversion can still materialize them.
To release retired observation blocks after repeated edits, explicitly attach
`current.compact()` under the same name and release old analyses and query views.
Compaction preserves the indices and coverage; it needs memory for new columns
and keeps unused relation definitions. See
{ref}`Reclaiming retired observations <user-tools-interactions-compaction>`.

This preserves other structures and checks calculation compatibility; attaching
`fresh` directly would replace the whole named analysis. Geometry delegation failures conservatively retain
unevaluated coverage because a partial write may have occurred.

This automatic boundary is the native MolSys form. If you edit a separately
accessed `molsys.structures` directly, explicitly replace each affected named
result with `analysis.invalidate_structures(structure_indices)`. Geometry
setters do not infer changes made through independent objects or aliased data.

Invalidation applies even when the moved atom did not participate in a previous
interaction: moving it can create a new one. No detector runs automatically.
Use structure coverage, not a zero occurrence count alone, to distinguish a pending
calculation from a calculated absence. See
{ref}`Changing coordinates <user-tools-interactions-coordinate-edits>` for a
copyable example and the complete edit policy.

Changing chemical-state atom or scientific bond assignments through
`msm.set(molsys, ...)` or `msm.set(molsys.topology, ...)`, or replacing
`molsys.chemical_states`, marks every
named analysis unevaluated. Charge centers, aromatic participants and
hydrogen-bond roles can change at fixed coordinates. MolSysMT conservatively
invalidates all covered structures because it does not infer each method's
chemical dependencies. Empty atom/bond selections and bond ID changes preserve
analyses. Assigning or clearing `structure_chemical_state_index` invalidates
only the selected structures. Earlier result/query snapshots remain available.

Native topology bond addition/removal and replacing its bond table also notify
the owner. Standalone topology copies are detached.
`molsys.chemical_states.append_state()` also makes all analyses unevaluated,
without copying existing states or coordinates. Explicit structure-to-state
assignments remain unchanged. With multiple states, structures without an
explicit assignment resolve to unknown. Appending preparation history only
archives evidence and preserves analyses. Other private chemical collection
edits, whole-topology replacement, mechanics changes and raw table/array edits require explicit
owner invalidation. Recalculate and attach new results before claiming that
these changed data have been evaluated.

## Invariants and Performance

Structural iteration reads the existing `structures` domain without copying
the complete ensemble first. Coordinate getters copy only the requested
atom and structure selection. The original system stays in memory, and
collecting every returned block still stores the complete selected result.
Use structure **indices** to choose rows; `structure_id` contains labels
that need not be consecutive numbers or match those indices.

- **String Identifier Invariant**: All element IDs (`atom_id`, `group_id`, `chain_id`) inside `topology` are normalized to string representations.
- **Fast Digestion Bypass**: Compatible with `skip_digestion=True` for high-frequency internal algorithm passes.

---

## API Documentation

See {ref}`API Native Queries` for resident-object queries and
{func}`molsysmt.basic.convert` for form-agnostic conversion.

Metal coordination candidates and one- or two-water hydrogen-bond paths can be named
independent analyses in `molsys.interactions`. Their observed geometry does not
change declared chemical-state bonds. See {ref}`Getting metal coordination
<Tutorial_Get_metal_coordination>` and {ref}`Getting water bridges
<Tutorial_Get_water_bridges>` for exact chemical requirements and atom scopes.

### Detached aromaticity

ChemicalStates owns declared aromatic flags. Optional
{func}`molsysmt.physchem.get_aromaticity` returns detached model-dependent flags
on a complete selected graph; it does not fill missing stored assignments.
See {ref}`Tutorial_Get_Aromaticity` for prerequisites and source-axis evidence.


### Named chemical types

Chemical element symbols remain in `atom_type`. Mechanical `atom_ff_type`
labels are separate parameter assignments. A named chemical-environment profile
can attach labels with an `atom_type_assignment` report in MolecularMechanics.
It records the original rule/provider versions and binds labels to chemistry.
Extraction projects parent labels; manual replacement clears their attribution.
Use `msm.set(molsys, element='atom', selection=[...], atom_ff_type=[...])`
to edit labels in the supplied atom-index order. The first subset edit allocates
the full system atom axis, leaving other labels unknown. An empty selection is
a no-op; `atom_ff_type=None` clears the full column. Charges, chemical states
and coordinates remain intact. This manual declaration clears named typing
provenance and requires owner invalidation of dependent interaction analyses.
The PDBQT writer rejects stale named reports before writing. Charges and typing
are independent operations; neither establishes full parameterization. Both
mechanical reports are excluded from H5MSM 0.5. See
{ref}`Tutorial_AutoDock_Typing` and {ref}`Tutorial_Assign_AutoDock_Types`.

Native heavy-atom repair and terminal insertion retain the selected state's
known atom assignments and provenance while leaving new chemical fields unknown
and marking connectivity partial. They require one chemical state for expansion.
Atom IDs survive; group sorting or inserted groups can change indices. Named
interaction definitions and source-axis maps are retained and remapped, while
occurrences and evaluated coverage are cleared for recalculation. Atom-aligned
structural observables and force-field parameters without new values are reported
as dropped. The heavy-atom tool offers strict rejection of that loss. See
{ref}`Tutorial_Add_missing_heavy_atoms` for repair limits and attribute policy.

## Chemical Correspondence

`chemical_states` supplies declared assignments for
{func}`molsysmt.chemical_states.get_atom_correspondences`. Its reusable dictionary maps
positions in both source atom axes, independently of coordinates or string IDs.
A metric selection retains its full covalent component as chemical context.
Coordinate changes permit map reuse; chemical changes, atom-axis reordering or
changed populations require recomputation.

{func}`molsysmt.structure.get_symmetry_corrected_rmsd` evaluates those maps in
the supplied Cartesian axes, preserving receptor-relative ligand position and
orientation. Its original positional baseline requires an explicit source map.
Both experimental tools retain detached original producer versions and scientific
attribution. See {ref}`Tutorial_Get_atom_correspondences` and
{ref}`Tutorial_Get_symmetry_corrected_rmsd` for required chemistry and limits.

Partial `fixed_atom_correspondence` anchors restrict the chemical search;
complete `candidate_atom_correspondences` restrict it to validated proposed maps.
Both use source indices and preserve the full chemical context. Keep the declared
`search_scope` with the value: an anchored or supplied-map minimum is conditional,
and `search_complete` refers to that scope. The baseline map only defines raw
positional RMSD. Cached dictionaries retain their constraints on reuse.

## Atom Axis

Atom indices are positions shared by all attached domains. Selecting a complete
atom set with `extract` keeps its selection semantics. A declared reordering uses
{func}`molsysmt.basic.permute_atoms` and returns an independent native system.
Only the atom axis changes: group, component, molecule, chain, entity, bond,
chemical-state and structure axes remain fixed. Original IDs stay string labels.
Stored chemistry, structural series, mechanics and named interactions must all
follow the new atom axis; permuting coordinates alone is insufficient.

The initial experimental operation supports built-in domains and rejects
unknown extensions without a remapping contract. Historical preparation axes
remain historical; the returned atom map describes the new transformation.
See {ref}`Tutorial_Permute_Atoms` for supported domains and memory limits.
