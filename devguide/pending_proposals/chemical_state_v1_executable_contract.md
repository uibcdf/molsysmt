# Chemical State v1 Executable Contract

**Status:** accepted and implemented for the fixed pre-1.0 priority scope

**Recorded:** 2026-07-15

## Purpose

This proposal turns the accepted topology and chemical-state architecture into
an executable first-version contract. It defines ownership, allowed fields,
missingness, graph invariants, compatibility behavior, and implementation gates
before native tables or public attributes change.

The contract is deliberately broader than a protein-topology bond list but
smaller than a cheminformatics toolkit. It must represent incomplete molecular
systems, conventional biomolecular topology, small-molecule chemistry,
covalent adducts, and explicitly perceived states without treating force-field
terms or observed interactions as chemical bonds.

## Audit findings driving the design

The current native implementation has four material limitations:

1. `Bonds_DataFrame.order` stores numeric strings and non-numeric concepts such
   as `"aromatic"` and `"dative"`; it therefore has no single scientific type.
2. `Bonds_DataFrame.type` is not protected from confusion with a force-field
   bond parameter type.
3. `formal_charge` is registered and stored as molecular mechanics even though
   RDKit and OpenFF provide it as molecular identity/state information.
4. An empty bond table cannot distinguish unavailable connectivity from a
   complete graph containing zero bonds.

The adapter audit adds these requirements:

- OpenMM and MDTraj can carry optional order and type but do not provide the
  complete small-molecule chemical model.
- RDKit independently exposes formal charge, isotope, atom and bond
  aromaticity, radical electrons, implicit-hydrogen policy, conjugation,
  stereochemistry, stereo reference atoms, and directional bond concepts.
- OpenFF separates formal order, aromaticity, fractional order, and
  stereochemistry.
- MDAnalysis can preserve whether connectivity was guessed.
- ParmEd bond `type` commonly denotes a mechanical parameter object, which
  must remain in molecular mechanics.
- Canonically sorting endpoint indices loses donor-to-acceptor direction unless
  direction is stored separately.

These findings describe semantic requirements. They do not authorize copying
third-party implementations.

## Accepted architectural premises

The following premises are inherited from the master architecture and are not
reopened by this proposal:

- stable atom inventory and semantic hierarchy belong to `Topology`;
- bonds, formal charge, valence-related atom state, and covalent components
  belong to `ChemicalState`;
- molecules remain semantic and stable while components are state-local;
- partial charge and force-field atom/bond types remain in
  `MolecularMechanics`;
- interactions and geometry-dependent contacts do not belong to chemical
  state;
- internal row indices are identity; `*_id` values are string labels and need
  not be unique;
- no generic capability or `coverage` object is introduced.

The completeness values defined below are scientific assertions about a graph,
not a second capability system. Attribute availability remains governed by the
canonical attribute registry and each form instance.

## Container contract

### Topology ownership

`Topology` owns:

- atom identity: `atom_id`, `atom_name`, and `atom_type`;
- stable isotope mass number when explicitly known;
- groups, molecules, chains, and entities;
- an ordered collection of zero, one, or multiple chemical states;
- an optional reference-state index.

`atom_type` continues to mean elemental or explicitly supported pseudoatom
identity. Element symbol and atomic number are derived from an unambiguous
`atom_type`; they are not duplicated in the native table. A source force-field
type must map to `atom_ff_type`, source metadata, or an explicit loss report,
not silently to `atom_type`. Inferring `atom_type` from `atom_name` is an
explicit operation with evidence, never an unreported converter fallback.

The proposed stable atom addition is:

| Field | Pandas dtype | Missing meaning | Semantics |
|---|---|---|---|
| `isotope` | `UInt16` | isotope not specified | isotope mass number, not atomic mass |

