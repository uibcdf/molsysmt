# Attribute-Centric Molecular-System Architecture

**Status:** architectural proposal; concept agreed, implementation contracts pending

**Priority:** foundational design; implementation must be split into independently
validated changes

## Purpose

MolSysMT should represent molecular information without requiring every molecular
system form to contain a complete system. A sequence, a topology, a coordinate
trajectory, a parameterized simulation system, an interaction analysis, and a
reactive QM/MM trajectory are all valid but different representations of
molecular information.

This proposal records the agreed architectural direction for extending that
model. It is intentionally more complete than an implementation ticket. It
separates decisions already made from details that still require evidence and a
maintainer decision.

No new public object or attribute described here is implemented merely because
it appears in this document.

## Executive decision record

The following architectural decisions are agreed:

1. MolSysMT remains **attribute-centric**. A molecular system is understood
   through the attributes available from one form or a composition of forms,
   not through a requirement that one object contain every possible property.
2. The global attribute registry is the common vocabulary. Form declarations
   and instance-aware `has_attribute()` checks are the capability mechanism.
   A second concept named `coverage` must not duplicate that mechanism.
3. Native `Topology` is proposed as the non-geometric topological umbrella. It
   contains a stable atom inventory and semantic organization plus zero, one,
   or multiple nested chemical states over that atom index space. Geometry must
   not silently mutate any chemical state.
4. Native `Structures` contains frame-dependent geometry and structural
   observables.
5. `MolecularMechanics` remains an optional information domain describing an
   energetic model or parameterization, not intrinsic chemical truth.
6. A future `Interactions` object may represent declared or observed
   non-covalent and coordination relationships, including their structure
   scope and analysis measurements.
7. `Topology.connections` will not be introduced. Non-covalent declarations
   and frame-dependent observations belong to the interaction domain. Covalent
   graphs, their atom-level chemical assignments, and their component
   partitions belong to chemical states nested under topology.
8. Reactive chemistry must not be represented by silently changing one graph
   with geometry. The chemical-state boundary is required conceptually from
   version 1.0 even if the first implementation efficiently supports only zero
   or one reference state; multi-state reactive workflows remain later work.
9. Provenance is optional cross-cutting metadata explaining where imported or
   derived information came from and, for calculations, which method and
   parameters produced it. It is not currently proposed as a peer molecular
   domain or mandatory public `MolSys.Provenance` object, and it does not
   replace the attribute system.
10. Element IDs are string labels and need not be unique. Internal indices are
    the identity and remapping mechanism. Converters must preserve duplicate
    source labels when the target representation permits them.

The following are not yet accepted implementation contracts:

- exact class names and public constructors for `Interactions`,
  `ChemicalState`, and any chemical-state collection;
- exact DataFrame, array, or sparse-storage schemas;
- exact controlled vocabularies and dtypes for new bond and interaction
  attributes;
- whether optional native domains are represented by `None` or by empty
  containers;
- whether `Interactions` is attached to `MolSys` by default, attached only on
  request, or normally returned as an independent form;
- the final long-term ownership boundary: experience may justify extracting
  chemical states from `Topology` or renaming the stable topology core in a
  later major design, but no such split or rename is approved now.

## Why this architecture matters

MolSysMT already supports molecular systems expressed as one form or as a
combination of complementary forms. A topology and a trajectory can contribute
different attributes to the same operation. The architecture should extend
that principle rather than introducing a monolithic definition of a complete
molecular system.

The intended model is:

```text
recognized molecular attribute
        |
representable and publicly deliverable by a form
        |
available in a particular instance
        |
consumed or produced by a form-independent operation
```

This makes the attribute vocabulary, not any third-party object model, the
interoperability boundary. Native objects group related attributes and provide
efficient invariants, but their existence must not imply that every grouped
attribute has a value.

The resulting scope is broader than trajectory analysis. The same language can
support sequence-level systems, structural ensembles, molecular mechanics,
drug-design interaction analysis, and eventually reactive trajectories while
preserving explicit scientific boundaries.

### Composition is part of the attribute contract

Attribute-centric composition is only safe when complementary forms refer to
compatible molecular data. A topology, trajectory, and parameterization cannot
be combined solely because their attribute names do not overlap. The
composition contract must validate at least:

- atom count and atom-order compatibility;
- an explicit atom mapping when index spaces differ;
- structure count, time, and frame alignment where more than one form is
  structure-dependent;
- unit compatibility;
- topology compatibility for mechanics, interactions, and chemical states;
- deterministic behavior when two forms can deliver the same attribute.

Conflicting sources must not be resolved silently. Candidate policies include
explicit source selection, declared precedence, equality validation within a
scientific tolerance, or preservation as separate named interpretations. The
accepted policy may depend on the operation, but it must be observable and
reproducible.

This is a central contract rather than an edge case. Without it, the union of
attributes can produce a syntactically valid but scientifically misaligned
molecular system.

## Evidence from the current repository

### Implemented foundations

The following foundations already exist:

- `molsysmt.attribute.attributes` registers a common vocabulary and classifies
  topological, structural, mechanical, and dynamical attributes.
- Every form adapter has an `attributes` declaration and a form-specific
  `has_attribute()` path.
- `msm.form.has_attribute(form, attribute)` reports the adapter's declared
  public delivery capability.
- `msm.has_attribute(item, attribute, include_none=False)` asks whether an
  instance can currently deliver an attribute.
- Public operations can consume a list of complementary molecular-system
  forms.
- Native `MolSys` currently synchronizes `Topology`, `Structures`, and
  `MolecularMechanics`.
- `Structures` stores coordinates and boxes as frame-indexed tensors.
- Existing hydrogen-bond functions already produce results per requested
  structure, demonstrating that these relationships are not topological
  constants.

These facts are implementation evidence, not evidence that every form
declaration is truthful or every optional-state distinction is already correct.

### Current gaps found during the design audit

The audit identified the following gaps:

- Some form-specific `has_attribute()` implementations return only a static
  declaration and do not inspect the particular instance.
- Native `has_attribute()` can infer availability from a non-empty atom or bond
  table even when an optional column is absent or all-null.