For the 1.0 compatibility baseline, the nullable column is part of the fixed
stable atom table even when every value is unknown. Whether post-1.0 native
storage should materialize it only when needed is evaluated in
`optional_native_columns_memory_model.md`; that optimization must preserve the
same logical attribute and missingness contract.

### Chemical-state collection

Chemical states use ordered row identity rather than a dictionary keyed by a
label. Each state has a nullable string `state_id`; labels may repeat, and an
ambiguous label lookup must fail rather than choose the first state.

The topology-level rules are:

- zero states: stable topology exists but chemical state is unavailable;
- one state: that state is the implicit reference state;
- multiple states with an explicit reference index: compatibility facades use
  that state;
- multiple states without a reference: state-dependent facade access raises a
  catalog-backed ambiguity diagnostic;
- setting bonds or invoking a bond mutation on a zero-state topology may create
  one reference state only through a documented mutation operation; a read
  must never create a state as a side effect.

`Topology.bonds`, `Topology.components`, and component-membership convenience
access are direct facades over the resolved reference state. They never copy or
own duplicate data. Reading these facades with zero states fails with an
unavailable-state diagnostic.

### MolSys structure-to-state association

Association between structures and chemical states belongs to `MolSys`, not
`Topology`. The logical representation is a nullable integer array aligned to
structures. A single state may apply implicitly to every structure; multiple
states require explicit association when an operation resolves state through
structure indices.

The accepted physical authority is
`MolSys._structure_chemical_state_indices`. `Structures` must not own a copy.
The canonical public attribute is `structure_chemical_state_index`; like
`structure_id`, it is requested from `element='system'` and filtered through
`structure_indices`. Its values are nullable 0-based indices into the ordered
chemical-state inventory. The public resolver `chemical_state='structure'`
requires the requested structures to map to exactly one known state.

This association does not permit different atom inventories. States involving
different explicit atom counts remain separate `MolSys` objects until a
heterogeneous-ensemble contract exists.

## ChemicalState data contract

A chemical state contains:

- state-level identity and completeness metadata;
- optional aligned atom-state columns;
- a bond table;
- optional component membership and component table;
- compact evidence and references to shared provenance records.

Allowed optional columns are not allocated eagerly. This avoids imposing a
small-molecule metadata cost on large biomolecular systems that only carry
connectivity.

## Canonical attribute policy and complete first-version inventory

Storage fields must not be added ahead of the canonical attribute contract, and
attribute declarations must not be added ahead of public delivery. Each
implementation slice updates storage, the global registry, relevant form
declarations, instance availability, delivery functions, tests, and lifecycle
documentation atomically.

The complete proposed canonical public inventory introduced or reclassified by
this contract is listed below. Names may change only through a recorded contract
amendment before implementation; an implementation must not add an undocumented
near-synonym.

### Stable-topology addition

| Canonical attribute | Domain | Shape per request | Dtype | Nullable | Units |
|---|---|---|---|---:|---|
| `isotope` | atom | one value per returned atom | `UInt16` | yes | dimensionless mass number |

### Chemical-state identity and status

| Canonical attribute | Domain | Shape per request | Dtype | Nullable | Dependencies |
|---|---|---|---|---:|---|
| `chemical_state_index` | chemical state | one index per returned state | `Int64` | no | `n_chemical_states` |
| `chemical_state_id` | chemical state | one label per returned state | `string` | yes | `chemical_state_index` |
| `n_chemical_states` | system | scalar | integer | no | `chemical_state_index` |
| `reference_chemical_state_index` | system | scalar | `Int64` | yes | `chemical_state_index` |
| `connectivity_completeness` | chemical state | one value per returned state | `string` enum | no | resolved chemical state |
| `component_completeness` | chemical state | one value per returned state | `string` enum | no | resolved chemical state |
| `component_evidence` | chemical state | one value per returned state | `string` enum | no | resolved chemical state |

### Structure-to-state association