- An empty native bond table currently cannot reliably distinguish unknown
  connectivity from known connectivity with zero bonds.
- Some adapters advertise bond metadata that their converters or getters do
  not preserve.
- Native `Bonds_DataFrame` stores `order` and `type` as strings without a
  documented chemical vocabulary or orthogonal semantics.
- All native bond rows currently participate in component inference.
- `Topology.add_bonds()` does not preserve the complete optional bond metadata
  supported by `MolSysBuilder.add_bond()`.
- Native-to-MDTraj, native-to-OpenMM, and ParmEd conversion paths inspected in
  this audit discard some bond order/type information.
- The normative description calls a component covalently connected but also
  uses metal coordination as an example that joins components. That is a
  conceptual contradiction to resolve.
- `formal_charge` currently lives in `MolecularMechanics` together with
  `partial_charge`, although formal charge is normally part of chemical
  identity and partial charge normally belongs to a model or calculation.

These gaps are reasons for staged validation. They must not be hidden by a more
ambitious object model.

## Attribute semantics

### Global vocabulary

Every public information item should have one canonical attribute name in the
global registry. Synonyms may support user language, but dispatch, dependency
metadata, form declarations, and tests should use the canonical name.

New information domains should extend the registry rather than building a
parallel capability mechanism. Likely future classifications include
interaction attributes and chemical-state attributes, but their exact registry
representation is an implementation decision.

### Attribute domain and cardinality

The registry must eventually describe more than a broad topological,
structural, or mechanical category. New attributes may run over different
domains:

- atoms, groups, bonds, components, molecules, chains, or entities;
- structures;
- an element-by-structure product;
- interactions, participants, or interaction occurrences;
- chemical states, transitions, or state-by-element products.

Before adding a public attribute, its contract should identify:

- canonical name and stable scientific meaning;
- element domain and structure dependence;
- expected shape or cardinality;
- dtype, nullability, and units;
- dependencies on other attributes;
- whether it is intrinsic, imported, inferred, or calculated;
- valid element scopes for `get()` and `set()`;
- extraction, merge, and serialization behavior.

This metadata extends the attribute vocabulary; it is not a replacement
capability system or a renamed coverage layer.

### Form capability versus instance availability

Two queries have different purposes:

- `msm.form.has_attribute(form, attribute)` asks whether the form's public
  adapter contract can deliver the attribute by design, directly or through an
  explicitly supported pipe.
- `msm.has_attribute(item, attribute)` asks whether the concrete molecular
  system can currently deliver a meaningful value.

The first is schema/capability metadata. The second is data availability. An
adapter declaration is not proof of correct delivery; executable tests remain
required.

If MolSysMT later needs to distinguish native storage from delivery through a
conversion pipe, that distinction must receive explicit metadata. It must not
change the meaning of the existing boolean silently.

Attribute introspection also needs a cost and side-effect contract. In
particular, the design must decide whether an instance query may open a file,
scan a trajectory, traverse a conversion pipe, or infer a value. The preferred
default is that `has_attribute()` reports availability without an expensive
scientific computation or silent inference. Expensive discovery should be
explicit, cacheable, and diagnosable.

Three concepts may be needed internally even if they do not become three
public functions:

- the form schema supports the attribute;
- the public adapter can deliver it through an accepted route;
- this instance currently contains or can cheaply expose a meaningful value.

The existing public booleans must retain one documented meaning. Additional
metadata should carry any finer distinction.

### Absent, unknown, partially known, and empty

These states should be expressed through the attribute representation rather
than through a new `coverage` layer:

| State | Example meaning | Candidate representation |
|---|---|---|
| Absent | An XTC contains no bond information | attribute unavailable / storage `None` |
| Unknown value | A bond exists but its order is not known | nullable value such as `NA` |
| Partially known | Some bond orders are known and others are not | array or column containing values and `NA` |
| Known empty | A monoatomic ion is known to have zero covalent bonds | present empty bond collection |
| Not evaluated | No hydrogen-bond analysis was run | no corresponding interaction dataset |
| Evaluated empty | The analysis ran and found no hydrogen bonds | present interaction dataset with zero occurrences |

The exact native representation must be decided and tested. In particular,
changing `Topology.bonds` from an always-present table to an optional value has
broad compatibility consequences and must not be done incidentally.

### Operation requirements

Operations should declare requirements in terms of attributes. Examples are:

- distances require coordinates and optionally a box for PBC;
- a bond graph requires deliverable bonded-atom pairs;
- a hydrogen-bond method requires geometry plus the chemical attributes needed
  by that method;
- an OpenMM execution path requires the topology, structures, and mechanical
  attributes used by the selected construction path;
- chemical-state assignment requires structures plus an explicit perception
  method or suitable electronic descriptors.

When required attributes are unavailable, an operation should either use a
documented derivation policy, request a complementary form, or fail with a
catalog-driven actionable diagnostic. It must not silently invent source data.

## Proposed molecular-system information domains

```text
Molecular-system information domains
|-- Topology
|   |-- stable atom inventory and semantic organization
|   `-- ChemicalStates     optional nested chemical graphs
|-- Structures
|-- MolecularMechanics
`-- Interactions           optional future domain
```

This diagram groups attributes by responsibility. Native `MolSys` currently
integrates topology, structures, and mechanics, but the current topology stores
one bond table directly and does not implement the nested chemical-state model.
It does not yet contain `Interactions`. A topology may legitimately contain no
chemical state, so the nested collection must not become a mandatory populated
object for sequence-only or otherwise incomplete representations.

### Topology

`Topology` is proposed as an umbrella with two responsibilities.

Its stable core owns:

- the atom index space, IDs, names, and `atom_type`;
- nuclear identity such as isotope when explicitly supplied;
- group, molecule, entity, and chain organization;
- semantic labels imported from source forms.

`atom_type` remains the memorable counterpart of `group_type`,
`molecule_type`, and related attributes. In the native chemical contract it
must represent elemental or explicitly supported pseudo-atom identity, never a
force-field type. `atom_ff_type` remains mechanical. Element symbol and atomic
number should be cheap derived attributes when `atom_type` is unambiguous;
inference from `atom_name` is a fallible explicit fallback, not exact source
preservation.

Nested chemical states own covalent graphs and electronic assignments over the
stable atom index space. For a conventional `MolSys`, one reference state may
apply to every structure. A topology can still be explicitly edited, but
geometry must not silently add or remove a bond or change a chemical assignment.
Inference from geometry is an explicit operation with evidence and provenance.

This nesting preserves the established and useful `Topology` name: the object
still contains the system's non-geometric topological descriptions rather than
becoming only an identity table. It also avoids making chemical states a peer
domain disconnected from the atoms they reference.

The nesting is a provisional ownership boundary, not an irreversible claim.
If multi-state experience shows that chemical states require an independent
lifecycle, they may move out of `Topology` in a future major design. If the
remaining stable core then no longer matches community expectations for the
word topology, it may be renamed, for example to a carefully reviewed
`TopologicalScaffold` or another accepted term. No rename should occur merely
for novelty, and compatibility cost must be measured first.

### Structures

`Structures` owns frame-indexed structural information:

- coordinates;
- velocities;
- box vectors;
- time and structure labels;
- frame-level thermodynamic observables already in its contract;
- atom-by-structure observations such as B factors or alternate locations when
  supported by the representation.

Irregular sparse relations must not be forced into dense structural tensors
merely because they depend on `structure_index`.

### Molecular mechanics

`MolecularMechanics` describes a model used to evaluate or simulate the
system. It may include:

- force-field identity and configuration;
- partial charges and force-field atom types;
- non-bonded settings;
- constraints;
- future explicit bonded terms and parameter tables.

Chemical bond metadata and mechanical bond terms are different. Equilibrium
lengths, force constants, functional forms, GROMACS function identifiers, and
OpenMM force terms must not be stored as chemical bond types.

The architecture should allow this domain to be absent. A future design may
also need more than one parameterization for the same topology. That extension
is not part of the first bond-contract implementation.

### Interactions

`Interactions` is proposed as a first-class form or native information domain
for non-covalent and coordination relationships. Candidate use cases include:

- hydrogen bonds;
- salt bridges;
- metal coordination;
- receptor-ligand contacts;
- aromatic stacking;
- cation-pi and halogen interactions;
- water-mediated interactions;
- declarations imported from sources such as mmCIF `struct_conn`;
- interaction fingerprints and pose-comparison inputs.

An interaction may be declared by a source, observed by a geometric method, or
both. Those facts must remain distinguishable.

The conceptual data model has three parts:

1. **Definition:** interaction kind, directionality, source, method, and method
   parameters.
2. **Participants:** one or more referenced atoms, groups, or other supported
   elements, each with an optional role such as donor, hydrogen, acceptor,
   metal, coordinating atom, cation, or aromatic group.
3. **Occurrences:** the structures or structure intervals where the interaction
   is observed, with optional distance, angle, score, energy, confidence, and
   periodic-image information.

A pair-only schema is insufficient. Hydrogen bonds may use three participants,
aromatic interactions use atom groups, water mediation uses multiple chemical
units, and metal coordination may have variable arity.

`Interactions` should normally be returned as an independent result. An
explicit attach operation may later add one or more named interaction datasets
to `MolSys`. Attachment must not make interactions mandatory, authoritative, or
silently current after source data changes.

Large trajectory results must be sparse and chunk-compatible. Repeating a full
interaction record for every frame is not acceptable when definitions and
contiguous occurrence intervals can be stored separately.

#### Structural and temporal scope

An occurrence must reference structures unambiguously. `structure_index` is the
native positional reference within one structures object, while time and
`structure_id` are attributes and need not provide a unique join key. The
design must cover:

- arbitrary and reordered structure subsets;
- non-contiguous occurrences and interval compression;
- appending structures after an analysis;
- analyses between trajectories with different frame counts or sampling times;
- an explicit alignment rule for interactions between two molecular systems;
- PBC image identity when an interaction crosses a unit-cell boundary;
- crystallographic symmetry mates and biological-assembly operators;
- source declarations whose structural scope is unknown.

An interaction with a periodic or symmetry-generated participant cannot be
reduced safely to two base atom indices without preserving the transformation
that identifies the observed copy.

Cross-system interactions are especially relevant to receptor-ligand workflows.
They require either a declared shared index space or participant references that
include the source system. Implicitly assuming that frame `i` in two systems
represents the same time is not acceptable.

### Chemical states

Chemical states are proposed as optional children of `Topology`, not as an
alternative spelling of `Interactions`. Each state describes a chemical graph
and compatible electronic assignments over the topology's stable atom index
space.

One state may own:

- covalent bond endpoints, formal orders, aromaticity, kind, conjugation, and
  stereochemistry;
- atom-level formal charge, radical or unpaired-electron state, aromaticity,
  stereochemistry, protonation, and implicit-hydrogen semantics;
- total formal charge or spin multiplicity when declared even if atom-level
  assignments are incomplete;
- a state-local covalent-component partition;
- connectivity and assignment status distinguishing unavailable, partial,
  complete, known-empty, explicit, inferred, and unknown information.

Formal charge is chemical-state information, not a force-field charge.
`partial_charge` and `atom_ff_type` remain in `MolecularMechanics`. Isotope and
elemental identity remain in the stable topology core because changing nuclear
identity is not an ordinary chemical-state transition.

A topology may contain zero states, one automatically selected reference state,
or multiple states. If multiple states exist, an explicit reference is required
before convenience access can resolve state-dependent attributes. The ordinary
attribute API should remain simple for zero-or-one-state systems. Direct
conveniences such as `Topology.bonds` or `Topology.components` may resolve the
reference state, but they must never duplicate the authoritative tables.

Structure-to-state assignment belongs to `MolSys` composition rather than to
coordinates or the stable topology core. One state may apply to many structures,
a structure may have no known assignment, and uncertain or probabilistic
assignment remains a later contract.