| Canonical attribute | Domain | Shape per request | Dtype | Nullable | Dependencies |
|---|---|---|---|---:|---|
| `structure_chemical_state_index` | structure | one value per returned structure | `Int64` | yes | `structure_index`, `chemical_state_index` |

`provenance_index` is intentionally absent from this molecular-attribute list.
It is a metadata reference and belongs to the future provenance/metadata API;
making it a molecular property would contradict the accepted provenance
boundary.

### Atom chemical-state attributes

| Canonical attribute | Domain | Shape per request | Dtype | Nullable | Units/dependencies |
|---|---|---|---|---:|---|
| `formal_charge` | atom | one value per returned atom | `Int16` | yes | elementary-charge units; resolved state |
| `atom_is_aromatic` | atom | one value per returned atom | `boolean` | yes | resolved state |
| `n_unpaired_electrons` | atom | one value per returned atom | `UInt8` | yes | resolved state |
| `n_implicit_hydrogens` | atom | one value per returned atom | `UInt8` | yes | resolved state |
| `allows_implicit_hydrogens` | atom | one value per returned atom | `boolean` | yes | resolved state |
| `atom_stereochemistry` | atom | one value per returned atom | `string` enum | yes | resolved state and graph interpretation |

These attributes are directly settable only on atoms in the first version.
`formal_charge` may additionally be requested from `system` as the aligned
per-atom array for compatibility with its existing contract. No automatic
group, molecule, chain, entity, or component aggregation is defined.

The first atom-stereochemistry vocabulary is `R`, `S`, `r`, `s`,
`unspecified`, and `unknown`. It stores semantic descriptors. RDKit traversal
tags such as clockwise/counterclockwise and non-tetrahedral implementation tags
are not silently inserted into this column; an adapter preserves them as
namespaced metadata where possible or reports them as unsupported semantics.

### Bond chemical-state attributes

| Canonical attribute | Domain | Shape per request | Dtype | Nullable | Dependencies |
|---|---|---|---|---:|---|
| `bond_id` | bond | one value per returned bond | `string` | yes | resolved state |
| `bond_order` | bond | one value per returned bond | `UInt8` | yes | resolved state |
| `fractional_bond_order` | bond | one value per returned bond | `Float64` | yes | resolved state |
| `bond_type` | bond | one value per returned bond | `string` enum | yes | resolved state |
| `bond_is_aromatic` | bond | one value per returned bond | `boolean` | yes | resolved state |
| `bond_is_conjugated` | bond | one value per returned bond | `boolean` | yes | resolved state |
| `bond_stereochemistry` | bond | one value per returned bond | `string` enum | yes | stereo reference atoms |
| `bond_stereo_atom_indices` | bond | `(n_bonds, 2)` | `Int64` | yes | bond stereochemistry |
| `bond_donor_atom_index` | bond | one value per returned bond | `Int64` | yes | directional bond semantics |
| `bond_acceptor_atom_index` | bond | one value per returned bond | `Int64` | yes | directional bond semantics |
| `bond_joins_components` | bond | one value per returned bond | `boolean` | yes | component inference policy |
| `bond_evidence` | bond | one value per returned bond | `string` enum | yes | optional provenance record |

Existing canonical connectivity attributes remain and become state-resolved:

- `bond_index`;
- `bonded_atoms`;
- `bonded_atom_pairs`;
- `inner_bond_index`;
- `inner_bonded_atoms`;
- `inner_bonded_atom_pairs`;
- `n_bonds`;
- `n_inner_bonds`.

Existing component attributes also remain and become state-resolved:

- `component_index`;
- `component_id`;
- `component_name`;
- `component_type`;
- `n_components`.

`partial_charge` and `atom_ff_type` remain mechanical. A future mechanical bond
parameter identifier must use a mechanically explicit name such as
`bond_ff_type`; it must not reuse `bond_type`.

### Required registry relationships

The attribute catalog must encode complete relationships rather than relying on
comments or getter behavior:

- all atom-state, bond-state, and component attributes depend on a resolved
  chemical state;
- component attributes additionally depend on meaningful component membership;
- `atom_stereochemistry` depends on the atom state and graph interpretation;
- `bond_stereochemistry` depends on `bond_stereo_atom_indices` when the stereo
  vocabulary requires reference atoms;
- `bonded_atoms`, `bonded_atom_pairs`, and all inner-bond attributes depend on
  bond endpoints;
- `n_bonds` depends on `bond_index` and must distinguish known zero from
  unavailable connectivity;
- `n_components` depends on `component_index` and must distinguish known zero
  from unavailable membership;
- `bond_joins_components` participates in component derivation but is not
  inferred from a missing `bond_type`;
- formal and fractional bond order have no implicit fallback relationship;
- aromaticity is not derived silently from a numeric order during delivery.

The current broad topological/structural/mechanical lists must gain an explicit
chemical-state classification or equivalent registry metadata. Compatibility
predicates such as `is_topological_attribute()` may continue to return `True`
for chemical-state topology attributes, but a dedicated classification must
allow state resolution without hand-maintained special cases.

### Complete delivery checklist for every attribute

No attribute in the inventory is complete until every applicable item below is
implemented or explicitly marked not applicable:

1. canonical registry entry, synonyms, domain, shape, dtype, nullability, units,
   dependencies, dependants, `get_from`, and `set_to`;
2. category exports and classification predicates;
3. native `attributes.py` capability declaration;
4. declarations for every priority form, defaulting to `False` unless a direct
   getter or accepted pipe can deliver the attribute;
5. instance-aware `has_attribute()` behavior distinguishing missing, nullable,
   known-empty, partial, and complete data;
6. public getter and, where accepted, setter for every declared element scope;
7. single-attribute and mixed-attribute `get()` delivery;
8. selection integration for attributes admitted by the grammar;
9. extraction, merge, copy, removal, sorting, and state-remapping behavior;
10. exact/equivalent/lossy/rejected conversion behavior and loss reporting;
11. persistence and legacy migration behavior;
12. Tier 1 declaration reachability and delivery tests, plus semantic fixtures;
13. NumPy-style docstring and doctest updates;
14. User Guide Foundations, Toolbox, and Cookbook updates;
15. verification and updates for the corresponding Four Paths course modules;
16. generated capability/reference tables, if present, regenerated from the
    registry rather than edited as an independent claim.

The form-adapter validation ratchet must fail any new Tier 1 `True` declaration
that lacks a reachable public getter or accepted pipe. Conversely, storage or a
getter alone does not authorize a `True` capability declaration until public
delivery and its tests pass.

### State-level fields

| Field | Domain | Meaning |
|---|---|---|
| `state_id` | nullable string | non-unique external or user label |
| `connectivity_completeness` | `unavailable`, `partial`, `complete` | scientific completeness of the bond set |
| `component_completeness` | `unavailable`, `partial`, `complete` | scientific completeness of component membership |
| `component_evidence` | `explicit`, `inferred`, `user_defined`, `unknown` | origin class of component membership |
| `provenance_index` | nullable `Int64` | optional shared provenance record |

The distinctions are mandatory:

- no chemical state: the state object does not exist;
- unavailable connectivity: a state exists with
  `connectivity_completeness="unavailable"`;
- known zero bonds: a state exists with
  `connectivity_completeness="complete"` and a zero-row bond table;
- partial connectivity: known bonds are stored, but absence of another edge is
  not asserted.

### Atom-state columns

All atom-state columns are aligned to the stable atom inventory. A missing
column means unavailable for every atom. A materialized nullable value means
unavailable for that atom. Explicit zero and `False` remain scientifically
distinct from missing.