Native selection must resolve the same state boundary. Grammar using stable
attributes such as atom, group, molecule, chain, or entity labels remains
state-independent. Grammar using components, bonds, formal charge, aromaticity,
or expressions such as `bonded to` is state-dependent. With one reference state
the current concise syntax should continue to work; with multiple states the
selector must receive or resolve an explicit state and reject unresolved
ambiguity rather than combining graphs silently. Selection results continue to
use stable topology atom indices.

Additional state dimensions may include tautomer identity, proton location,
spin multiplicity, electronic state, and changes in a QM/MM region or active
Hamiltonian. Their inclusion requires evidence; the initial schema must not
assume that bond edits and formal charges exhaust chemical-state identity.

A reactive trajectory should not require copying a full topology for every
frame. A likely representation is one stable topology core, unique chemical
states or overlays, and a structure-to-state mapping. The first implementation
should validate the boundary using zero or one state; efficient multiple-state
storage and reactive assignment require a separate scientific-validation phase.

Continuous electronic observables such as Wiberg bond orders, atomic
populations, spin densities, or time-dependent partial charges are evidence for
state assignment, not automatically discrete topology. They may eventually
require another specialized representation. The first `ChemicalStates` design
must not erase that distinction.

State assignment may be unknown, ambiguous, or probabilistic. The data model
should not force every structure into exactly one confidently known state. A
future implementation must compare hard assignment, unassigned transition
regions, and probability or confidence distributions before choosing its stable
contract.

## Chemical bond contract

### Findings from external object models

The audit compared the semantics exposed by MDTraj, OpenMM Topology, RDKit,
OpenFF, MDAnalysis, ParmEd, and mmCIF:

- MDTraj and OpenMM Topology expose endpoints plus a compact type/order model.
- RDKit separates a rich qualitative bond type from aromaticity, conjugation,
  direction, and stereochemistry.
- OpenFF separates integer formal order, aromaticity, fractional order, and
  stereochemistry.
- MDAnalysis can preserve type, order, and whether a connection was guessed.
- ParmEd demonstrates why chemical classification and force-field bond
  parameters must be separate.
- mmCIF separates chemical-component bond attributes from broader structural
  connections such as metal coordination.

These systems are evidence for interoperability requirements, not templates to
copy. Their current APIs and supported semantics must be rechecked when each
adapter is implemented.

The verification must also include resonance and valence-sensitive examples.
Formal bond order is representation-dependent in some resonance systems, and
aromaticity models can disagree while representing equivalent chemistry. A
round trip therefore needs both exact-field tests and chemically equivalent
tests with a documented equivalence policy. Exact equality must not be demanded
where the target model canonicalizes an equivalent resonance form, but such a
change must not be hidden as ordinary exact preservation.

### Agreed semantic separation

Native bonds should be able to distinguish at least these concepts:

- endpoint atom indices;
- formal bond order;
- aromaticity;
- fractional or partial bond order when supplied by a calculation;
- chemical bond kind, including an explicit unknown state;
- conjugation when available;
- stereochemistry when available;
- whether the value was explicit or inferred;
- source-specific metadata needed for a faithful round trip.

Exact columns, dtypes, nullability, and vocabularies remain to be designed. The
following invalid conflations must be removed:

- storing `"aromatic"` as a numeric bond order;
- storing `"dative"` as a numeric bond order;
- treating a mechanical bond parameter type as a chemical bond kind;
- assuming an unknown order is a single bond;
- allowing coordination, hydrogen bonds, or generic contacts to join covalent
  components automatically.

### Components, molecules, and labels

A component remains a covalently connected atom set and therefore belongs to a
chemical state. `component_index` is local to that state and may change when a
bond forms or breaks. Only bond kinds explicitly admitted by the final
covalent-connectivity policy may participate in component inference.
Coordination and observed non-covalent relationships do not participate.

Component membership is logically derived from the state graph and may be
cached only with deterministic invalidation. Source-declared component
membership may be preserved with evidence even when connectivity is partial,
but a connected subset observed in a partial graph must not be advertised as a
complete component partition. Using molecules as components is an explicit,
recorded assumption, never a silent fallback.

Molecule and component are orthogonal. A covalent adduct may be one component
while retaining two semantic molecule labels, such as a protein and a covalent
drug. A metal coordinated to a protein remains a separate covalent component
unless an actual covalent bond is represented.

`atom_id`, `group_id`, and other `*_id` values are labels, not primary keys.
They are strings in native objects and may repeat. Internal indices define row
identity, membership, selection, and remapping. A converter must not renumber a
source label merely to make it unique.

### No `Topology.connections`

A unified topology-connections table was considered and rejected because it
would either make geometry-dependent relationships appear invariant or require
`structure_index` inside `Topology`. It would also create ambiguous component
semantics and duplicate interaction-analysis modules.

Source-declared covalent bonds map to a topology chemical state.
Source-declared coordination or other non-covalent relationships map to an
interaction dataset with explicit source and structural scope.

## Provenance and reproducibility

Provenance answers where information came from; it does not answer whether an
attribute exists. Examples include:

- bonded atom pairs read from an OpenMM Topology;
- bond orders imported from an RDKit molecule;
- coordination declared by an mmCIF category;
- partial charges assigned by a named charge method;
- hydrogen bonds computed with a named geometric definition and thresholds.

Provenance is not currently another molecular-system layer beside topology,
structures, mechanics, or interactions. It is optional cross-cutting metadata
attached to the block, column, or derived dataset whose origin it explains. A
mandatory public `MolSys.Provenance` object is not part of the first chemical-
state vertical.

The initial provenance design should operate at data-block, column, or derived
dataset granularity rather than attaching a record to every scalar. At minimum,
derived results should preserve:

- source molecular forms or source artifact identity where available;
- producing operation and method;
- scientifically relevant parameters and units;
- selected atom and structure scopes;
- software version or algorithm version when needed for reproducibility;
- topology and structures revisions or equivalent fingerprints when the result
  can become stale.

Provenance records should distinguish:

- original source identity;
- transformations and conversion steps;
- producing scientific method;
- method parameters and units;
- software and algorithm version;
- validation or curation decisions.

A compact evidence value such as `explicit`, `inferred`, `user_defined`, or
`unknown` may vary per bond or assignment. It is not a substitute for a
provenance record containing the producing source, method, version, and
parameters. Evidence may reference shared provenance rather than repeating a
large metadata object in every row.

Persistence must not copy credentials, tokens, private query strings, or
developer-machine absolute paths into portable artifacts. Source identity may
use a sanitized URI, logical identifier, content hash, or user-approved path.
Granularity should remain proportional: column- or dataset-level provenance is
the default, with per-value evidence reserved for cases that scientifically
require it.

Provenance should be accessible without pretending that it is an intrinsic
molecular property. Whether it appears in the global attribute registry, a
metadata API, or both remains open.

## Staleness and consistency

Derived information can become invalid:

- changing coordinates can invalidate observed interactions and state
  assignments;
- changing topology can invalidate interactions, chemical states, and molecular
  mechanics;
- extracting atoms or structures requires participant and occurrence remapping;
- merging systems may create ambiguous external references;
- appending structures must not imply that existing interaction analyses cover
  the new structures.

The design must choose one or more explicit policies:

- immutable result snapshots tied to source fingerprints;
- revision counters with stale-result detection;
- explicit invalidation when attached data is affected;
- recomputation only when the user requests it.

Silent recomputation and silently stale attached results are both unacceptable.
SMonitor diagnostics should report incompatibility or staleness at public
boundaries, while normal successful access remains quiet.

## Representative scenarios

### Sequence-only representation

A sequence provides group identity and order but no coordinates, explicit atoms,
or mechanics. Operations requiring unavailable attributes must request another
form or a documented construction step.

### Topology plus coordinate trajectory

A topology form supplies stable identity plus a reference chemical state with
bonds; XTC or DCD supplies coordinates, time, and box. Form composition exposes
their union without requiring the file formats themselves to contain the
missing information.

### Parameterized classical MD system

The stable topology core and one reference chemical state apply to all frames,
`Structures` contains those frames, and `MolecularMechanics` contains the active
energetic model for that state. Multiple interaction analyses may be calculated
without becoming part of topology.

### Docking and ligand-series analysis

Structures represent poses. Named interaction datasets can represent receptor-
ligand contacts, hydrogen bonds, coordination, and water mediation for each
pose. Sparse occurrences and reproducible method parameters support pose
ranking, interaction fingerprints, and comparison across a ligand series.

### PharmacophoreMT integration

PharmacophoreMT can consume chemical attributes, structures, and interaction
datasets without requiring MolSysMT to own the complete pharmacophore model.
Pharmacophore features, tolerances, exclusion volumes, and feature-level
constraints remain responsibilities of PharmacophoreMT.

### Covalent-drug and reactive QM/MM trajectory

Interactions describe pre-reactive geometry and environmental stabilization.
Continuous electronic observables describe evolving electronic structure.
Chemical states describe the discrete non-covalent complex, transition region,
and covalent adduct when a scientifically declared perception method supports
that assignment.

The mechanical graph, perceived chemical graph, and interaction graph may
differ. The data model must preserve those differences.

### Heterogeneous models

Models with different atom counts, mutations, or explicit proton inventories do
not fit one dense `Structures` tensor. The initial supported representation
should remain separate `MolSys` objects or a collection of systems. A future
heterogeneous ensemble must not be smuggled into `ChemicalStates` without a
separate contract.

## Relationship to the wider ecosystem

Several libraries contain important parts of this architecture:

- MDAnalysis combines topology and trajectory and supports auxiliary
  time-series data.
- OpenMM separates chemical topology, executable system, context, and state.
- OpenFF separates chemical topology from force-field parameter collections.
- Biotite provides efficient atom-array stacks with optional bond lists.
- ASE combines optional atomistic properties with attachable calculators.
- RDKit provides rich molecular graph semantics.

The proposed distinction is the integration of these concerns through one
form-independent attribute vocabulary, complementary forms, and universal
operations. This is a strategic opportunity, not yet a validated claim of
complete or unique implementation. Public novelty claims require a separate,
dated landscape review.

## Alternatives considered

### Keep only the current three native domains

This minimizes implementation work but leaves interaction results as ad hoc
arrays and provides no coherent route for declared coordination, reproducible
interaction datasets, or reactive chemical states.

### Add `Topology.connections`

This is simple for static imports but creates ambiguity between invariant
chemistry and geometry-dependent observations. It was rejected.

### Store interactions inside `Structures`

This aligns them with frames but mixes irregular sparse relations with dense
numeric tensors and makes higher-arity participants awkward. It was rejected.

### Always attach `Interactions` to `MolSys`

This is convenient but risks mandatory memory cost, stale state, conversion
complexity, and the false impression that one analysis is authoritative. The
preferred direction is an independent result with explicit optional attachment.

### Compute interactions only on demand and never persist them

This avoids staleness but prevents reproducible comparison, sharing, incremental
analysis, and downstream pharmacophore or drug-design workflows. It was
rejected as the only mode, although on-demand computation remains the default.

### Store reactive covalent changes as interactions

This avoids a new object but loses the consequences for bond order, formal
charge, components, and chemical identity. It was rejected.

### Use one topology per frame

This is explicit but prohibitively redundant for long trajectories and obscures
repeated chemical states. It may be an interchange fallback, not the preferred
native model.

### Keep chemical states as a peer of topology

This gives states an independent lifecycle but disconnects each graph from the
stable atom index space it necessarily references and weakens the conventional
meaning of topology. Nesting is the preferred first boundary. Extraction to a
peer domain remains a future major-design escape hatch if real multi-state use
shows that independent ownership is more coherent.

### Rename topology immediately

Renaming the stable portion to `MolecularIdentity`, `MolecularInventory`, or
`TopologicalScaffold` could make a strict identity/chemistry separation more
explicit, but it would impose broad compatibility and teaching cost before the
multi-state model has implementation evidence. `Topology` remains the umbrella
name for now. A later rename is permitted only with evidence, an accepted term,
and a major-version migration plan.

### Introduce a generic unrestricted property bag

This maximizes extensibility but weakens units, semantics, validation, dispatch,
and conversion fidelity. Specialized domains must extend the canonical
attribute vocabulary instead.