| Field | Pandas dtype | Semantics | First vertical |
|---|---|---|---|
| `formal_charge` | `Int16` | integer formal charge in elementary-charge units | required |
| `is_aromatic` | `boolean` | atom is aromatic in this state | required |
| `n_unpaired_electrons` | `UInt8` | number of unpaired electrons | required |
| `n_implicit_hydrogens` | `UInt8` | represented implicit hydrogens | required |
| `allows_implicit_hydrogens` | `boolean` | implicit-H addition is permitted by the representation | required |
| `stereochemistry` | `string` | semantic atom stereochemistry such as `R`, `S`, `r`, or `s` | required but nullable |

Explicit hydrogen atoms remain normal atoms. `n_implicit_hydrogens` does not
count explicit hydrogen neighbors. `stereochemistry` stores a semantic label;
source traversal tags or implementation-specific chiral codes belong in
namespaced adapter metadata when required for an exact reverse conversion.

`unknown` and `unspecified` are explicit source values and are not the same as a
missing value. Arbitrary source enum strings are not accepted silently.

**Native public implementation status (2026-07-15).** These six fields are
implemented in private native state storage with the dtypes and missingness
rules above and are publicly delivered by native `Topology` and `MolSys`.
Internal storage uses the concise column names in this table; canonical public
attributes map `is_aromatic` to `atom_is_aromatic` and `stereochemistry` to
`atom_stereochemistry`. Public `get()`, `set()`, instance-aware availability,
mixed stable/state requests, and reference-state selection are tested. Missing
fields and unresolved multi-state reads fail explicitly. H5MSM 0.4 persistence
is implemented; rich third-party adapter conversion and explicit public state
selection remain gated.

### Bond table

The first-version allowed schema is:

| Field | Pandas dtype | Required | Semantics |
|---|---|---:|---|
| `bond_id` | `string` | no | non-unique source/user label |
| `atom1_index` | `Int64` | yes | lower canonical endpoint index |
| `atom2_index` | `Int64` | yes | higher canonical endpoint index |
| `bond_order` | `UInt8` | no | integral formal order; zero is allowed when explicitly represented |
| `fractional_bond_order` | `Float64` | no | fractional/partial order, independent of formal order |
| `bond_type` | `string` | no | chemical relationship kind, never a mechanical parameter type |
| `is_aromatic` | `boolean` | no | aromatic bond flag |
| `is_conjugated` | `boolean` | no | conjugation flag |
| `stereochemistry` | `string` | no | semantic bond stereochemistry |
| `stereo_atom1_index` | `Int64` | no | first stereo reference atom |
| `stereo_atom2_index` | `Int64` | no | second stereo reference atom |
| `donor_atom_index` | `Int64` | no | directional donor endpoint/reference |
| `acceptor_atom_index` | `Int64` | no | directional acceptor endpoint/reference |
| `joins_components` | `boolean` | no | whether this edge participates in covalent-component inference |
| `evidence` | `string` | no | `explicit`, `inferred`, `user_defined`, or `unknown` |
| `provenance_index` | `Int64` | no | optional shared provenance record |

The initial `bond_type` vocabulary is intentionally small:

- `covalent`;
- `dative`;
- `unknown` when the source explicitly says the kind is unknown.

Missing `bond_type` means unavailable, not `unknown`. Additional chemical kinds
require a contract amendment and component-participation decision. Amide,
disulfide, aromatic, single, double, and force-field parameter class are not
values of `bond_type`: they belong respectively to annotations, aromaticity,
formal order, or molecular mechanics.

`bond_order` never stores `"aromatic"`, `"dative"`, or an arbitrary source
string. Unknown order is never promoted to one. Aromaticity and fractional
order are independent columns.

`joins_components` prevents component semantics from depending on an
ever-growing bond vocabulary. Default normalization is:

| Bond type | Default `joins_components` |
|---|---:|
| `covalent` | `True` |
| `dative` | `False` |
| missing or `unknown` | missing; complete inference is not permitted |

A converter may provide a different explicit value only when source semantics
justify it and evidence/provenance records the decision.