## Recommended version 1.0 boundary

The final release decision remains open, but the recommended boundary is
deliberately narrower than the complete vision.

### Recommended before 1.0

- make Tier 1 attribute declarations and public delivery truthful;
- document form capability, instance availability, null, and known-empty
  semantics;
- define the minimum nested chemical-state boundary and reference-state
  behavior, efficiently supporting zero or one state;
- define the minimum native chemical graph and bond contract inside that state;
- separate formal bond order, aromaticity, fractional order, and bond kind;
- make covalent components state-local and resolve their participation and the
  metal-coordination contradiction;
- move formal charge conceptually into chemical state while preserving a read
  migration path from old mechanical payloads;
- preserve the accepted minimum bond semantics through priority native and
  third-party conversion routes;
- version affected persistence schemas and expose deterministic conversion
  losses.

### Recommended after 1.0

- stable public `Interactions` API;
- attaching interaction datasets to `MolSys`;
- persisted interaction networks and fingerprints;
- a formal PharmacophoreMT handoff contract;
- efficient multi-state storage, topology timelines, uncertain assignments,
  and reactive-trajectory support;
- dynamic electronic-property support;
- multiple simultaneous mechanics parameterizations inside one native object.

A small experimental interaction result may be developed before 1.0 to test the
architecture, but it should not become a release blocker or a stable public
contract without its own approval.

## Implementation program

Each phase requires a separate maintainer decision. Later phases do not block
earlier consolidation unless their invariants reveal a contract conflict.

### Phase 0: accept the architecture and boundaries

1. Review this proposal and record accepted, amended, or rejected decisions.
2. Decide the version 1.0 boundary.
3. Accept, amend, or reject nested chemical states, reference-state behavior,
   and the future extraction/rename escape hatch.
4. Reconcile the normative component definition and the metal-coordination
   example.
5. Mark narrower proposals as subordinate or superseded where their assumptions
   conflict with the accepted bond contract.

**Deliverable:** an accepted decision record and an explicit 1.0 scope.

**Gate:** do not change schemas until the component definition, form/instance
attribute semantics, and migration responsibilities have an owner and decision.

### Phase 1: make attribute claims truthful

1. Audit global attributes, form declarations, public getters, and instance
   `has_attribute()` behavior.
2. Define the exact meanings of form capability, instance availability,
   nullable values, and known-empty collections.
3. Add delivery tests for every Tier 1 declared attribute.
4. Ensure an attribute declaration does not become evidence merely because a
   converter returns an object.
5. Add catalog-driven diagnostics for required but unavailable attributes.

**Deliverable:** a machine-readable audit in which every Tier 1 declaration
points to a public delivery test or an explicit supported derivation.

**Gate:** do not use new interaction or chemical-state booleans until the
existing capability and instance-availability semantics pass this audit.

### Phase 2: consolidate the reference chemical-state contract

1. Approve the zero/one-state container, explicit reference-state behavior, and
   convenience access without duplicate authority.
2. Approve exact atom-chemistry and bond attributes, dtypes, nullability,
   vocabularies, and component-participation rules.
3. Move formal charge into chemical state while retaining a compatibility path
   for old mechanical payloads.
4. Update native tables, builder operations, extraction, merge, removal,
   sorting, copying, and rebuild logic, including state-local components.
5. Make native selection and `bonded to`/component predicates resolve the
   reference state and define explicit multi-state ambiguity diagnostics.
6. Version H5MSM, MolSysDict, YAML, and other affected serialization
   schemas where required.
7. Implement adapters incrementally, beginning with native, OpenMM Topology,
   MDTraj, RDKit/OpenFF, MDAnalysis, ParmEd, and mmCIF based on representable
   semantics.
8. Emit or return an explicit loss report for non-representable target fields
   according to the accepted conversion policy.

**Deliverable:** one versioned reference chemical-state schema nested under
topology, native lifecycle operations, persistence, and at least two independent
external semantic round-trip fixtures.

**Gate:** do not migrate the complete adapter matrix until native, H5MSM or the
selected canonical persistence form, and the first two external forms pass the
same conversion-truth fixtures. A failed schema prototype must be revised before
fan-out.

### Phase 3: prototype `Interactions`

1. Define canonical interaction attributes and the smallest participant model
   that supports pairs, hydrogen-bond triples, and grouped aromatic features.
2. Represent source declarations separately from observed occurrences.
3. Prototype sparse occurrence storage and chunked trajectory production.
4. Keep the result independent from `MolSys` initially.
5. Implement extraction and structure slicing before optional attachment.
6. Validate one narrow vertical slice: hydrogen bonds or metal coordination,
   not every interaction kind at once.

**Deliverable:** an independent experimental result form supporting definition,
participants, occurrences, extraction, and one independently validated
interaction kind.

**Gate:** do not attach the result to `MolSys` or promise persistence until
participant remapping, structural scope, PBC/symmetry semantics, and stale-source
behavior are demonstrated.

### Phase 4: persistence and optional attachment

1. Define a versioned serialization schema.
2. Define topology/structure revision or fingerprint semantics.
3. Add explicit attach, detach, stale-check, and named-dataset operations if
   evidence supports attachment.
4. Preserve not-evaluated versus evaluated-empty semantics.
5. Validate old-file compatibility and unknown-version diagnostics.

**Deliverable:** a versioned schema plus explicit attach/detach semantics backed
by old/new golden fixtures.

**Gate:** attachment remains experimental if mutation can leave a silently stale
or dangling dataset.

### Phase 5: drug-design interoperability

1. Add receptor-ligand and metal-coordination fixtures.
2. Compare interaction fingerprints across poses and structures.
3. Define a stable handoff contract with PharmacophoreMT without importing it
   as a hard dependency or duplicating its feature model.
4. Evaluate water-mediated and higher-arity interaction representation.
5. Benchmark sparse storage and chunked analysis on realistic pose ensembles
   and trajectories.

**Deliverable:** a validated receptor-ligand vertical slice and a reviewed
cross-package handoff record.

**Gate:** do not move pharmacophore-specific features into MolSysMT merely to
make the integration easier; shared concepts must first qualify as stable
MolSysMT attributes.

### Phase 6: multi-state reactive chemistry research

1. Select representative reactive and covalent-drug datasets with legally and
   scientifically usable references.
2. Separate raw electronic observables from discrete chemical perception.
3. Extend the validated reference-state boundary with unique state overlays and
   structure-to-state assignments.
4. Validate component and formal-charge behavior across states.
5. Compare epoch segmentation, state overlays, and event-log alternatives.
6. Do not expose a stable public API until scientific validation and extraction
   semantics are demonstrated.

**Deliverable:** a research report comparing epoch segmentation, state overlays,
event logs, and uncertain assignments on at least one representative reactive
dataset.

**Gate:** no stable API until atom mapping, state uncertainty, component changes,
serialization, and independent scientific validation are all resolved.

## Verification matrix

### Composite-form compatibility

- Atom counts, order, and explicit mappings are validated before attributes are
  combined.
- Conflicting values from two forms follow an explicit source-selection,
  precedence, comparison, or multi-interpretation policy.
- Topology and mechanics cannot be paired when their particle or atom index
  spaces are incompatible.
- Structure-dependent forms define frame and time alignment rather than joining
  on coincident positional indices implicitly.
- Unit-compatible duplicate values are compared after canonical conversion.
- Strict mode rejects unresolved conflicts and reports both candidate sources.
- Permissive behavior, if supported, returns a structured loss or conflict
  report rather than silently choosing.

### Attribute truth

- Form declarations agree with public delivery for every documented element
  scope.
- Instance-aware checks distinguish unavailable values from present nullable
  values.
- Known-empty collections remain available and report zero elements.
- A composite molecular system resolves each requested attribute from a
  deterministic source.
- Derived attributes identify their dependencies and do not hide unavailable
  source evidence.

### Bond science and interoperability

- Single, double, triple, aromatic, unknown-order, and dative examples preserve
  every target-representable semantic field.
- Formal and fractional bond order are never silently interchanged.
- Aromaticity is independent of numeric order.
- Coordination does not join covalent components.
- Duplicate string IDs survive native round trips and compatible external
  round trips without invented renumbering.
- Conversion tests compare target semantics, not only object construction.
- Losses are explicit and deterministic.
- Isotopes, formal charges, radicals, atomic aromaticity, atom chirality, and
  explicit hydrogen semantics are inventoried for every claimed chemically
  faithful route.
- Resonance and aromatic canonicalization tests distinguish exact preservation
  from documented chemical equivalence.
- Malformed valence, dangling endpoints, self-bonds, and duplicate-edge policy
  have explicit validation outcomes.

### Native transformations

- Atom extraction remaps bonds, interaction participants, mechanics, and state
  overlays consistently.
- Structure extraction remaps interaction occurrences and state assignments.
- Merge behavior is defined for duplicate labels and independent internal
  indices.
- Removing atoms or structures cannot leave dangling references.
- Appending structures does not falsely extend the scope of prior analyses.
- Property-based tests generate valid subsets and verify that remapped references
  preserve graph invariants.
- `set()`, removal, merge, structure concatenation, and topology rebuild either
  preserve attached-data compatibility or invalidate it explicitly.

### Interaction science

- Declared and observed interactions remain distinguishable.
- Directional and higher-arity participant roles round-trip.
- Distances use nm internally; angles use the established radians convention;
  public quantities use PyUnitWizard.
- PBC and periodic-image choices are reproducible.
- Different methods or thresholds can coexist as named datasets.
- Empty evaluated results differ from absent analysis.
- Results match an independent implementation or analytical fixture for each
  accepted interaction kind.
- Non-contiguous and reordered structure selections retain the correct
  occurrences.
- Cross-system analyses require explicit atom and time/frame alignment.
- PBC-crossing, crystallographic-symmetry, and biological-assembly examples
  preserve the transformation identifying each observed participant.
- Negative fixtures cover invalid roles, wrong arity, dangling participants,
  incompatible structure scopes, and malformed units.

### Reactive states

- Repeated states are stored once and reused by structure mappings.
- Bond and charge changes reproduce the expected component partitions.
- Continuous electronic descriptors remain accessible without forced
  discretization.
- Ambiguous transition structures need not be assigned falsely to a state.
- Extraction and serialization preserve state identity and transition order.
- Hard, unassigned, and probabilistic state assignments are compared before a
  stable representation is selected.
- Tautomer, proton-location, spin, and QM/MM-region changes are either
  represented explicitly or declared outside the accepted state contract.
- A trajectory whose atom inventory changes is rejected or segmented according
  to a documented policy.

### Performance and scale

- Interaction analysis uses `ChunkedExecutor` for large trajectories.
- Sparse results do not allocate a dense atom-pair-by-frame tensor by default.
- Benchmarks record dataset, environment, versions, warm-up policy, statistic,
  and date or commit.
- No proposed layer adds a soft dependency to import-time startup.
- Supported Python versions are 3.11, 3.12, and 3.13.
- Each accepted interaction representation has a measured memory budget per
  definition, participant, and occurrence.
- Cache and revision behavior is deterministic under concurrent read-only use;
  mutation is either synchronized or documented as unsupported.
- Attribute introspection benchmarks distinguish metadata-only checks from file
  opening, scanning, conversion, or scientific computation.

### Persistence and migration

- Every schema version has minimal, complete, nullable, known-empty, and
  malformed golden fixtures.
- Old fixtures remain readable for the promised compatibility window.
- Unknown future versions fail with an actionable diagnostic.
- Portable provenance excludes secrets and unintended machine-local paths.
- Round trips preserve attribute availability semantics, not only non-null
  values.
- Migration is idempotent or explicitly one-way and records the source schema
  version.

### Lifecycle integrity

For every accepted public API slice:

- NumPy-style docstrings and doctests are complete;
- Foundations, Toolbox, and Cookbook material reflects the behavior;
- all corresponding Four Paths modules are reviewed and updated;
- serialization and migration behavior is documented;
- SMonitor catalog diagnostics cover invalid or stale states;
- ArgDigest validates public arguments;
- optional dependencies remain lazy under DepDigest;
- Ruff and the developer-guide validator pass.