## Graph and component invariants

The first vertical enforces the following structural invariants:

1. Endpoint indices are non-null, distinct, and within the stable atom range.
2. `atom1_index < atom2_index`; directional chemistry is preserved in the
   dedicated donor/acceptor fields.
3. Only one bond row is allowed per unordered endpoint pair. Query-graph
   multi-edges are deferred.
4. Self-bonds are rejected as malformed input.
5. Stereo reference and donor/acceptor indices must be in range and satisfy the
   accepted relationship-specific constraints.
6. Missing chemical attributes do not make a structurally valid edge invalid.
7. Implausible valence produces optional chemical-validation diagnostics; it
   does not make incomplete or unusual chemistry structurally malformed.

Component inference follows only edges with `joins_components=True`.

- Complete connectivity with complete participation values permits a complete
  inferred component partition.
- Partial connectivity may produce connected fragments for an analysis, but
  those fragments must not be exposed as a complete component partition.
- Explicit complete component membership may coexist with partial bond data if
  its evidence is preserved.
- A source assumption that molecules equal components must be explicit and
  reported; it is never an unmarked fallback.
- A covalent drug-protein adduct may be one component while retaining two
  semantic molecules.

Bond mutation invalidates inferred components deterministically. Explicit
component membership is marked inconsistent/stale after a conflicting graph
mutation and requires an explicit retain, rebuild, or replace decision; it is
not overwritten silently.

Extraction, merge, and atom removal remap every endpoint, stereo reference,
directional reference, atom-state row, and component membership together.
Sorting bond rows does not change chemical meaning or provenance association.

## Formal-charge migration

Chemical-state formal charge becomes authoritative. Partial charge and
`atom_ff_type` remain authoritative in `MolecularMechanics`.

The compatibility path is:

1. New writes store formal charge only in chemical state.
2. Legacy deserializers that find formal charge only in molecular mechanics
   migrate it into the reference chemical state and record legacy origin.
3. If both locations contain equal values, chemical state wins and the legacy
   duplicate is deprecated.
4. If both locations conflict, conversion or loading fails with an explicit
   resolution diagnostic; no precedence rule chooses silently.
5. The old `MolecularMechanics.formal_charge` access remains a temporary
   compatibility facade and is removed only through the normal deprecation
   lifecycle.

The public `formal_charge` attribute changes classification from mechanical to
chemical/topological state. This requires attribute-registry, `has_attribute`,
get/set, User Guide, API docstring, Cookbook, and course updates before the
public migration is complete.

## Conversion policy

Every chemical conversion is classified as exact, chemically equivalent,
lossy, or rejected, using the definitions in the execution checkpoint.

The proposed public control is a conversion policy with two behaviors:

- `strict`: reject any in-scope non-representable semantic field;
- `permissive`: return the target but emit a typed diagnostic and produce a
  structured loss report; permissive never means silent.

An optional report-return mechanism is preferred over changing the default
return type. Exact API spelling remains deferred until it is reviewed against
the existing `convert()` signature and lifecycle-integrity requirements.

Source-specific metadata may be retained in namespaced adapter metadata for an
exact reverse conversion, but it cannot masquerade as a canonical chemical
field. A generic conversion to another target reports loss of such metadata
when relevant.

### Priority adapter expectations

| Source/target | First required behavior |
|---|---|
| H5MSM 0.3 | read as one reference state; legacy bonds are treated according to a documented migration assumption |
| H5MSM 0.4 | persist the full accepted reference-state schema and explicit completeness |
| OpenMM Topology | preserve endpoints, optional order/type, elements, isotope where available, and report unsupported state fields |
| MDTraj Topology | preserve serial/resSeq labels exactly, endpoints, and available order/type without inventing chemistry |
| RDKit Mol | preserve accepted atom/bond state fields, direction, stereo references, and missingness |
| OpenFF Molecule | preserve formal charge, formal/fractional order, aromaticity, and stereochemistry |
| MDAnalysis | preserve endpoints, available type/order, and guessed evidence |
| ParmEd | separate chemical order/connectivity from mechanical bond parameter objects |
| mmCIF | distinguish chemical-component bonds, structural covalent connections, and non-covalent/coordination declarations |