## Risks and controls

### Architectural breadth

Risk: the proposal becomes a multi-year rewrite.

Control: implement narrow vertical slices. Bond consolidation, one interaction
kind, and reactive-state research are separate decisions.

### Attribute explosion

Risk: every external field becomes a public attribute.

Control: add attributes only for stable scientific concepts used across forms.
Keep source-specific round-trip metadata namespaced until a general concept is
demonstrated.

### False capability claims

Risk: new booleans advertise attributes that are not actually deliverable.

Control: require public delivery tests and instance-aware fixtures before Tier 1
claims.

### Stale derived information

Risk: attached interactions or states disagree with modified source data.

Control: immutable result snapshots or explicit revision checks; never silent
refresh.

### Persistence lock-in

Risk: an early schema freezes an inadequate participant or state model.

Control: prototype in memory, version the first persisted schema, and reject
unknown future versions explicitly.

### Scientific overclaiming

Risk: geometric criteria are presented as chemical truth.

Control: preserve method, parameters, evidence kind, and uncertainty; require
independent scientific validation.

### Core-object weight

Risk: optional analyses make common topology/trajectory workflows heavier.

Control: independent lazy result objects, sparse storage, and optional
attachment. Measure before embedding.

### Composite-source ambiguity

Risk: complementary forms expose conflicting attributes or incompatible index
spaces and dispatch silently chooses one.

Control: validate compatibility before composition, require deterministic
source resolution, and expose conflicts through structured reports and strict
failure modes.

### Introspection cost

Risk: `has_attribute()` unexpectedly opens large files, performs conversion, or
runs scientific inference.

Control: keep the default query metadata-driven and cheap; make expensive
discovery explicit and measurable.

## Open decisions requiring evidence

1. What compatibility and precedence policy governs complementary forms that
   deliver the same attribute?
2. How should MolSysMT represent explicit atom and frame mappings between forms
   with different index spaces?
3. Which attribute-registry fields are required to express domain,
   cardinality, structure dependence, units, nullability, and derivation?
4. May instance `has_attribute()` open or scan a file, traverse a conversion
   pipe, or infer a value, and how is that cost exposed?
5. What exact zero/one-state container and reference-state rule preserves
   convenient `Topology.bonds` access without creating a second authority?
6. Which exact bond kinds participate in covalent component inference, and how
   should dative bonds be treated?
7. How should formal charge move into chemical state, and how should old
   mechanical serialization migrate without two independent values?
8. Which atom-level chemical attributes are mandatory for a chemically faithful
   graph contract, and which belong to later slices?
9. Which bond stereochemistry representation is sufficient for faithful RDKit,
   OpenFF, and mmCIF round trips, including stereo reference atoms?
10. What constitutes chemical equivalence when resonance or aromaticity
    canonicalization changes an exact representation?
11. What is the minimum structured provenance API after the first evidence
   fields, given that provenance is cross-cutting metadata rather than a peer
   molecular domain?
12. What is the minimum participant representation for aromatic groups,
   water-mediated interactions, and cross-system interactions?
13. Should `Interactions` support references to two independent molecular
   systems, or require an explicit merged index space?
14. How are time alignment, PBC images, symmetry mates, and biological-assembly
    operators represented in interaction occurrences?
15. Which source revision mechanism is stable across copy, extraction,
   serialization, and process boundaries?
16. Can one `MolSys` hold multiple molecular-mechanics parameterizations, or is
   that better represented by complementary forms?
17. Are `ChemicalState` and `chemical_states` the correct public names, and
    should the nested collection later leave `Topology` if its lifecycle becomes
    independent?
18. Does state assignment support probabilities or confidence, or only hard and
    unassigned states?
19. What is the supported representation for reactive trajectories whose atom
    inventory changes?
20. Which slices, if any, are release blockers for 1.0 rather than post-1.0
    architecture?
21. Under what evidence and major-version compatibility plan would the stable
    topology core be renamed if chemical states are extracted in the future?

## Non-goals

- Copying implementation code from third-party libraries.
- Making every external representation lossless.
- Treating all contacts as stored interactions by default.
- Replacing PharmacophoreMT's feature and pharmacophore model.
- Turning `MolSys` into an unrestricted metadata dictionary.
- Implementing a general reactive-chemistry engine as part of bond-table work.
- Storing force-field terms in chemical topology.
- Adding DuckDB, Polars, Arrow, or Rust as a prerequisite for this architecture.
- Supporting Python 3.10.

## Related work

- [Chemical Graph and Conversion Execution Checkpoint](../archive/resolved_proposals/chemical_graph_and_conversion_execution_checkpoint.md)
- [Conversion Fidelity Matrix and MolSysDict Schema Evolution](conversion_fidelity_and_molsysdict_v1.md)
- [Post-1.0 SDF/MOL2 chemical metadata expansion](chemical_metadata_preservation_sdf_mol2.md)
- [Explicit Form Support Registry](../archive/resolved_proposals/explicit_form_support_registry.md)
- [Technical and Scientific Quality Improvement Program](technical_and_scientific_quality_improvement_program.md)
- [Topology Selection Indexing and PyArrow](topology_selection_indexing_and_pyarrow.md)
- [Core specification](../CORE_SPECIFICATION.md)
- [Interface contract](../INTERFACES.md)
- [Forms and conversions](../forms_and_conversions.md)
- [Scientific validation](../scientific_validation.md)
- [Scalability](../SCALABILITY.md)

## Completion criteria for this proposal

This proposal can be marked accepted when:

- the executive decisions are reviewed and amended where necessary;
- the version 1.0 boundary is recorded;
- the bond-contract implementation is split into an approved executable plan;
- interaction and reactive-state work remain explicitly staged;
- conflicting pending proposals are marked subordinate or superseded;
- accepted durable rules are moved into normative developer documentation.

It can be marked implemented only after the accepted phases meet their own
tests, scientific validation, conversion-fidelity, persistence, and lifecycle
criteria. Acceptance of the architecture is not implementation evidence.