H5MSM 0.3 migration may map legacy pair-only bonds to `bond_type="covalent"`
and `joins_components=True` because that matches the historical component
semantics, but the migration must mark this as a legacy assumption rather than
source-explicit chemistry.

## Native selection contract

Stable predicates remain state-independent. Predicates involving formal
charge, aromaticity, bond fields, component membership, or `bonded to` require
a resolved chemical state.

- one state resolves implicitly;
- multiple states resolve through an explicit state argument, an explicit
  reference state, or a structure selection that maps to exactly one state;
- ambiguous duplicate state labels raise an error;
- a structure selection spanning different states cannot return one ordinary
  atom-index selection for a state-dependent predicate and is rejected unless
  a future state-indexed result type is requested explicitly;
- zero states or unavailable required fields produce unavailable-attribute
  diagnostics, not empty selections.

This preserves the current meaning of `select()` as one set of atom indices and
prevents a trajectory-dependent query from silently returning a union or
intersection across states.

### Accepted explicit-state API

The first public state resolver is the keyword argument
`chemical_state='reference'` on `get()`, `set()`, `has_attribute()`, and
`select()`. The name `chemical_state_index` is not available for this control
because it is already a canonical attribute flag accepted by `get()`.

Accepted values are:

- `'reference'`, the backward-compatible default, which applies the one-state
  implicit rule or the stored reference index;
- `'structure'`, which resolves the unique known state associated with the
  requested structures of one native MolSys;
- a non-negative integer selecting one state by its 0-based index.

`None` is normalized to `'reference'`. Boolean values, negative integers, and
state IDs are rejected. IDs are labels and may be duplicated, so treating them
as selectors would contradict the native identity contract. State inventory
attributes such as `chemical_state_index`, `chemical_state_id`, and
`n_chemical_states` continue to describe all states even when the resolver
selects one state for other attributes.

Explicit resolution is execution-local and nested-call safe. It must not
change `reference_chemical_state_index`, copy a topology, or leave mutable
state after success or failure. The first implementation supports explicit
indices on native `molsysmt.Topology` and `molsysmt.MolSys`. Explicit indices
on external forms fail closed until the relevant adapter has an audited
multi-state mapping; callers can convert to a native form first.
Structure-to-state resolution is implemented by the nullable MolSys
association. A selection containing missing associations or more than one
state fails closed instead of choosing a reference, union, or intersection.

## Rejected alternatives

### Materialize every optional chemical-state column for every system

Rejected because nullable chemical-state metadata would impose substantial
memory cost on large protein and trajectory workflows. Chemical-state and rich
bond schemas are fixed logically, but optional columns are allocated only when
present. The stable atom table uses a fixed 1.0 physical schema; its possible
post-1.0 sparse-by-absence evolution is a separate compatibility decision.

### Infer components from every stored edge

Rejected because dative, unknown, query, or future relationship kinds do not
share one covalent-component policy. `joins_components` makes the decision
explicit and testable.

### Encode aromaticity and dative character in bond order

Rejected because those concepts are orthogonal to integral or fractional bond
order and cannot round-trip faithfully when conflated.

### Keep formal charge in molecular mechanics

Rejected because formal charge defines chemical state independently of a
force field and is needed by RDKit/OpenFF-style molecular representations.

### Let zero states return an empty bond table

Rejected because it would conflate unavailable chemistry with known zero
bonds. Compatibility access must resolve a real state.

## Implementation sequence after approval

The contract has been accepted for staged private implementation. The
recommended vertical and current status are:

1. add private `ChemicalState` storage and completeness enums without exposing
   a new public constructor;
2. implement optional atom-state columns and the normalized bond table with
   validation tests;
3. migrate native lifecycle operations and component invalidation;
4. add formal-charge compatibility migration and conflict tests;
5. implement state-aware native selection diagnostics;
6. implement H5MSM 0.4 plus explicit 0.3 reading and migration fixtures;
7. migrate RDKit and OpenFF as the first rich semantic adapters, then OpenMM
   and MDTraj as reduced adapters;
8. update public attributes and all lifecycle-integrity documentation;
9. remove legacy physical component storage only after repository-wide scans,
   conversion-truth tests, and performance gates pass.

Steps 1, 2, 4, 5, and 6 are complete; step 3 is substantially complete, and
the accepted portion of step 8 is implemented. The normalized bond table materializes
only used optional columns, enforces the canonical nullable dtypes and graph
invariants, and translates only unambiguous legacy `order`/`type` values.
Opaque legacy labels are rejected rather than installed as canonical chemistry.
Step 3 is substantially complete for copy, pickle, atom removal, state-aware
component storage, single-state add, and multi-state extraction. Component
membership has one state-local physical authority and no longer appears in the
stable atom table. Extraction subsets atom-state rows and independently remaps
component membership, component tables, bond endpoints, stereo references, and
directional references for every state. Native add preserves chemical atom
attributes for its supported single-state case and rejects multi-state input
until an explicit alignment policy is accepted.
The first private bond-access seam now covers native lifecycle operations and
`MolSysBuilder`. Central native getters, capability checks, native dictionary
forms, ViewerJSON, and H5MSM 0.3 native serialization now resolve the same
state seam. Legacy pickles migrate their atom-level `component_index` column
into the reference state, while H5MSM 0.3 deliberately keeps its legacy
physical dataset as an adapter translation. Native inference and all
endpoint-only preparation/build paths have also migrated, including additive
missing-bond behavior. Format and third-party
adapters still require explicit fidelity mappings. Extraction and native add
remap endpoints, stereo references, and donor/acceptor references together;
stereochemistry is removed when its reference atoms are not retained. H5MSM
0.4 persists every native state, nullable atom chemistry, state-local
components, normalized rich bonds, completeness, evidence, and provenance
references. Version 0.3 remains an explicit one-reference-state migration path,
and unknown future versions fail closed. The selector resolves state-local
component membership and the six public
atom-state fields lazily. It rejects missing attributes or an ambiguous
multi-state reference. State identity and completeness are inspectable through
public `get()`. Explicit state arguments now resolve native atom chemistry,
components, bonds, availability, and selection without mutating the stored
reference. `structure_chemical_state_index` is public, H5MSM-backed, and
preserved by native copy, extraction, removal, append, and concatenation.
Rich-bond public delivery is implemented for native Topology, MolSys, and
H5MSM. RDKit and OpenFF implement the priority rich inbound probes; MDTraj and
OpenMM implement their reduced bidirectional subset. Conversion preflight
reports and strict loss rejection are public. MDAnalysis, ParmEd, and mmCIF
implement audited rich inbound mappings; PDB/PDBFixer expose their reduced
semantics honestly, and NetworkX uses a documented canonical attribute graph.
The 17 active H5MSM demos are regenerated as 0.4 artifacts against an
independent manifest, with one isolated 0.3 migration fixture.

## Recorded approval checklist

The maintainer confirmed the following first-vertical decisions. Future changes
must amend them through a new decision record:

- optional `isotope` storage in stable topology;
- atom-state field names and first-vertical scope;
- bond field names and the initial `bond_type` vocabulary;
- explicit `joins_components` semantics;
- zero-state facade behavior;
- formal-charge migration and conflict policy;
- strict/permissive conversion-report direction;
- selector ambiguity behavior;
- H5MSM 0.4 as the first persisted chemical-state version.
