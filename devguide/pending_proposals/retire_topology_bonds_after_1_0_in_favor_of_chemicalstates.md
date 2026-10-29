---
summary: Complete ChemicalStates separation from Topology before 1.0.
issue: uibcdf/molsysmt#255
status: active
opened: 2026-09-29
closed:
verification: measured
area: [native, api, form, topology, chemical-states, docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# Complete ChemicalStates separation from Topology before 1.0

**Role:** accepted migration plan and execution tracker.
**Maintainer decision:** 2026-10-28.
**Implementation status:** In progress on `dev/chemical-states-separation-255`.
Storage extraction and the target-test battery exist there; public Topology
chemistry, query dispatch and file schemas have not been cut over. Main receives
the maintained record only. The dated execution receipt below distinguishes
passing controls from intentionally failing targets.

The maintainer explicitly replaces the earlier post-1.0 scheduling with a
coordinated pre-1.0 separation. The historical filename and issue number are
retained so existing issue/record links continue to work. The issue's original
post-1.0 title describes its opening decision; this dated record holds the
accepted expanded scope. Analysis and progress stay here under the
[reporting protocol](../reporting_protocol.md), rather than repeated issue posts.

## What

Make native Topology a stable atom inventory and semantic/chain hierarchy with
no owned or hidden chemical-state collection. Make ChemicalStates the complete
native authority for state-local bonds, discrete chemical assignments, component
tables and atom-to-component membership. MolSys coordinates these independent
domains. Introduce the public functional module `molsysmt.chemical_states` and
move the nine existing connectivity/chemical-graph tools identified below.
Chains, their IDs and ordered chain/group membership remain in Topology.

## Why

Chemical-state ownership was implemented under uibcdf/molsysmt#254, but native
Topology still constructs a private collection, exposes chemical facades and
houses much of the implementation. Queries, builders and adapters depend on that
route. Its apparent stable topology therefore still carries state-dependent data.
Complete the separation before freezing the 1.0 interface, and before introducing
the identity/scaffold tools proposed in uibcdf/molsysmt#447.

The expected benefit is an explicit, consistent API and reliable state selection.
A pure topology copy should no longer copy chemical payloads. No quantified RAM,
speed or universal chemistry-coverage improvement is claimed by this plan.

## Accepted boundary and exclusions

| Owner | Target responsibility |
| --- | --- |
| `Topology` | Stable atom elements/isotopes and labels; groups, molecules, entities and chains; their stable memberships, including ordered chain/group declarations. |
| `ChemicalStates` | State records, nullable reference, bonds and bond attributes, discrete atom assignments, state-local components and membership, completeness/evidence and preparation history. |
| `Structures` | Coordinates, boxes and other structural series under the existing units/ownership contract. |
| `MolSys` | Explicit domain composition, shared atom-axis validation/remapping, structure-to-state association and named-analysis invalidation. |
| `chemical_states` | Public form-agnostic connectivity, chemical-graph analysis and state operations. |
| `topology` | Sequence analysis and tools about represented stable hierarchy. |
| `physchem`, `structure`, `pbc`, `interactions` | Their existing property/model, geometric, periodic and interaction responsibilities; compose the new chemical owner where needed. |

Do not migrate a function solely because it reads a chemical state. TPSA,
lipophilicity, geometry and interaction recognition retain their scientific
owners. Review state-assignment tools later if necessary; this is not permission
to relocate all of physchem or implement new preparation science.

Excluded: new detectors/acceptor models, hydrogen refinement (#323), chemical
normalization (#366), identity/scaffold implementation (#447), state enumeration,
new MolecularMechanics behavior/persistence, new H5MSM root versions, GUI
synchronization policy and unrelated parser/streaming redesigns. Keep scientific
methods, declared coverage, units and provenance unchanged during migration.

## How: contracts that must survive

### Inventory, states and components

- A standalone Topology neither constructs nor owns ChemicalStates. Its weak
  MolSys owner link may notify supported edits, but cannot recover hidden chemistry
  to keep old chemical getters working indirectly.
- Remove `Topology.bonds`, `Topology.components`, their counters, chemical
  constructor arguments, state proxies and chemical editing/rebuild methods.
  Pure Topology comparison, copying and extraction concern its own inventory.
- Component indices are positions within one state, not stable cross-state
  identities. Component IDs remain string labels. Preserve component metadata
  only under the supported correspondence rule, not matching row numbers alone.
- Preserve the existing explicit `joins_components` policy and completeness/
  evidence semantics. Do not redefine component connectivity as a side effect
  of the namespace move, or equate an incomplete graph with complete chemistry.
- Molecules and components remain different. Initial molecule inference may use
  an explicitly selected state's partition when stable hierarchy is missing.
  Changing a state must not silently rebuild molecule/entity/chain inventory.
  Component type/name inference may request stable inventory context explicitly.
- Do not introduce `groups.component_index`, `groups.chain_index`, a second
  bond table, or an element/symbol store competing with stable Topology.
- Keep absence, a present collection with zero states, a state with unavailable
  connectivity and a complete graph with zero edges distinguishable. An empty
  stored bond table alone does not establish physical absence of bonds.

### Construction and public queries

- Preserve the current `ChemicalStates(n_atoms=...)` zero-state constructor.
  MolSys/Builder create any documented initial working state themselves; never
  obtain one as a side effect of constructing/converting a Topology.
- Prefer preserving ordinary MolSys/Builder constructor convenience and the
  existing unknown/incomplete initial-state semantics. Settle exact signatures
  before coding; do not combine unrelated default changes with the migration.
- ChemicalStates native methods and its form adapters must support bonds,
  components, assignments and counts where the domain actually provides them.
  A state-only system can expose graph indices without pretending to supply
  elements, atom names or group hierarchy that it lacks.
- `basic.get/set/select/info/has_attribute/where_is_attribute` and native
  `get/info` retain their public experience. Chemical fields route through the
  chemical domain; mixed queries on MolSys can use both domains without copying
  the full system. Reconcile attribute classifications and piping, not only imports.
- Resolve the state before validating state-local bond/component indices.
  Preserve explicit reference, integer-state and structure-associated selection.
  A missing/ambiguous/mixed state cannot silently become state zero or reference.
- Resolution cannot mutate the collection's reference index. Preserve nested and
  independent query behavior, including failures. Read native tables directly
  below the validated boundary; no native rebuild through universal dispatch.
- State-dependent queries on pure Topology follow the supported missing-attribute
  behavior, not fabricated empty arrays or zero counts. Scientific operations
  requiring chemistry reject unavailable prerequisites with useful diagnostics.

### Lifecycle and edits

- MolSys owns one chemical collection, independently of its topology. Replacing
  a topology cannot replace chemistry implicitly; replacing chemistry cannot
  introduce a second topology-owned collection. Preserve explicit correspondence.
- MolSysBuilder owns chemical states separately. Preserve selected-state editing,
  other state records, reference/associations, IDs and original preparation history.
  Extending atoms coordinates all owned states without inventing assignments.
- Use one coordinated atom map for inventory, every state's bonds/assignments/
  components, structures, mechanics where supported and named analyses. Preserve
  extraction, removal, permutation and managed prefix growth contracts.
- Validate incompatible changes before publication. A rejected edit cannot leave
  the topology and chemical atom axes at different sizes. Define attached native
  domain edits so direct access cannot bypass owner coordination.
- Preserve controlled chemistry/geometry edit invalidation, including evaluated-
  empty coverage, stale analysis references and explicit recalculation. No automatic
  scientific recalculation or full-coordinate snapshot/hash surveillance is added.
- Preserve native copy/deepcopy/pickle graph aliasing, concrete types, weak owner
  exclusion/rebinding and protected geometry sharing. Historical preparation reports
  keep their original operation-index scope and producer, not rewritten indices.

### Functional namespace

Create lowercase `msm.chemical_states` independently of uppercase
`msm.ChemicalStates`. Public functions accept any supported molecular-system form
supplying their prerequisites, not exclusively a native ChemicalStates instance.

| Current `topology` export | Canonical target |
| --- | --- |
| `get_bondgraph` | `chemical_states.get_bondgraph` |
| `get_covalent_blocks` | `chemical_states.get_covalent_blocks` |
| `get_covalent_paths` | `chemical_states.get_covalent_paths` |
| `get_rings` | `chemical_states.get_rings` |
| `get_rotatable_bonds` | `chemical_states.get_rotatable_bonds` |
| `get_rigid_fragments` | `chemical_states.get_rigid_fragments` |
| `get_substructure_matches` | `chemical_states.get_substructure_matches` |
| `get_atom_correspondences` | `chemical_states.get_atom_correspondences` |
| `get_dihedral_quartets` | `chemical_states.get_dihedral_quartets` |

`get_sequence_alignment` and `get_sequence_identity` remain in topology and must
continue working with group-only/sequence inputs. Dihedral-quartet recognition
moves; computing angles from coordinates remains in structure. Add explicit
state/structure selection to paths and quartets and the documented digestion
boundary, preserving positional arguments where practical.

Relocate shared chemical-graph helpers under their new owner and update consumers
in build/physchem/interactions. Reuse Rust primitives; neither a new algorithm,
new dependency nor compiled ABI rename is required merely by moving ownership.
Update lazy discovery, API registry/waivers, ArgDigest caller maps, SMonitor
callers, Ackredit boundaries, docs and addon inventories. Retain original method
names, numerical results and historical producer metadata.

Recommended cutover: no permanent compatibility facades or duplicate public
ownership. Old native Topology chemical access must disappear. Any temporary
functional-path alias needs an explicit bounded exception with consumer, removal
condition and tests; it is not the default implementation strategy.

### Conversion, dictionaries and files

- Conversion to native Topology is an inventory/hierarchy projection. Preserve
  chemistry through MolSys or explicit domains. Apply the conversion-fidelity
  report/strict contract; do not lose chemistry silently in an intermediate
  Topology used to construct a supposedly complete output.
- Audit real producer routes, not just changing every `to_form` string to MolSys.
  Use the smallest faithful domain/context and preserve lazy coordinate access.
  State-only, structures-only, group-only and mixed partial systems remain valid.
- H5MSM 0.5 already stores independent layers. Preserve its root version, typed
  layer codecs, topology layer-2 chain/group relation, associations, units,
  original producer versions and named analyses. Read 0.3/0.4 through the maintained
  warning/migration route into the new owners.
- Recommend new TopologyDict/MolSysDict schema 0.2 rather than silently changing
  schema 0.1. TopologyDict contains stable inventory; MolSysDict has an explicit
  chemical-state domain. Freeze the actual schema during P0/P6 before writers.
- Reuse ChemicalStatesDict's typed/null-mask codec. It is not directly JSON
  serializable: define explicit JSON-safe transport without losing types, nulls,
  units, multiple states, reference selection or correspondence. Do not insert
  NumPy arrays into a payload advertised as directly JSON compatible.
- Legacy dictionary readers decode chemistry directly to its new owner, without
  a chemical intermediate Topology. A pure-Topology projection reports any loss.
- Audit old pickle class paths and legacy restoration separately from copy.
  Private decoding aliases may resolve historical state-storage classes without
  restoring a Topology chemistry facade. Mixed legacy Topology payloads need an
  explicit migration/refusal contract; never discard their chemistry silently.

## Execution tracker

Checkboxes are the work-item record. Mark an item complete only after its actual
exit evidence exists; record commit, command/exit status, scope, environment and
remaining limitations in the phase receipt. A moved file or passing import alone
is not completion. Do not manufacture a completion percentage from phase count.

| Phase | Dependencies | Current state | Exit evidence |
| --- | --- | --- | --- |
| P0: contract and baseline | Maintainer decision | Contracts, baseline and receiving notices recorded | Accepted contracts, frozen source/worktree and impact inventory |
| P1: target/characterization guards | P0 | Initial 36 target cases recorded; broader controls/measurements remain | Independent expected behavior and baseline evidence |
| P2: native authority | Initial P1 controls; full cutover still needs P3/P4/P6 | Storage/graph primitives, C1 stable molecules, C3 graph edits and private typed assignment authority implemented on development branch; pure Topology and consumer cutover remain | Standalone state operations; pure Topology; no hidden recovery |
| P3: query/form dispatch | P2 | Stable molecule projection, collection-owned scopes, stored/nullable queries, atom/bond/component assignments and direct typed dictionary reads implemented on development branch; dictionary setters, predicates and mixed-owner cutover remain | Basic/native/form parity and truthful capabilities |
| P4: builder and lifecycle | P2, P3 | Stable molecule transport, C4 restriction and atomic selected-state graph edits implemented; MolSys/Builder ownership cutover remains | Coordinated edits/remaps/copies and invalidation |
| P5: functional module | P3; P4 for integration | Not started | Nine moved APIs, state selection and unchanged scientific controls |
| P6: conversions/persistence | P3, P4 | Topology layer 3 and bounded legacy molecule recovery implemented; dictionary 0.2 and final domain cutover remain | Versioned payloads, legacy readers, partial and full round trips |
| P7: docs and consumer receiving | P5, P6 | C1/C3/C4 lifecycle documentation and ChemicalStates native guide updated on development branch; final migration and receiving remain | Lifecycle docs and immutable consumer receipts |
| P8: integrated source closeout | P1-P7 | Not started | Exact-source checks, published implementation and issue receipt |

Documentation work can accompany each implementation phase. Independent execution
may overlap, but dependent phases cannot claim their exits early. The final
installed-candidate qualification remains in #334/#254 after source closeout.

### Design review — 2026-10-28

The accepted ownership model remains appropriate. The plan covers the major
subsystems, but it is not yet an implementation-ready contract. The following
source-inspected findings make P0.5 concrete; their implementation choices are
pending, not additional approved APIs. No refactoring or target tests were run
for this review. The runtime inspected is unchanged from `71fbe4f46d3c70e4e973c8025f01752a8c9b1084`;
`01221cf999b59e76c1bdf0351267d8c82940c552` adds planning documents only.

**R1 — Phase numbers are not a safe order for deleting existing dependencies.**
P2's removal affects MolSys construction/attachment, Builder, native queries and
producer adapters that are migrated in P3/P4/P6. For example,
`molsysmt/native/molsys.py` still binds chemistry through Topology, and
`molsysmt/_private/native_composition.py` uses its private chemical collection.
An isolated native-core test passing would not make that intermediate source
usable. Before implementation, identify coherent increments and the required
bootstrap changes across those workstreams. Prepare independent chemical storage
first; coordinate owner binding, producer assembly and query delivery before
removing their old route. Existing facades may remain on the isolated migration
branch while their callers are ported; this does not authorize a new facade,
second store or final compatibility API. Publish to main only a coherent tested
cutover. Do not treat phase dependencies as requiring an incompatible sequence
of public main commits. Record any intentionally broken branch checkpoint as
such, never as a passing source delivery.

**R2 — Stable atom-to-molecule membership needs an explicit group-free model.**
`molsysmt/native/_topology_infer.py:molecule_indices_from_atoms` reads reference
components when there are no groups. The canonical atom table has group/chain
membership, while molecule membership otherwise lives on groups. Builder's
`_retain_group_free_molecule_axis` currently aligns component positions with
inherited molecules and rejects connectivity that splits/merges those boundaries.
Removing chemical ownership without replacing this dependency loses stable
membership. Select a representation in Topology that preserves declared
group-free atom-to-molecule membership independently of later states, without
inventing groups or equating molecules with components. Decide its precedence,
unknown entries, remapping and legacy initialization. Carry it through extraction,
permutation, dictionaries and H5MSM. The H5MSM root stays 0.5; an additional
versioned topology-layer encoding may be needed, so retaining existing layer
readers must not be mistaken for freezing every layer's writer version.

**R3 — The editing migration needs a public method/signature map.**
The nine-function table covers graph analysis, not the complete editing surface.
Before code changes, inventory each removed constructor argument/native method
and its replacement owner, required stable context, selected-state argument,
return value and owner notification. Include add/remove bonds, component rebuild,
atom assignments and MolSys convenience methods. Distinguish graph edits from
chemical perception/preparation and stable hierarchy rebuilds; do not mechanically
move every chemistry-consuming operation. Specify whether returned tables are
live or detached and which direct edits are supported. Reject unsupported writes
clearly rather than promising automatic invalidation of arbitrary raw table edits.

**R4 — Remapping must distinguish restriction from rebuilding connectivity.**
`ChemicalStates._extract_atoms` currently restricts bonds and remaps stored
component membership; it does not recompute the induced graph's components.
Removing the middle atom of a three-atom path exposes that distinction. Decide
whether the supported operation preserves declared membership/evidence, rebuilds
when the knowledge permits it, or requires an explicit rebuild. Do not introduce
automatic scientific inference merely by relocating this method. Record component
metadata transfer for split/merge, incomplete connectivity and removed last atoms.
Also define the admitted state-alignment rule for system addition and structure
append: state indices and IDs alone do not establish equivalent chemistry.
Preserve current explicit associations and ambiguity handling; reject unsupported
combinations without inventing a Cartesian product of states. Add analytical
controls for path restriction, split/merge, reordered states and failed edits.

**R5 — Use a route matrix for capabilities, including indirect consumers.**
For representative native, dictionary, external-object and file forms, record
which routes deliver inventory, chemical states and their composition, and which
pure-Topology projections intentionally lose chemistry. In particular,
Topology-to-ChemicalStates/graph/engine adapters cannot continue advertising a
delivery path that only returns a fabricated empty chemical domain. Include
`basic.compare`, `Iterator`, selection syntax engines and count/provider helpers
as explicit audit targets: current compare normalization calls Topology component
rebuilds, and iteration classifies attributes before selecting a route. Port
existing supported behavior; new state-aware iterator features are not implied.
Use actual route/capability checks and independent values, not successful imports
or a text search alone, as the exit evidence.

**R6 — Capture performance baselines before changing the implementation.**
P8's after-change measurements need comparable P0/P1 baseline inputs and results.
Select representative atom/state/bond counts, a group-free case, a group-only
case and a large structures axis. Compare native queries, pure-Topology/MolSys
copies, atom remapping and projected H5MSM reads, recording peak memory and
allocation/I/O behavior as well as elapsed time. Specify the comparison and
investigation criteria before interpreting results; do not invent an absolute
speedup target. Atomic edits must stage affected data without routinely copying
all coordinates, every unaffected state or a whole file. This is a bounded
migration regression check, not a new storage-engine benchmark project.

R2 and the constructor/edit/schema decisions in R3 must be resolved before their
implementations. R1 determines integration order; R4/R5 determine guards and
routes; R6 requires baseline evidence before the measured paths change. These
are refinements of P0-P8, not a second independently maintained task tracker.

### P0 contract decisions — 2026-10-28

The maintainer authorizes proceeding with the review follow-up. The engineering
choices below resolve R1-R5 for implementation; R6 has selected workloads but
still requires performance measurements before their implementations change.
These are target contracts, not descriptions of current runtime behavior.
No implementation, new API export, writer change or target test is delivered
by recording them. The later execution receipt records P0.6 notices separately
from still-pending client receiving and installed qualification.

#### C1: stable molecule membership without synthetic groups

Keep the existing atom/group table columns. Add optional atom-aligned stable
membership to Topology, internally `_atom_molecule_membership`: a one-dimensional
int64 vector of length n_atoms, using -1 for unknown. Allocate it only when an
ungrouped atom has a declared molecule. With no such declarations, store None.
This costs eight bytes per atom when materialized, independent of the number of
structures or chemical states; this is a representation bound, not a benchmark.

Resolve molecule membership by this disjoint rule:

1. An atom with a group uses that group's molecule_index, including an unknown
   value. The optional vector must contain -1 at that atom's position.
2. An atom without a group uses the optional vector; an absent vector means
   unknown. Never consult ChemicalStates while answering this topology query.
3. A grouped atom cannot override its group's molecule. Reject conflicting
   assignments before mutation rather than choosing a precedence silently.

Use a native `Topology.set_atom_molecules(molecule_indices, atom_indices='all',
skip_digestion=False)` boundary for ungrouped assignments and normal basic/native
get routes for reading resolved membership. None entries declare unknown, while
nonmissing indices must identify stored molecules. Existing grouped membership
editing remains at the group level. A grouped position included in a setter
request must match its resolved group value and is a no-op, never an override.
Internal codecs/builders use the same
validator; do not create an alternative public atom-table column.

Mixed grouped/ungrouped systems are supported. Adding a group to a previously
ungrouped atom must explicitly reconcile its declared molecule and clear the
optional entry transactionally; it cannot silently discard a conflict. Atom and
molecule remaps apply to this vector. Pure Topology copies and projected reads
retain it without accessing chemistry. No group or molecule is invented on read.

When initially building missing hierarchy from chemistry, the builder may
materialize a selected component partition into this stable representation
once, with its established inference evidence. Subsequent bond/state edits
never refresh it. For legacy inputs whose group-free membership was represented
by reference components, snapshot that documented source partition during
migration. An ambiguous/missing reference cannot establish membership: preserve
unknowns and report the limitation, rather than selecting state zero.

#### C2: constructors, domain attachment and builder state

The target Topology signature is:

```python
Topology(n_atoms=0, n_groups=0, n_molecules=0, n_entities=0,
         n_chains=0, skip_digestion=False)
```

Remove n_bonds/n_components from Topology and audit positional calls: their
removal changes positional binding, so the old positional order is not a
compatibility promise. Preserve MolSys's existing constructor arguments and
order, including n_bonds/n_components. MolSys creates its own initial working
state with unavailable completeness, then allocates requested staging rows in
that state. Counts/placeholders do not certify bonds or components as complete.
ChemicalStates(n_atoms=...) still creates zero states and no reference.

Explicit composition/conversion of a Topology does not call the ordinary MolSys
constructor and thereby add chemistry. A topology-only MolSys remains
chemical_states=None. A present zero-state ChemicalStates remains present and
empty. Replacing an attached topology with a compatible atom axis preserves
chemistry; replacing chemistry preserves stable hierarchy. A replacement operation
declares positional correspondence; equal counts are a shape check, not proof of
identity. Atom-axis resizing uses a coordinated edit, not these setters.

MolSysBuilder stores its own ChemicalStates. A fresh builder has one unknown
working state. From a MolSys, it copies the source's present collection/reference,
or preserves its explicit absence. An operation requiring chemical editing on an
absent/zero-state input fails with instructions to supply/create a state; it does
not create one merely by reading/building. Bond editing gains a keyword-only
chemical_state argument, defaulting to reference. An ambiguous reference fails.
Counts lacking a state argument use the same resolvable-reference rule.

Builder must carry a source MolSys's structure/state association vector as staging
metadata and restore it at build. This is an explicit extension of the current
builder, whose documented behavior stores no such associations. Structural-axis
replacement must validate alignment or reject an incompatible existing map before
publication; no reassignment by position after an unexplained length change.
Named analyses/mechanics remain outside the builder's supported stored payload;
this migration does not silently advertise their preservation.

#### C3: editing surface and mutable-table boundary

The target native mapping is as follows. New native methods use arg_digest and
skip_digestion; chemistry arguments are keyword-only where added to an existing
positional signature. Native methods operate on native data without universal
conversion/selection dispatch.

| Current entry | Target contract |
| --- | --- |
| Topology.add_bonds(pairs) | ChemicalStates.add_bonds(bonded_atom_pairs, *, chemical_state='reference', skip_digestion=False); returns None. Validate pairs and rebuild the selected state's stored-graph components. |
| Topology.remove_bonds(indices) | ChemicalStates.remove_bonds(bond_indices='all', *, chemical_state='reference', skip_digestion=False); returns None, compacting selected-state bond indices. Empty input is a no-op. |
| Topology.rebuild_components(...) | ChemicalStates.rebuild_components(redefine_indices=True, redefine_ids=True, redefine_types=True, redefine_names=True, force=False, *, chemical_state='reference', topology=None, skip_digestion=False); returns None. |
| Topology.n_bonds/n_components and get_n_* | ChemicalStates.get(n_bonds=True/n_components=True, chemical_state=...); no new ambiguous collection-wide bond/component property. |
| Topology.reset_bonds/reset_components | No new public reset facade. Construction allocates staging rows privately; removing all bonds uses remove_bonds('all'); explicit component reconstruction uses rebuild_components. |
| Topology.bonds/components and atom-state fields | State-aware basic get/set and ChemicalStates native get/info/adapters; no replacement Topology property or hidden owner lookup. |
| MolSys.rebuild_components(ids, types) | Preserve its two positional flags; expose remaining reconstruction flags, chemical_state and skip_digestion as keywords; delegate to its chemical collection with explicit topology context. |
| Topology.add_missing_bonds | Remove it; use the existing build.add_missing_bonds form-agnostic preparation operation. Do not add geometry-based perception to ChemicalStates. |
| MolSys.add_missing_bonds | Preserve the convenience operation and its scientific arguments, add keyword-only chemical_state, and delegate to the existing build pipeline; test actual parameter forwarding. |
| Builder.add_bond/remove_bonds | Preserve existing return conventions, add keyword-only chemical_state and edit the builder's chemical collection. |
| Atom/bond/state metadata setters | Keep existing public basic.set attribute names/units; route them to selected ChemicalStates records. Private typed setters move with the authority. |

For rebuild_components, an explicit native topology provides stable context. An
attached collection may obtain that context from its MolSys owner; a standalone
collection can rebuild graph indices without it. Unavailable type/name evidence
stays unknown, not an invented label. Preserve exact-atom-set metadata matching,
joins_components, nullable IDs and completeness policy. Missing inventory needed
by an actual scientific perception tool is a prerequisite error.

Preserve get_bonds' current live-table return for this migration. It is a read/
interchange view, not a supported editing gateway: arbitrary pandas/NumPy writes
cannot promise validation or owner invalidation. Document that limitation beside
the method and provide the controlled methods/basic.set path. Do not introduce
coordinate or table polling, a second table store, or an unmeasured mandatory
copy on every read. Internal callers requiring edits must migrate to the
controlled boundary rather than relying on a writable getter.

Controlled bond changes stage validated bonds, component updates and affected
analysis invalidation before publication. Failure in reconstruction/allocation
leaves all three unchanged. This deliberately strengthens the current documented
bond-first/component-later behavior and needs a failure-injection guard. Only
affected chemical records are staged; coordinates and unrelated states are not
copied. Follow existing label-only versus scientific-change invalidation rules;
conservatively invalidating all evaluated coverage for chemical changes remains
admitted, without adding automatic recalculation.

#### C4: restriction, reconstruction and state alignment

Keep state indices/reference/structure associations unchanged by an atom-only
selection. Remap every bond atom reference, not just its endpoints: stereo,
donor/acceptor indices and assignment-indexed evidence need the existing supported
remap/invalidation rules. Never copy invalid pointers into a smaller domain.

For components, distinguish these cases explicitly:

| Source evidence / operation | Target behavior |
| --- | --- |
| Pure atom permutation | Preserve component membership/metadata under the shared atom map; it changes neither connectivity nor molecules. |
| Extraction with complete stored connectivity | Recompute the selected induced graph's component partition using existing participation flags. Preserve metadata only for unchanged full source atom sets; changed components receive generated local string IDs and unknown names/types unless explicitly reconstructed with adequate context. |
| Extraction with partial/unavailable connectivity | Restrict declared component memberships and compact retained rows without certifying them as the complete induced-graph partition. A cut/changed partition downgrades complete component declarations to partial; unavailable remains unavailable. |
| Explicit bond edit/rebuild | Rebuild from the admitted stored graph; preserve completeness/evidence limits. Known edges do not imply complete chemistry. |

The complete-connectivity extraction rule is a deliberate correction to current
restriction-only behavior. A complete path 0-1-2 extracted to [0, 2] must have two
components while retaining one stable molecule if that was its declared identity.
No caps, hydrogens, aromaticity, protonation or bond orders are perceived during
this correction. A graph complete within a selected domain is not a certificate
of a complete standalone chemical fragment; boundary-sensitive scientific tools
must retain their existing full-context requirements. Preparation history keeps
its original operation-index scope.

Topology.add concerns only stable inventory and memberships. MolSys.add keeps
the admitted one-state plus one-state chemical union; zero/absent/multistate
chemical combinations lacking an admitted alignment policy fail before mutation.
Do not introduce broadcasting, pair-by-ID matching, zipping by equal counts or a
Cartesian product. Topology-only additions do not need a chemical-state policy.

For append_structures, preserve associations when chemical inventories match
under the existing strict ordered comparison; its implementation moves out of
Topology. A structures-only source may use the target's existing unambiguous
single-state convention, or unknown associations for multiple states. Conflicting
declared source chemistry is rejected rather than silently assigned to target
state zero. Reordered states require explicit alignment before appending; no
new public state-alignment/enumeration API is introduced in this migration.

#### C5: wire boundaries and legacy projection

Freeze the TopologyDict/MolSysDict writer version at '0.2'. Preserve 0.1 readers
and report chemical loss when a legacy chemical payload is projected to pure
Topology. The latest TopologyDict has its existing format/kind/version/metadata
and five stable tables, optional chain_groups and optional atom_molecules; no
bonds/components or chemical-state records. atom_molecules represents only the
ungrouped map in C1, not resolved grouped membership.

MolSysDict 0.2 has explicit topology, chemical_states, structures,
structure_chemical_state_indices and interactions entries, in addition to
format/kind/version/metadata. An absent domain is None, a present zero-state
collection is an encoded collection with states=[], and an empty named-analysis
collection is {}. Topology embeds its complete versioned dictionary. Chemistry
and named analyses reuse their existing versioned typed codecs; association
indices use nullable int64 storage. Structures retain explicit quantity records
and the existing optional-series/site/assembly information supported by the
native/file contracts. Unsupported mechanics or extension payloads must be
reported/rejected under the existing conversion-fidelity policy, not silently
omitted. No MolecularMechanics persistence is admitted.

Keep the standalone ChemicalStatesDict/InteractionsDict in-memory contracts.
For their inclusion in a directly JSON-safe MolSysDict, use one private reusable
typed transport under the existing serialization owner: primitive mappings/
sequences plus explicit dtype/shape array records. Numeric/bool arrays use
validated base64 C-order bytes; string arrays use validated string values with
dtype/shape. Preserve large integer bits, nonfinite values and null masks without
pickle, object-array decoding or executable YAML tags. Use PyUnitWizard's existing
QuantityRecord for dimensionful values instead of building a competing unit codec.
The transport has its own version and a reserved envelope; malformed lengths,
unsupported dtype/shape and unknown versions fail before native construction.
At a schema-declared array position, the envelope fields are
`__molsysmt_transport__='ndarray'`, `version=1`, `dtype` (NumPy dtype.str),
`shape` (nonnegative integer dimensions), `order='C'`, `encoding` and `data`.
For numeric/bool arrays encoding is 'base64' and data is the encoded bytes;
for fixed-width Unicode arrays encoding is 'strings' and data is a flattened
C-order list of strings. Object/structured arrays are unsupported. Validate
decoded byte/value counts against dtype and shape, including zero-sized and
scalar arrays. Domain schemas identify these positions; arbitrary user metadata
cannot become a typed array merely by containing the reserved key.
Do not extend the existing scalar-only to_builtin helper to pretend this is
lossless. JSON/YAML serialization is a materializing interchange boundary;
large numeric workloads continue to use H5MSM.

H5MSM root version remains 0.5. Read topology layers 1/2 unchanged. Write a new
topology layer 3 only when atom_molecules is materialized, retaining the existing
five tables and optional chain_groups plus the typed membership vector. Readers
must reject unsupported versions truthfully. Legacy group-free membership that
requires chemical context is initialized by the complete-file migration/assembly
route, not by a chemistry-reading pure topology getter. A projected older topology
layer alone can retain unknown membership and report that limitation. Independent
chemical/interactions layers need no version bump solely because Python ownership
moved. Existing canonical artifacts are not rewritten.

#### C6: coherent delivery order and route admission

Use an isolated development branch for runtime work. Capture the baseline first;
prepare independent chemical storage, stable membership and validated internal
primitives while the existing facade still serves unmigrated branch callers.
Then migrate MolSys/Builder binding and the essential native producer/partial
composition routes with basic/native queries as one usable slice. Move graph
functions and remaining adapters/codecs, and finally delete the old Topology
chemical implementation/facades after every required caller has a replacement.
There is no phase-by-phase permission to publish a broken main.

P2-P6 are linked workstreams with this cutover order; dependencies in the overview
identify prerequisite functionality, not a claim that all of P2 can close before
any P4/P6 bootstrap change. A development checkpoint may contain disclosed failing
target tests, but source closeout requires the coherent required gates. Preserve
no new permanent old-path aliases. No third-party client is edited without the
suite's owning contribution route and receiving issue.

The initial route matrix must test these contracts:

| Input/target | Required admitted route |
| --- | --- |
| Pure native Topology / latest TopologyDict | Stable queries, copying and extraction; chemical capability absent, even while attached to MolSys. |
| ChemicalStates / ChemicalStatesDict | State-local graph/count/assignment delivery; labels and structural selections require declared external context. |
| MolSys / MolSysDict / H5MSM 0.5 | Present domains and explicit associations; mixed native/basic queries without whole-system reconstruction. |
| Complementary native/partial providers | Compose explicit shared axes; reject conflicting owners/providers before applying selection. |
| RDKit, PDB/mmCIF, SDF/PDBQT and other supported producers | Preserve available chemistry in MolSys/ChemicalStates; direct Topology output is a reported projection. |
| Topology to chemistry/graph/engine targets | Remove fictitious chemistry routes; require explicit domain composition where the target needs bonds/assignments. Stable-only targets remain admitted. |
| Sequence/FASTA forms | Preserve group-only inventory, chain_groups and zero atoms without allocating fake chemical bonds or coordinate atoms. |
| compare / Iterator / selection engines | Reconcile actual attribute classifications and providers; missing chemistry cannot silently become reference-state zeros or trigger unrequested inference. No new iterator scientific feature is admitted. |

`get_missing_bonds=True` is not permission to restore a chemical store inside a
pure Topology. Keep admitted derivations at their appropriate provider/build
boundary, with truthful capability/fidelity reporting.

#### C7: baseline receipt and measurement selection

Runtime baseline source: `451b914cab8b596c01d84432a4f41b4a3e28f3cf`; earlier
`71fbe4f46d3c70e4e973c8025f01752a8c9b1084` has identical runtime source. The
development worktree has four unrelated API autosummary edits, preserved without
staging them. Python 3.14.7 on Linux x86_64 imports this checkout's molsysmt and
its local `_rust.abi3.so`. Dependency versions: NumPy 2.4.6, pandas 2.3.3, h5py
3.16.0, RDKit 2025.9.5, pytest 9.1.1, xdist 3.8.0 and Pytest Receptor
1.2.1+22.g00a31c4. This identifies the source-test environment, not an installed
canonical package or a new platform qualification.

Executed on 2026-10-28:

```bash
python -m pytest --receptor=llm -n 12 \
  tests/native/test_chemical_states.py \
  tests/native/test_chemical_states_owner.py \
  tests/native/test_molsys_chemical_state_association.py \
  tests/native/test_group_free_molecules.py \
  tests/native/test_molsys_builder.py \
  tests/basic/get/test_explicit_chemical_state.py \
  tests/form/file_h5msm/test_chemical_states_v05_probe.py \
  tests/form/file_h5msm/test_absent_chemical_states_v05_probe.py
```

Exit 0: 97 passed in 8.65 s, nine warnings (seven unknown atom-name warnings and
two expected legacy H5MSM warnings). These are unchanged current-behavior tests,
including assertions that the refactoring must intentionally replace. They do
not verify C1-C6 or any new API. No new target tests had been written at this
baseline checkpoint; the later execution receipt records the initial battery.

Select these bounded performance controls before changing the measured paths:

- Small analytical: three atoms/path, two chemical states, cut/permuted selections;
  plus a zero-atom, three-chain group-only system for inventory queries.
- Chemical scaling: 10,000 and 100,000 atoms, one and ten stored states,
  approximately one stored bond per atom, reused versus differing partitions.
- Structural isolation: 1,000 atoms by 1,000 structures, one/ten states, verifying
  that chemical-only edits do not allocate/copy the coordinate payload.
- Projected file access: H5MSM with named analyses and independently optional
  domains; compare metadata/topology-only reads and a nonconsecutive structure
  selection without materializing the full file.

Record actual fixture sizes, seeded construction, dependency/hardware origin,
one warm-up plus seven timed repetitions, median/range and process peak memory
with independently run baseline/target processes. Retain commands and inputs
with the eventual benchmark evidence under this issue. Investigate a reproducible
time/RAM regression, and reject unbounded structural materialization or chemistry
copying during pure-Topology operations. Do not classify timing noise or infer
speedups from these unexecuted workloads. Measurements remain pending P1/P8.

### P0: contract and implementation preflight

- [x] P0.1 Record the maintainer-approved ownership, chain boundary and nine-function map.
- [x] P0.2 Record source observations, probe limitations, phase dependencies and acceptance matrix.
- [x] P0.3 Reconcile current roadmap/scope/status references and #447's proposed namespace, without changing runtime contracts.
- [x] P0.4 Record source/worktree, import/native-extension origins and preserved existing changes in C7. Create the isolated runtime branch required by C6 before the first implementation edit; it is not needed for this documentation-only follow-up. Never reset/stash unrelated work.
- [x] P0.5 Record target constructor signatures, missing-state behavior, the editing API map, stable group-free molecule membership, remap/state-alignment policy, coherent cutover and wire contracts in C1-C6; select baseline workloads in C7. Runtime implementation and performance measurements remain pending.
- [x] P0.6 Open the owning suite impact and four client-receiving issues before rollout; the dated execution receipt identifies them and their source-only status. No published minimum version is invented.

Exit: reviewable contract and baseline, including any deliberate exception. Routine
engineering decisions within this plan do not create a new permission round;
changes to scientific scope or compatibility promises need an explicit decision.

### P1: meaningful guards before refactoring

- [ ] P1.1 Characterize existing scientific outputs and supported completeness/participation policies with independent expectations; retain original controls.
- [x] P1.2 Add initial target guards for pure Topology, absent/zero/unknown/complete chemistry and standalone state-only operations. Copy guards reject chemical traversal regardless of the private attribute name. Targets remain intentionally failing until implemented.
- [x] P1.3 Add two-state controls with different bond/component counts, ambiguous reference, structure associations, nonconsecutive indices and failed resolution without source mutation. These define expectations, not passing delivery evidence.
- [ ] P1.4 Freeze lifecycle/codec/consumer examples to port, including group-free molecules, FASTA groups and new managed-prefix composition.

Exit: recorded baseline plus intentionally failing target tests, with causes and
scope explained. Intentional pre-implementation failures are not a passing gate.

### P2: complete native chemical authority

- [ ] P2.1 Move state storage, bond/component table schemas, coercion, validation, concatenation and remapping to native chemical ownership; remove circular imports from ChemicalStates into Topology's chemical implementation.
- [ ] P2.2 Provide supported state-aware bond/component editing, reference handling and rebuild operations; preserve completeness, evidence, dtypes, string IDs and histories.
- [ ] P2.3 Make Topology constructor/copy/compare/reset/extract operate on stable inventory; remove state proxies, chemical counters and mutation methods.
- [ ] P2.4 Preserve component inference policy and explicit stable-context labeling; separate initial molecule inference from later state changes.

Exit: native guards demonstrate independent authorities, no chemistry recovery
through an attached Topology, and proper handling of unavailable/ambiguous states.

### P3: basic/native queries and form contracts

- [ ] P3.1 Replace Topology-scoped chemical-state resolution with chemical-domain resolution and correct state-local index validation.
- [ ] P3.2 Complete ChemicalStates/ChemicalStatesDict get/set/select/has_attribute routes actually supported by their data, and native get/info delivery without universal reconstruction.
- [ ] P3.3 Route MolSys mixed queries through the right domains; remove chemical capabilities from pure native Topology/its latest dictionary schema and review legacy adapters separately.
- [ ] P3.4 Audit the attribute catalogue, element/component helpers, piping, selection engines, count helpers and native provider; preserve missing-field and empty-selection semantics.

Exit: equivalent supported basic/native/form queries return independent expected
values; no declared attribute passes only because a placeholder route exists.

### P4: coordinated builders and lifecycle

- [ ] P4.1 Give MolSysBuilder its own chemical collection, retain multi-state inputs and explicit working-state edits, and publish all atom-axis growth transactionally.
- [ ] P4.2 Decouple MolSys topology/chemistry setters; preserve explicit associations and safe owner binding/replacement.
- [ ] P4.3 Port copy, extraction, remove, permutation, addition/merge, managed-prefix growth and structure append to shared maps and explicit state-alignment policies.
- [ ] P4.4 Preserve current named-analysis invalidation and stale-reference handling through native/public edits; rejection must leave every domain coherent.

Exit: original source remains unchanged for copy-producing operations; supported
edits preserve all relevant domains and unsupported edits fail before publication.

### P5: chemical_states functional module

- [ ] P5.1 Register lazy lowercase module, move all nine public tools and their owning graph helpers, and update internal callers.
- [ ] P5.2 Normalize state selection once; add explicit state/structure arguments to paths/quartets with validated skip_digestion and compatible positional conventions.
- [ ] P5.3 Update scientific attribution/diagnostic callers, dependency metadata, API stability registry/waivers and addon inventory without changing scientific profiles.
- [ ] P5.4 Qualify form parity, state-only prerequisites, finite/empty results, selected source indices and reuse of compiled kernels. Keep sequence tools and chains in topology.

Exit: canonical new APIs reproduce admitted science and resolve the selected
state, with no accidental reference fallback or source mutation.

### P6: producers, conversions and persistence

- [ ] P6.1 Port native/form producers including PDB/mmCIF, SDF/PDBQT, RDKit, MDTraj, OpenMM and supported other engines; retain declared versus inferred/unknown chemistry.
- [ ] P6.2 Implement explicit Topology projections, complete MolSys assembly and partial-domain composition, including honest conversion reports and strict-loss behavior.
- [ ] P6.3 Version dictionary writers/readers and typed JSON transport; preserve old payload reading without chemical Topology intermediates or silent losses.
- [ ] P6.4 Qualify H5MSM 0.5 optional layers, associations and analyses; 0.3/0.4 warnings/migration; preparation history, units and agreed pickle restoration/migration.

Exit: supported full/partial native and file round trips preserve expected data,
absence and source maps; malformed/unsupported payloads fail clearly and safely.

### P7: documentation, instructions and client receiving

- [ ] P7.1 Update CORE_SPECIFICATION, native/query/conversion/invalidation guidance, API references, User Guide Foundations/Toolbox/Cookbook and affected Four Paths modules; execute changed examples.
- [ ] P7.2 Update owned AGENTS instructions for the new domain boundary and native dependencies. Shared synchronized guides stay read-only; request changes in their provider if needed.
- [ ] P7.3 Publish a migration map and deliver consumer handoffs; receive MolSysViewer loaders/addon, DockingMT torsion/correspondence and PharmacophoreMT graph callers, and check TopoMT beyond a simple text search.
- [ ] P7.4 Record exact old/new consumer/provider sources, required routes and pending package availability; preserve unrelated dirty/divergent sibling worktrees and historical evidence.

Exit: no current documentation describes the old facade as the target model;
client source receiving is identified and tested, or a specific unresolved impact
keeps this phase open. Source receiving is not installed/public qualification.

### P8: integration, merge and source closeout

- [ ] P8.1 Run the relevant and full required source tests using the shared Python 3.14 environment, 12 workers and Pytest Receptor; complete Ruff and API/form/dependency/devguide/documentation gates.
- [ ] P8.2 Compare representative scientific values and source/index/units/provenance independently; execute strict documentation and changed notebook/doctest examples.
- [ ] P8.3 Measure representative native query/copy and file/streaming workloads after correctness. Record inputs/environment; reject accidental full trajectory loads, repeated chemistry copies or unbounded scans.
- [ ] P8.4 Merge the coherent result using the authorized local route, publish an unskipped head, inspect exact-source CI with GH Run Receptor and record any missing evidence. No force/reset or PR requirement is introduced here.
- [ ] P8.5 Place final rules in maintained normative guidance, select an actual mechanically addressable regression guard, archive this plan and close #255 with the implementation commit and settled limitations.

Exit: a coherent source delivery, explicit consumer impact and all applicable
executed source gates. Later package/tag/Release/DOI publication needs the separate
exact-candidate approvals and qualification; this plan authorizes none of them.

## Execution receipt — 2026-10-29

This development checkpoint does not complete the migration or qualify a release
candidate. Runtime changes and deliberately failing targets remain on
`dev/chemical-states-separation-255`; main keeps its runtime. Four unrelated API
autosummary edits and all sibling worktrees were preserved. A full temporary
worktree checkout failed and Git removed it; the branch uses the existing
checkout instead. No auxiliary environment or native-extension rebuild was made.

### Coordination and actual receiving state

Advance notices are open:

| Owner | Issue | Boundary |
| --- | --- | --- |
| MolSysSuite | uibcdf/molsyssuite#155 | Cross-client impact coordination. |
| MolSysViewer | uibcdf/molsysviewer#269 | Native-array bonds and maintained caller inventories. |
| DockingMT | uibcdf/dockingmt#56 | Graph/torsion/fragments/correspondence and prepared-source workflows. |
| PharmacophoreMT | uibcdf/pharmacophoremt#69 | SMARTS diagnostics and indirect preparation/state/query consumers. |
| TopoMT | uibcdf/topomt#100 | Indirect Topography audit; no direct dependency proven by the bounded search. |

Refreshed origin/main sources inspected: Viewer
`8903f0659f2833cc979e4072cf60d17e8bcc6ef9`, DockingMT
`8d40870724e21cf579ce4d5289d46b5d8a5aaa1c`, PharmacophoreMT
`87de52f1a13913ed1d941c3a0a6425a979a64b1f` and TopoMT
`6e88237e7e71dcf569613a4a860eaa1d12bcb79d`. Behind/divergent clients and
Viewer edits were not changed. Notices establish no receiving commit, installed
compatibility or new dependency minimum. P7 and final qualification remain open.

### Initial targets and retained baseline

[Test checkpoint 6dcedaa80cc5d3531c67e3483d69fd2e35c15f54](https://github.com/uibcdf/molsysmt/commit/6dcedaa80cc5d3531c67e3483d69fd2e35c15f54)
adds `tests/native/test_chemical_domain_separation.py`: 36 cases using
hand-authored public ChemicalStatesDict inputs, without constructing chemistry
through the Topology implementation being removed. Four passing controls cover
valid fixture decoding, nonconsecutive selected-state queries, independent copies
under controlled assignment and current H5MSM state/association recovery.

The remaining 32 targets fail explicitly: chemical namespace absent, native state
query delivery missing, Topology chemical access/copy coupling, stable molecule
membership absent, owner replacement/Builder associations not migrated,
controlled editing absent and future persistence unavailable. These are not 32
independently diagnosed new regressions. No xfail/skip was added.

Combined with C7's unchanged eight modules, the run returned exit 1: 101 passed,
32 failed, nine warnings in 8.89 s, using `--receptor=llm -n 12`. After storage
extraction, the target module alone returned exit 1: four passed, 32 failed in
13.62 s. These are honest failing development results, not passing source gates.
Implement P2-P6 before merging this module to main; do not weaken its assertions.

### P2 storage foundation

[Implementation checkpoint e1bcedfa43a7a2094fe5bcf8b34af2ee16db56bf](https://github.com/uibcdf/molsysmt/commit/e1bcedfa43a7a2094fe5bcf8b34af2ee16db56bf)
moves three storage classes, their schemas and existing bond-normalization/atom-
remapping helpers to `molsysmt/native/_chemical_state.py`. ChemicalStates creation,
growth, restriction and its typed codec now import their own owner. The three
class bodies and two moved helper bodies retain exact AST equivalence to the
baseline, apart from helpers becoming module functions. Scientific criteria,
units and diagnostic identities were not redesigned.

Topology retains marked private bindings/thin delegation for staged callers and
original pickle paths. Its chemical collection, public facades, mutations and
query plumbing still exist. Bond-table concatenation and remaining native
ownership still need migration: P2.1 is not complete merely because storage
moved. No new public API is exported.

Five controls in `tests/native/test_chemical_state_storage.py` pass. They poison
former Topology gateways while exercising standalone creation/growth/copy, typed
encoding/decoding, restriction and zero-state transport. They also recover the
trusted pre-extraction fixture `tests/native/data/chemical_states_before_separation.pkl`:
4,591 bytes, SHA-256
`a9675d019bce8eccdabb1548efb4349674e07709af9e5be791c0ff96f37c5cf0`.
Its sidecar records original sources/protocol. Legacy paths resolve to one
canonical implementation, not a second store. Current pickles use the new class
owner; forward reading by an older installed provider is not claimed. H5MSM and
dictionary schemas are unchanged.

Executed in C7's shared source environment:

```bash
python -m pytest --receptor=llm -n 12 \
  tests/native tests/basic/get tests/topology \
  tests/form/file_h5msm tests/form/molsysmt_Topology \
  --ignore=tests/native/test_chemical_domain_separation.py
```

Exit 0: **3,785 passed**, 126.43 s, 701 warnings. The command explicitly excludes
the disclosed future targets; it is not a full passing branch suite. Warnings
include legacy H5MSM, existing pandas future warnings and declared attribute/
unit-cell diagnostics; no filters were relaxed. The five new storage controls
and original 97-case selection pass separately; counts overlap the broader run
and must not be summed. Other forms/full-package/final P8 qualification remain.

`ruff check molsysmt` and both new test modules, changed-file Ruff formatting,
`git diff --check` and `validate_dependencies.py` pass. The unchanged native
extension has SHA-256
`f32ed73f7ef3cf3225e12fbc56b9c4236a4452d758c94661f41860ad00d82c1c`.
No dependency floor, environment or attribution boundary changed. Relocating
native storage does not introduce a new scientific method or credit claim.

### Bounded copy baseline and remaining measurements

The existing benchmark ran before runtime edits:

```bash
python devtools/scripts/benchmark_native_copy.py \
  --case 10000x10 --case 1000x1000 \
  --operation deferred_copy --operation eager_copy --operation selected_read \
  --repeats 7 --output devtools/data/chemical_domain_copy_baseline_20261029.json
```

Exit 0. The [immutable artifact](https://github.com/uibcdf/molsysmt/blob/e1bcedfa43a7a2094fe5bcf8b34af2ee16db56bf/devtools/data/chemical_domain_copy_baseline_20261029.json)
identifies test-only producer 6dcedaa80, implementation hashes, environment,
warm-up, seven repetitions, medians, process RSS and separate traced allocation
measurements. It marks the worktree dirty because the preserved API-doc edits
were present; runtime hashes identify the measured code. These two one-state
copy/read controls do not replace C7's multistate, large-atom, group-only,
chemical-edit and projected-file measurements. No post-migration speedup or RAM
reduction is claimed. Preserve original bytes and extend evidence before changing
remaining measured paths.

At that checkpoint, the next work was stable molecule membership and the
remaining chemical-owned primitives. The following receipt records the molecule
work. Owner binding/editing and queries still require the coordinated C6 cutover;
storage relocation alone does not finish P2.

### C1 stable molecule membership

[Implementation checkpoint 77bc140ff0ba4c05df6b537d979333b1aad9c393](https://github.com/uibcdf/molsysmt/commit/77bc140ff0ba4c05df6b537d979333b1aad9c393)
is on `dev/chemical-states-separation-255`, ahead of the final domain cutover.
Main remains at documentary checkpoint `a3eeb2dabf35fdd5abd6aac81b4e5f6e87e049f5`;
this runtime is not merged there. Topology declares ungrouped atom ownership through
`set_atom_molecules(molecule_indices, atom_indices='all')`. Indices are positional;
labels do not qualify. Unknown entries are nullable at the public boundary.
Grouped atoms inherit their group's owner, and conflicting declarations reject
before publication. There is no additional atom-table column. An optional
int64 vector stores only ungrouped ownership, with `-1` for unknown positions;
it is absent when no ungrouped assignment is known and costs eight bytes per
atom when present. This is a storage bound, not a measured whole-object RAM
improvement. Argument digestion preserves strict boolean/integer distinctions
and rejects units, duplicate selectors, malformed shapes and invalid domains.

Atom/molecule queries now project this stable hierarchy rather than consulting
the reference chemical state's components. Initial explicit graph construction
may snapshot a partition once. Bond edits and changes of selected state do not
redefine known molecule ownership. The existing native comparison's molecule
flag now reaches its boolean argument contract and compares the stored map.
Other comparison and state-query migration belongs to P2/P3.

Copying, extraction, atom permutation, native addition and builder atom/group
growth transport the independent vector. Extraction retains molecules reached
only through ungrouped atoms and remaps entities. Addition offsets molecule
positions independently of IDs. Group insertion reconciles the direct vector
with grouped ownership. Rebuilding a component graph can merge two fully
declared molecules without merging their stable hierarchy. A newly added atom
that bridges several declared owners still requires an explicit declaration;
the builder does not choose an owner arbitrarily. Existing explicit unknown
positions are not assigned merely because new atoms were added.

A changed supported declaration stages invalidation of attached named analyses
before publishing membership. Evaluated-empty coverage is invalidated too;
old analysis snapshots and coordinate storage remain intact. No-op assignments
preserve analysis identity. Failure-injection controls verify atomic rejection.

H5MSM root 0.5 now supports topology layer 3 with typed `atom_molecules` and
optional existing `chain_groups` membership. Topology-only reads preserve the
stable map without reading chemistry. Newly unknown group-free ownership also
uses layer 3 with an all-`-1` dataset, so a later joint read cannot mistake it
for the legacy implicit partition. Native storage remains absent in that case.
Layers 1/2 remain readable. Their legacy molecule representation is recovered
only when both domains are decoded with a declared identity atom-axis link and
an unambiguous reference partition matching the molecule inventory. Equal axis
lengths alone are insufficient. A topology-only legacy projection leaves
unavailable ownership unknown. Old native pickle decoding similarly snapshots
its original shared-domain representation once; queries never invoke recovery.

Dictionary 0.2 is not implemented yet. The two legacy 0.1 writers explicitly
reject independent molecule assignments that their schema cannot represent,
rather than silently dropping them. H5MSM is the supported transport for those
declarations during this development checkpoint. The legacy decoder remains in
place; it is not the planned chemical-owner cutover.

Guards are in `tests/native/test_atom_molecule_membership.py` and the extended
`tests/form/file_h5msm/test_topology_v05_probe.py`. Existing hierarchy fixtures
now explicitly clear or reconcile their source declarations before replacing
group tables. Assertions remain; the MDTraj partial-group case covers both
unknown and known molecule ownership, including target-only fallback groups.
The earlier empty-selection case also exercises correctly typed empty indices.

The focused membership/H5MSM selection passes **48 tests** (exit 0, 7.74 s).
Validation in the existing Linux/Python 3.14.7 development environment uses
`pytest-receptor` and twelve workers. The broad command above, excluding only
the explicitly unfinished target module, executes **3,830 passing tests and one
network-dependent failure** (188.31 s). The failing 2NZT alignment control passes
separately in 8.99 s when DNS/network access is available. These are split
results, not a single exit-zero broad run. The prior C1 iteration passed all
3,828 tests before the three final H5MSM controls/reader refinements. No tests
were skipped, marked xfail or weakened to conceal incomplete work.

The 36 future targets now report **6 passed, 30 failed** (exit 1, 5.77 s), compared
with the storage checkpoint's 4/32. Remaining failures include pure Topology
ownership/copy isolation, explicit chemical-state queries, MolSys/Builder
association preservation, state editing, dictionary 0.2 and the functional
namespace. These are required implementation work, not release-qualified
expected failures. Do not merge runtime changes to main while they remain.

Eight doctests pass across Topology and the two modified dictionary writers.
The Topology foundation, API reference, form Toolbox, group-free Cookbook,
H5MSM guide/specification and Common Core Module 4 now explain the implemented
declaration and persistence behavior. All three affected notebooks execute
successfully in the development environment; previous executable examples are
retained. Public API stability, docstring fidelity, course structure, Ruff and
dependency validation pass. Four pre-existing unrelated API-RST edits and the
native binary retain their original hashes. No dependency floor, environment,
scientific method or attribution requirement changes.

An initial full HTML build exhausted temporary-storage quota while copying
large static views. A concurrent repeat of write tests reported quota errors
and two HDF5 worker crashes under that condition; it is not passing evidence.
Only this checkpoint's failed build directories were removed. The subsequent
broad test result above is after that cleanup. Static-view duplication is not
necessary to validate the edited references. A subsequent full-source HTML
structure build using the Sphinx Python API, twelve workers,
`autosummary_generate=False` and an explicit `html_static_path=[]` succeeds
(exit 0). Extension/theme assets remain; repository static views are omitted
from this diagnostic output. Two existing `_static` README toctree warnings
remain, with no warnings for the edited API/pages. This is reference/HTML
structure evidence; it does not qualify the complete deployed assets or replace
the final P7/P8 documentation and exact-candidate gates.

Next: finish the remaining chemical-owned primitives, then coordinate native
owner binding, state-aware editing and query dispatch under C6. The nine moved
functional APIs, pure Topology, dictionary 0.2, final client receiving and C7
performance measurements remain pending. This checkpoint does not close #255,
qualify a release or deliver a new minimum package version to clients.

### P2 chemical primitives and C4 induced-graph restriction

[Implementation checkpoint 595a35ad9d7d53470a6e3930cc2fd26e02054dde](https://github.com/uibcdf/molsysmt/commit/595a35ad9d7d53470a6e3930cc2fd26e02054dde)
on `dev/chemical-states-separation-255` moves bond-table concatenation to
`native/_chemical_state.py` and graph partition/exact component matching to
`native/_chemical_components.py`. The temporary Topology and `_topology_infer`
gateways delegate to those owners; chemical-template validation now calls the
chemical primitives directly. The graph kernel is the existing Rust component
routine with the same stored `joins_components` participation convention. This
does not introduce another connectivity algorithm, a dependency or a new
scientific credit claim.

The strict ordered chemical-inventory comparison also moves to ChemicalStates.
It compares atom cardinality, raw reference selection, ordered states, the
existing scientific metadata and all four stored tables/vectors without resolving
a reference or changing the collection. Preparation history remains outside this
chemical-change comparison, as before. Topology still checks its stable tables
and then delegates during this staged migration. MolSys append still uses that
temporary gateway; its final domain-aware cutover remains P4.

Native atom restriction no longer invokes legacy normalization on source
records. Chemical-owned validation checks atom-row alignment, positional
component rows, nullable integer memberships, component-index bounds and atom
assignments before staging a result. Misaligned unknown vectors and invalid
memberships reject without repairing or mutating the source. Legacy decoding
retains its explicit compatibility path. This is not a claim that every mutation
and codec validation path has already migrated.

C4 restriction now distinguishes complete and incomplete stored connectivity:

- A complete source graph yields components of the selected induced graph.
  The analytical path 0-1-2 restricted to [0, 2] yields two components while
  retaining one declared stable molecule. The reference/state order and structure
  associations do not change. Component labels transfer only for exact full
  source atom sets; changed components get local string IDs and unknown names/
  types. Exact unchanged complete declarations retain their evidence; newly
  inferred partitions record inferred evidence. Unknown bond participation keeps
  the existing conservative component-completeness limit.
- Partial/unavailable connectivity restricts declared memberships and compacts
  retained rows without inferring a complete partition. If a retained complete
  component declaration is cut, its completeness becomes partial; unavailable
  stays unavailable. Removing entire components while retaining other complete
  declarations does not downgrade the unchanged retained components.
- All retained bond atom references use the existing canonical remapper.
  Reversed endpoints also swap their endpoint-local stereo neighbors, while
  donor/acceptor roles follow their original atoms. A removed stereo neighbor
  clears both references and the incomplete annotation; wholly unknown optional
  fields remain unmaterialized. The new reversed-order control exposed and
  guards the previously unrequested canonical-order option in this path.

No cap/H generation, aromaticity perception, chemical-state selection or
interaction recalculation runs during extraction. Complete induced connectivity
does not certify a prepared standalone chemical fragment. Historical preparation
records retain their original operation-index scope.

`tests/native/test_chemical_state_storage.py` now has 28 passing cases, including
Topology-gateway poisoning, dtype/null-preserving bond concatenation, strict
inventory comparison, complete versus incomplete restrictions, exact metadata
matching, empty/reordered domains, source immutability, malformed membership
rejection, participation overrides and directional/stereo remapping.
The stereo control also exercises public extraction of a topology-free MolSys
and a chemical-only H5MSM round trip, preserving the remapped endpoint roles
and component label. The final 28-case owner selection passes in 5.28 s.
Existing native component-metadata, rich-bond, extraction/removal and chemical-template
controls are retained. No assertion was weakened or future target marked xfail.

Executed in the same Linux/Python 3.14.7 development environment:

```bash
python -m pytest --receptor=llm -n 12 \
  tests/native tests/basic/get tests/topology \
  tests/form/file_h5msm tests/form/molsysmt_Topology tests/element/component \
  tests/physchem/test_chemical_template*.py \
  tests/basic/test_extract.py tests/basic/test_extract_extended.py \
  tests/basic/test_remove.py tests/basic/test_remove_extended.py \
  tests/basic/test_remove_ownership.py \
  tests/build/add_terminal_atoms/test_component_hydrogen_reinsertion.py \
  --ignore=tests/native/test_chemical_domain_separation.py
```

Exit 0: **4,104 passed**, 88.90 s, 766 warnings. This selection explicitly excludes
the unfinished contract targets and is not a full branch/release qualification.
The earlier 132-case extraction/removal selection and 28-case chemical-owner run
pass separately but overlap this broader run; do not sum their counts. Final
execution uses a fresh ignored repository-cache temporary directory through
`TMPDIR`/`--basetemp`, with network access for existing public-PDB controls.
An earlier, narrower sandbox run passed 4,001 tests and failed only at DNS;
a later expanded run was interrupted by temporary quota/HDF5 worker errors.
Those are not passing evidence. Completed owned pytest data were removed;
the successful final run's temporary payloads were automatically removed too.
No environment or package was installed or replaced.

The target module now has **7 passed, 29 failed** (exit 1, 6.55 s). The newly
passing target is complete-path restriction with independent molecule identity.
Pure Topology, independent MolSys/Builder ownership, state-aware queries/editing,
the functional namespace and dictionary 0.2 still require implementation before
runtime merges to main. P2.1 remains open for the remaining normalization/
assembly paths and their coordinated consumers; these moved primitives alone
do not complete native chemical authority.

Fifteen doctests pass across basic.extract, MolSys, Topology and ChemicalStates.
The extraction Toolbox, group-free Cookbook and Common Core Module 18 execute
successfully; the MolSys foundation and manifest now describe complete versus
partial restriction and source-index scope. Two schema-4.4 notebooks initially
received unsupported cell IDs for the inserted cells; removing only those three
metadata fields preserves source/output payloads. The source notebook-schema
guard then passes all 496 cases. Public API stability, docstring fidelity, course
structure, dependency validation and Ruff pass. The four unrelated API-RST edits
and native binary are preserved. C7 performance comparison, final client
receiving and P8 exact-source qualification remain pending.

The HTML structure build succeeds with twelve Sphinx workers and repository
static views omitted, using the same explicit Python-list override as the C1
checkpoint. All four edited conceptual/tutorial pages and their expected new
sections are present in HTML. The source-schema repair removes the initial
notebook JSON diagnostics; no errors remain. The two existing `_static` README
toctree warnings remain. Diagnostic HTML/doctrees are stored in ignored repository
cache, avoiding another large `/tmp` asset copy. This does not qualify final
deployed static views or replace P7/P8 documentation gates.

Next: implement the admitted C3 selected-state editing/rebuild boundary using
these owned primitives, then move query dispatch and MolSys/Builder ownership
together under C6. Do not add new scientific profiles during that cutover.

### C3 selected-state graph editing and component reconstruction

Implemented in development commit
[`6f632c0e16243bfe5300daf77a0eda68380fde90`](https://github.com/uibcdf/molsysmt/commit/6f632c0e16243bfe5300daf77a0eda68380fde90):
native `ChemicalStates.add_bonds`,
`remove_bonds` and `rebuild_components` with the C3 signatures. They use ArgDigest
and keyword-only state selection/skip_digestion. Reference resolution selects
one existing state without changing the reference. Absent, zero-state, ambiguous
and invalid selections reject before editing, including otherwise empty input.
Indices are positional, state-local for bonds, and reject boolean, fractional
or unitful inputs. Repeated removal indices delete a row once. No-op graph edits
retain table/component/analysis identity.

Only the affected state's graph/component data are staged. Bond normalization,
component reconstruction and required analysis invalidation all precede field
publication. Kernel, label-inference or invalidation allocation failures do not
publish bonds/components. Success preserves coordinates, atom assignments,
producer-history objects, unrelated states, the reference and structure-state
associations. Held bond tables and analysis snapshots remain their old values
when supported edits replace current data. No constructor or chemical gateway
of Topology is invoked by standalone editing.

Scientific graph/completeness changes conservatively invalidate all named
analyses of the owner, including evaluated-empty coverage. Label-only component
reconstruction preserves component evidence and observations. The publication
path uses already prepared fields, not an eager copy of MolSys, coordinates or
unrelated chemical states. Default reconstruction does not allocate exact-
component matching work when every label will be regenerated; a poisoned-matcher
guard enforces that bound. This is not a measured whole-workflow speedup; C7
timing/RAM comparisons remain pending.

Source inspection also identifies an existing scaling limit retained by the
shared label criteria: type/name inference forms a full group mask for each
component, with worst-case work proportional to components times groups. C7
must include solvent-rich many-component context and compare grouped lookup
before claiming large-system editing throughput. This checkpoint establishes
ownership and transactional correctness, not an optimal labeling implementation.

Edges added by pair alone retain unknown order/type. Unavailable connectivity
becomes partial, not complete, after an edge is declared. Rebuilt components
use the existing joins_components/Rust partition criterion; unknown participation
does not certify completeness. Removing known edges preserves the prior
connectivity-completeness limit. Complete known empty graphs can have isolated
components; an unavailable empty table is not silently promoted to known absence.

An explicit native Topology, or an owning MolSys's topology when available,
provides stable group context. Matching atom cardinality is checked; supplying
context declares positional correspondence rather than proving identity. Context
is not mutated or queried for bonds/components. Existing group recognition and
component type/name criteria are reused. Their implementations now accept
explicit membership/context in the chemical owner; legacy topology inference
delegates to the same criteria. Missing typing can be inferred from explicitly
nullable stable metadata without changing it. Inadequate evidence remains
missing, including unsupported generated-name cases. Unrequested labels retain
their original dtype and transfer only across exactly unchanged full atom sets.

The shared component-type classifier previously had no result for a declared
nucleotide group with a missing/unrecognized DNA/RNA name. It now returns
unknown for that case; controlled rebuilding leaves the resulting type/name
missing. This is a conservative missing-evidence fallback, not a new recognition
profile. Both missing and unknown names have regression controls. The separate
stable-constructor normalization remains part of P2.3: some current default group
label columns contain literal `"nan"` strings. Explicit nullable metadata is used
by the missing-context controls; no consumer-specific replacement store or
silent constructor rewrite is introduced in this checkpoint.

The logical `force` flag has a decorator-scoped boolean contract; existing
physical-force unit digestion retains its old route. Native context validates
its type, and native state editing does not admit a structure-scoped selector.
No dependency floor, quantity policy, native binary, scientific detector profile
or attribution boundary changes. Existing criteria and compiled kernels are
reused rather than claimed as a new scientific method.

`tests/native/test_chemical_state_edits.py` adds 50 passing cases. They reuse the
analytical public wire fixtures rather than constructing chemistry through a
Topology. Controls cover state selection, index domains, absent/ambiguous states,
empty/idempotent edits, exact labels and dtypes, complete versus unavailable
graphs, atomic kernel/invalidation failure, retained assignments/history/maps,
unmodified coordinate storage, explicit context without chemical traversal,
incomplete nucleotide context and absence of hidden Topology construction.
Existing component-metadata and chemical-storage guards are retained.

The same broad command as the preceding checkpoint, with repository-cache
`TMPDIR`/`--basetemp` and public-PDB network access, now executes **4,154 passed**
(exit 0, 109.49 s, 767 warnings) with Pytest Receptor and twelve workers. It
includes the new edit module and explicitly excludes the still-unfinished
target module. The earlier 4,152-case run and focused owner/context selections
overlap this result; do not sum them. Successful run temporary payloads were
removed automatically. The environment remains the shared Linux/Python 3.14.7
development environment, with no installs or auxiliary environments.

The 36 original targets now report **10 passed, 26 failed** (exit 1, 10.41 s).
The three newly passing targets cover selected-state removal, failed component
staging without chemistry/analysis publication, and successful invalidation of
evaluated-empty coverage. Those remaining failures are required native ownership,
query/dispatch, builder/association, functional-module and dictionary work; they
are not waived release tests. P2.2 remains open for the remaining private
assignment/edit routes and their coordinated consumers. This is not a main merge
or an installed-candidate qualification.

All seven ChemicalStates doctests pass. Source notebook-schema guards pass
496 cases; Common Core Module 4 and the group-free Cookbook execute successfully
against the final implementation. The new ChemicalStates foundation and native
editing Toolbox expose availability, selector/reconstruction modes, staged
publication, stable context, completeness and mutable-table limitations. The
API reference documents all four implemented methods, including get_bonds, and
course inventory/navigation/manifest are updated. The class remains experimental
in the stability registry; its documentation/guard pointers now identify the
chemical owner. Standalone general get/set/query delivery remains explicitly
pending P3 rather than being advertised by the new editing surface.

The final HTML structure build succeeds with twelve Sphinx workers and the
explicit empty repository-static-path override used in previous checkpoints.
The new foundation/Toolbox pages, both executed notebooks and all four method
anchors are present. There are no parser/API errors or edited-page warnings;
the same two `_static` README toctree warnings remain. Large deployed static
views are not duplicated by this diagnostic build. Notebook fingerprints match
the final code cells, and all preceding executable examples are retained. The
four unrelated RST edits and the native extension retain their recorded hashes.

Next: move the remaining private chemical assignment/edit boundaries and the
state resolver/query providers to ChemicalStates. Keep that work coordinated
with MolSys/Builder independence and the nine-function namespace move under C6.

### C3 continuation: typed assignment authority and scoped resolution

Development commit
[`997684a9356578943a682ca44fc51a5eb49c0c4f`](https://github.com/uibcdf/molsysmt/commit/997684a9356578943a682ca44fc51a5eb49c0c4f)
moves private atom assignments/removal, bond-field and stereo-reference assignment,
component membership and prepared bond publication into ChemicalStates.
Topology's corresponding methods are temporary delegates,
not a second implementation/store or a newly promised public compatibility API.
Removing those delegates remains part of C6. No public signature, dependency floor,
wire schema, scientific detector criterion or unit policy changes in this block.
Existing formal-charge adapter boundaries still normalize elementary-charge
quantities before calling the typed storage owner.

Selected-state scopes are keyed by the collection in a ContextVar owned by
`native/chemical_states.py`. The public orchestration decorator resolves MolSys's
chemical collection directly, including a chemical-only MolSys, or an explicitly
supplied standalone ChemicalStates. Repeated complementary references to the same
collection are deduplicated. It no longer enters Topology's state context for a
MolSys. The explicit legacy Topology route remains admitted on the development
branch until producer/query cutover. Scope entry validates first; nested failure
restores the previous scope and never rewrites the reference. Separate collections
and concurrent read contexts remain independent. This is not a concurrency
guarantee for mutations of a shared collection.

Reading stored atom assignments or component membership no longer invokes
`_ensure_compatibility`, which could replace aligned vectors or normalize columns
during a read or before a later rejected assignment. Legacy repair remains at
decoding/construction boundaries. Assignments validate source alignment and prepare
their affected replacement before owner invalidation/publication; they do not
normalize the source in place. Absent/ambiguous state access fails before mutation,
and the collection does not invent a state for private assignment. The historical
zero-state Topology construction branch remains explicitly temporary under C6.

Typed atom fields retain their nullable dtype/value rules. Bond row selectors are
validated against the selected state's own table without truncating fractional
values or interpreting booleans as indices. Stereo references are prepared and
validated as a pair before publication. Scientific assignments conservatively
invalidate the owner's observations, including evaluated-empty coverage, without
materializing coordinates. Failures in value validation or allocation for
invalidation preserve every stored state field and analysis snapshot. Other
states, producer history and structure associations remain outside the edit.

The broad regression exposed an existing producer dependency: Topology merge
updated its collection's atom count but relied on a later field assignment to
repair zero-length atom-state rows. It now explicitly extends the collection's
atom domain during unpublished construction before assigning membership or
attributes. This fixes the producer instead of restoring repair in query/set
paths. The complete MolSys/Builder/producer ownership migration remains pending.

A new lossless-wire control exposed a second subtlety: normalizing a bond-ID-only
edit could materialize implied joins_components defaults, sort rows or discard
all-null optional columns. A label edit now validates without publishing those
unrequested normalization effects. It preserves stored row positions and nullable
columns, changes only string labels, and retains evaluated interaction coverage.
Canonical scientific-field/table replacement still uses the existing normalization
rules. Low-level membership/table staging is not chemical perception or automatic
component reconstruction; the public C3 graph operations supply reconstruction.
General selected-state attribute delivery and supported standalone assignments
remain P3 work, not capabilities advertised by these private methods.

`tests/native/test_chemical_state_assignments.py` adds 41 controls, including
independent wire inputs, no hidden Topology construction/legacy repair, selected
state dtypes, rejected selectors, nested/thread-local scopes, collection-based
public resolution, scientific/label-only invalidation and injected allocation
failure preserving every state-field identity. Two existing molecule-identity
controls now enter the chemical owner's scope instead of writing the removed
Topology ContextVar directly; their independent molecule expectations remain.

The established broad selection now reports **4,195 passed** (exit 0, 99.89 s,
769 warnings), using Pytest Receptor, twelve workers and the same Linux/Python
3.14.7 development environment. As before, the unfinished 36-target module is
explicitly excluded. Its separate final run reports **10 passed, 26 failed**
(exit 1, 5.86 s). Their required ownership/attribute/builder/namespace/dictionary
work remains open; no xfail/skip or relaxed expected value was introduced.
Focused runs overlap the broad selection and are not additional passing cases.
The source has not become a coherent main or installed release candidate.

All seven ChemicalStates doctests pass. Common Core Module 4 and the group-free
Cookbook execute against this implementation (7.8 s and 8.6 s); every preceding
source cell remains unchanged and execution fingerprints match. The native
foundation and Toolbox explain controlled metadata publication, label-only
preservation and source-read behavior. Their rendered HTML is verified; the
twelve-worker structure/reference build succeeds with the same two `_static`
README toctree warnings and no new errors. This diagnostic uses the previously
documented empty repository-static override, not deployed-view qualification.

Ruff, formatting for changed Python files, docstring fidelity, dependency
validation, course structure, API registry and public signature comparison against
`b14b799b91f8e2f4d48eaa56b2dc7559a724d088` pass. A read-only probe confirms native
and universal atom-domain queries with chemical_state=1 on a chemical-only MolSys,
without a Topology or reference change; it does not certify general chemical
attribute delivery. No packages/environments were installed, and the existing
native extension and four unrelated RST edits retain their recorded hashes.
Successful and resolved-failure test payloads are removed; compact logs remain
in ignored qualification cache.

Native query, copy and remap performance comparisons in C7 remain pending; no
speedup or memory improvement is inferred from moving authority or passing
correctness controls. Next: deliver state-local attribute/count providers and
their native/basic query contracts, coordinated with the MolSys/Builder authority
cutover rather than adding another chemical facade.

### P3 first slice: stored axes, counts and declarations

Development commit
[`2c69fcc1208df7c3f46afe2dab5eed7041a85951`](https://github.com/uibcdf/molsysmt/commit/2c69fcc1208df7c3f46afe2dab5eed7041a85951)
adds the first standalone native/basic get slice for stored atom, bond and
component positions, selected-state counts, membership and component
incident counts. Collection inventory (state indices, IDs, count and reference)
remains collection-wide. Connectivity/component completeness and component
evidence return the selected state's stored scalar declaration. These are new
ChemicalStates capabilities; legacy Topology/MolSys metadata providers have not
yet been changed to this scalar delivery contract.

Numeric selection and masks resolve bond/component cardinalities in the active
state, not the reference or another state's table. Explicit order/repetitions,
empty shapes and basic.get's sorted mask intersection are preserved. Common
index validation also rejects mixed boolean/integer lists, which previously
could be coerced to integer positions; Boolean masks remain supported. The
corresponding native/universal controls cover this accepted P3.1/P3.4 boundary.

A zero-state collection still supplies its atom domain and state inventory.
Its chemical counts fail as unavailable rather than returning a fabricated zero.
An existing unknown state can have zero stored edges/components and unavailable
completeness; a complete edge-free graph remains distinct. Inventory reads do not
require an unambiguous reference, while state-dependent reads do. Explicit state
selection never changes the reference or source storage. `has_attribute` retains
the distinction between materialized values and supported include_none routes.

Atom incident counts include edges to unselected atoms. Component counts include
each internal edge once and each cross-component edge at its known incident
components, independently of the joins_components partition criterion. Unknown
membership is not assigned to a component, and empty declared component rows
remain represented. An explicit atom selection counts distinct known component
memberships; 'all' retains the existing full declared-inventory convention.
Membership projections reject invalid stored references rather than silently
mapping them to another row.
These reads do not reconstruct a partition or perceive chemistry.

The owning private query module operates on resident typed arrays/tables. Numeric
native get avoids universal discovery, selection/conversion and compatibility
repair; controls poison those routes. Existing parent/child grouping from native
hierarchy is factored into a shared private membership-packing primitive and
reused for component members and atom/bond incidence. Counts use NumPy's compiled
bincount, not nested Python scans over every atom/component or an atom-pair matrix.
These are internal representation helpers, not speculative public utilities.
No Rust kernel, dependency, unit policy, schema, detector criterion or scientific
attribution boundary changes. This block reads stored assignments rather than
executing a new published scientific method.

`tests/native/test_chemical_state_queries.py` adds 94 independent native/universal
cases with analytical wire inputs. Besides parity, expected literal values cover
state-local bounds, incident/cross-component counts, masks, invalid boolean and
fractional indices, unknown membership, empty component rows and complete versus
unknown chemistry. All stored field identities/evidence stay unchanged, and
numeric native calls cannot construct a Topology or enter universal discovery.
The pre-existing common native alias/mask/bounds control now also includes the
ChemicalStates position. An intermediate focused run reports 150 passed, including
the first 93 cases and the common native module; overlapping checks are not additive.
The additional allocation guard checks a cardinality-only query over a
one-million-atom zero-state domain. Full-axis cardinality reads use the stored
count without enumerating atom or component positions. After dispatch warm-up,
the guard permits ordinary API bookkeeping but rejects allocating a million
positions. A controlled negative run returns the correct count while injecting
that list: the guard rejects its 39,997,231-byte traced peak against the generous
1,000,000-byte allowance (expected test exit 1, driver exit 0). This demonstrates
that numerical correctness alone cannot satisfy the memory guard.

A bounded allocation probe uses one warm-up and seven repetitions of
`collection.get(element='atom', n_atoms=True)` on
`ChemicalStates(n_atoms=1_000_000)` with zero states. With tracemalloc active,
the measured median is 0.657 ms and the maximum new traced peak is 8,448 bytes.
This fixture contains no atom records, bonds, states, coordinates or structural
payload. These are warmed Python-allocation observations for this metadata call,
not whole-process RSS, full-system memory, cold-start throughput or a comparison
against the C7 baseline. The final benchmark work remains necessary.

At this stored-axis checkpoint, rich atom/bond fields, component labels, general
standalone set/predicate delivery, ChemicalStatesDict query piping and mixed
MolSys/Builder/provider cutover remained open. The next receipt records the
subsequent field/label slice. Existing get_bonds still supplies
the documented live interchange view. Reference-scoped info can summarize
supported resident counts and component membership; it has no new public
chemical_state selector in this checkpoint. A group-level query requiring stable
context rejects instead of inventing hierarchy. The updated foundation gives an
explicit element/attribute route table instead of advertising complete migration.

The original target module now reports **17 passed, 19 failed** (exit 1, 5.96 s),
up from 10/26. The seven newly passing targets cover standalone selected-state
counts, state-local bounds, failed/ambiguous resolution, absent versus zero-state
domains and complete edge-free versus unknown connectivity. Remaining required
targets are not waived, skipped or merged into main as a passing gate.

The final broadened regression includes `tests/basic/select` and the public
structure-index controls in addition to the preceding checkpoint's selection.
It reports **4,485 passed** (exit 0, 105.51 s, 773 warnings) with Pytest Receptor
and twelve workers, excluding the still-required target module explicitly.
An earlier 4,484-case run had one unchanged fresh-interpreter Ackredit-absence
control time out at 60 s. That control passes alone in 3.76 s, and the unchanged
complete selection then passes 4,484 cases in 107.68 s before the final allocation
guard is added. No timeout, test expectation or scientific control was relaxed.
The original failure is retained here; its root environmental cause is not
established, and overlapping runs are not summed.

All nine native ChemicalStates/query doctests pass; basic.get's bundled-system
doctest also passes (one module case, 13.51 s). The final Common Core Module 4
and Cookbook examples execute in 9.7 s and 8.6 s. Their new stored-state queries
are rendered in HTML, every preceding code example remains, and code fingerprints
match executed sources. The foundation route table, Toolbox, API reference,
course inventory, manifest and scoped content contracts are updated. The
twelve-worker reference/structure build succeeds with the same two `_static`
README toctree warnings and no new errors, using the previously documented empty
repository-static override rather than qualifying deployed views.

All 97 form-adapter structural/delivery-ratchet checks pass, including the newly
declared ChemicalStates routes. Ruff, changed-file formatting, docstring fidelity,
dependency checks, course structure, API registry and signature comparison against
`fdd4ca6a41deb0c8f0354a51df33d714864f0f97` pass. Public signatures, the shared
Linux/Python 3.14.7 environment, the recorded native binary and four unrelated RST
edits are unchanged; no package or auxiliary environment was installed. Resolved
test payloads are removed; compact logs and allocation probe data remain in
ignored qualification cache.

Integrated C6/C7/client qualification remains pending. No overall timing or memory
improvement is claimed merely from using resident providers. Next: extend the
chemical owner's actual field/label providers and selected-state assignment
dispatch, then coordinate them with MolSys/Builder and codec ownership cutover.

### P3 second slice: nullable stored fields and component labels

Development commit
[`4332d3bd8efaf54109ec096d17e9c3204589fa64`](https://github.com/uibcdf/molsysmt/commit/4332d3bd8efaf54109ec096d17e9c3204589fa64)
extends standalone ChemicalStates native/basic get with seven stored atom
assignments, twelve public bond attributes and state-local component IDs, names
and types. Component labels project onto atom positions through declared nullable
membership. The native chemical owner holds field mappings, availability and
projection; thin decorated form getters expose those existing catalogue names.
These are **Contract-tested** and **Parity-tested** stored-data routes, not new
chemical perception or independently validated preparation methods.

An absent atom-property column returns None; a materialized column retains one
nullable value per selected atom. Missing bond fields retain edge cardinality,
including two independently nullable atom references for bond stereochemistry.
Empty selections retain the documented shapes. False/zero remain available
assignments. IDs remain string labels rather than positions. Masks, repetitions,
selected-state bounds, unavailable/ambiguous errors and reference restoration
remain consistent with basic.get. Selected component labels never index unknown
membership as the last component. Queries do not create states, rebuild graphs,
normalize assignments, copy full state tables or modify other states/history.
Formal charge retains the existing discrete Int16 schema and integer multiples
of the elementary charge; it is neither a partial-charge quantity nor a summed
system charge. No unit policy, detector, compiled primitive, schema or attribution
boundary changes. Reading stored evidence does not earn execution credit for the
scientific method that originally produced it.

Full-axis field reads avoid enumerating row positions, and small component-label
selections project the requested membership rows before integer conversion and
reference validation. An allocation guard preallocates a one-million-atom
unknown-state membership, warms dispatch and traces only the query for two atom
positions. Its generous 1 MB allowance rejects full-axis materialization. A
controlled negative variant reads the entire membership before selecting the
same two rows: values still match, but the guard fails at **11,011,854 bytes**
(expected pytest exit 1, control driver exit 0). This is an allocation regression
control, not whole-process RSS or a general speed/memory benchmark.

Verification on Linux/Python 3.14.7 in the existing development environment:

- The established native/basic-get/basic-select/topology/H5MSM/component/template
  and extraction/removal regression, extended with the new native fields and
  ChemicalStates form tests, reports **4,599 passed**, exit 0, **107.94 s**,
  776 warnings. The unfinished target-contract module is selected separately.
  Runtime sources are unchanged across that run and the final focused run below.
- Final field/form/previous-axis/rich-bond selection reports **214 passed**,
  exit 0, **6.70 s**. This includes the revised allocation guard and 114 new
  native/form cases; counts overlap the broad regression and are not additive.
  Literal expectations use independently spelled typed wire records, not the
  production field mappings. Direct adapter bounds, missing/all-null fields,
  False/zero, independent stereo references, detached results, source table
  identity/content, no discovery/repair/Topology construction and dictionary/
  chemical-only H5MSM 0.5 round trips are covered.
- Native query/ChemicalStates doctests report **9 passed**, exit 0, **0.56 s**.
- The original target-contract module remains **17 passed, 19 failed**, exit 1,
  **5.87 s**. Its outstanding pure-Topology, MolSys replacement, Builder,
  dictionary association and new functional-namespace requirements are unchanged;
  no test is skipped, xfailed or weakened to claim migration completion.

Reproducible final focused checks:

```bash
python -m pytest --receptor=llm -n 12 \
  tests/native/test_chemical_state_field_queries.py \
  tests/form/molsysmt_ChemicalStates \
  tests/native/test_chemical_state_queries.py \
  tests/native/test_rich_bond_public_attributes.py
python -m pytest --receptor=llm --doctest-modules \
  molsysmt/native/queries.py molsysmt/native/chemical_states.py \
  molsysmt/form/molsysmt_ChemicalStates/get_chemical_attributes.py
python -m pytest --receptor=llm -n 12 tests/native/test_chemical_domain_separation.py
```

Foundations, Toolbox, API notes, course Common Core 04 and the group-free Cookbook
now explain the same stored-field contract. Both notebooks execute (7.3 s and
7.6 s), preserve all previous code cells and retain executed outputs/fingerprints.
The Cookbook contrasts known zero/False reference assignments with an unknown
alternative. Sphinx HTML succeeds with the established diagnostic static-assets
exclusion and two pre-existing static README toctree warnings. Rendered sections,
anchors and nullable examples are inspected; this is not deployed-view testing.

The maintained `devtools/scripts/validate_course.py` confirms 156 modules. The
obsolete duplicate under `docs/content/course/devtools/validate_course.py` was
also invoked and still rejects its old template (0/156), as already recorded
under #304; it is not a newly failing course/release gate. All 97 adapter
structural/delivery-ratchet checks, Ruff/formatting, docstring validation,
optional-import checks, 277-symbol registry and signature comparison against
`69aaf8b5dbe81f77bd35c1159705b5bfea17960a` pass. The native binary and four unrelated
RST edits are unchanged. No dependency/environment installation, main merge,
release or tag is included. Successful test payloads are removed; compact logs
remain in ignored `chemical-domain-255-qualification` cache.

**Next at that checkpoint:** selected-state assignment delivery using the existing chemical owner's
validated staged setters; then dictionary/predicate and mixed-owner routing,
MolSys/Builder ownership, functional API/codec cutover and C7 receiving checks.
P3 as a whole and #255 remain open. Topology's temporary delegations and the
separate live-table mutation limitation remain explicit until coherent C6.

### P3 third slice: standalone atom/bond assignment

Development commit
[`faa783d5aa4798ce652de17ea35b20fe450bea7d`](https://github.com/uibcdf/molsysmt/commit/faa783d5aa4798ce652de17ea35b20fe450bea7d)
provides `msm.set(chemical_states, ..., chemical_state=...)` for all seven stored
atom assignments and twelve rich bond fields. Thin decorated form setters reuse
the chemical owner's existing staged atom/bond primitives through one private
mapping/selection helper; they do not reconstruct Topology or introduce a second
chemical store. Attribute-inferred destinations and explicit atom/bond selectors
are supported. These routes are **Contract-tested** and **Parity-tested** as
stored assignments, not new scientific preparation methods.

Resolve the selected state before editing, including empty selections. Missing,
invalid and ambiguous states reject without implicit creation/reference changes.
Values follow ordered unique selected positions. Scalars broadcast; None records
unknown values, retaining nullable columns. A first subset atom assignment leaves
unselected atoms unknown. Repeated write positions reject rather than choosing
an ambiguous value; read-only repeated selections remain supported.

One attribute stages typed validation and owner invalidation before publication.
Failure retains source table identities, analysis objects and geometry. Other
states, preparation history, reference and structure associations remain intact.
A controlled edit through `molsys.chemical_states` conservatively invalidates all
named analyses, including evaluated-empty coverage; old analysis snapshots retain
their old contents. A multi-attribute basic.set call is a sequence of independent
assignments, not one transaction across attributes. This new staging statement
applies to the standalone/alias ChemicalStates route; final MolSys/Topology
adapter cutover remains pending.

New public-boundary controls exposed and corrected these concrete defects:

- Nullable aromaticity, hydrogen-count, unpaired-electron and stereochemistry
  setters rejected scalar None. Assignment contexts now accept it without
  relaxing existing get/compare query-flag handling.
- Native integer atom fields could accept booleans as counts. The canonical
  chemical storage validator now rejects them. Formal-charge digestion also
  checks Int16 bounds before narrowing and rejects boolean counts; typed missing
  values remain supported. Formal-charge quantities explicitly extract in
  elementary charge, reject nonfinite/fractional values and retain the existing
  integer-count output/schema. A real nondefault Coulomb/angstrom application
  context and default elementary-charge/nm context both pass.
- A bond-ID-only edit could promote unavailable connectivity to partial and
  consequently invalidate observations. An independent control reproduced that
  promotion; label publication now preserves the original declaration as well
  as row layout, nullable columns and named analysis identity.

Bond metadata retains existing canonical normalization, participation/evidence
and stereo-reference checks. Metadata assignment does not automatically rebuild
components; use the explicit reconstruction method after changing participation
when requesting the modified graph partition. A public test records the stored
partition before, and reconstructed partition after, that operation. Review this
explicit-reconstruction/declaration boundary during C6 rather than accidentally
introducing different behavior in the new form adapter. No new perception,
force-field protocol, compiled kernel, schema, dependency or scientific-credit
boundary is included.

Executed in the existing Linux/Python 3.14.7 development environment:

- Extended native/get/select/topology/H5MSM/component/template/extract/remove
  regression plus affected basic-set and argument-digester suites: **5,085 passed**,
  exit 0, **98.69 s**, 775 warnings, Pytest Receptor with **12 workers**. The
  unfinished target-contract module is selected separately. No auxiliary
  environment or installation is used.
- Final selected public/private assignment, nullable query and direct-form
  controls: **224 passed**, exit 0, **6.65 s**. There are 69 new public/direct-form
  cases. They cover literal value/dtype/null expectations, selected-state bounds,
  malformed/duplicate positions, no implicit states, charge units, failure and
  invalidation allocation, no Topology/repair, source immutability and H5MSM 0.5.
  This overlaps the broad regression; counts are not additive.
- Basic.set, ChemicalStates/native-query and all nineteen new adapter docstrings:
  **29 passed**, exit 0, **7.46 s**, with executable public-route examples.
- Original migration contract: **17 passed, 19 failed**, exit 1, **5.74 s**.
  Pure-Topology authority/copy, topology replacement, Builder associations,
  dictionary associations and the new functional namespace remain outstanding.
  No target is weakened, skipped or xfailed.

```bash
python -m pytest --receptor=llm -n 12 \
  tests/native/test_chemical_state_public_assignments.py \
  tests/native/test_chemical_state_assignments.py \
  tests/native/test_chemical_state_field_queries.py \
  tests/form/molsysmt_ChemicalStates
python -m pytest --receptor=llm -n 12 --doctest-modules \
  molsysmt/basic/set.py molsysmt/native/queries.py \
  molsysmt/native/chemical_states.py molsysmt/form/molsysmt_ChemicalStates/set.py
```

Foundations, native-editing/API notes, the Set tutorial, course Common Core 10
and the group-free Cookbook describe the same boundaries. Three notebooks execute
in 7.7 s, 9.8 s and 8.0 s, preserving all old executable cells and updated outputs/
fingerprints. The touched basic.set inventory entry now points to the actual
Common Core 10 path rather than its obsolete module name. Sphinx HTML succeeds
with the established diagnostic static-assets exclusion and two pre-existing
static README toctree warnings; changed sections/anchors/rendered nullable
examples are inspected. This is not deployed Viewer qualification.

All 97 adapter structural/delivery-ratchet checks, the maintained 156-module
course validator, Ruff/formatting, docstring fidelity, optional-import checks,
277-symbol registry and signature comparison against
`26efebbecc77a96c8020346a3f680c9c6081adca` pass. The Rust binary and four unrelated
RST edits are unchanged. Successful regression payloads are removed and compact
logs remain in ignored qualification cache. No main merge, tag or release.

**Next at that checkpoint:** standalone component membership/label assignment and declarations with
explicit inventory/graph consistency; then dictionary/predicate and mixed-domain
routing, MolSys/Builder authority, functional module and codec cutover. P3 and
#255 remain open. C6/C7 receiving and release qualification remain separate.

### P3 fourth slice: declared component membership and labels

Development commit
[`c70605834d143675f0a536ef1b879d8d3f9dd6a7`](https://github.com/uibcdf/molsysmt/commit/c70605834d143675f0a536ef1b879d8d3f9dd6a7)
adds seven decorated form setters: atom-to-component membership and component
ID/name/type labels from component rows or atom projections. `component_index`
now declares its atom assignment destination in the shared attribute catalogue.
Native chemical helpers own normalization and staged publication; digesters reuse
their value contract without reconstructing Topology. These are **Contract-tested**
and **Parity-tested** declarations, not new chemistry or graph-perception methods.

The bounded public contract is explicit:

- Component indices refer to existing state-local rows. Scalars/one-item vectors
  broadcast; other vectors follow ordered unique atom positions. None denotes
  unknown membership. Reject invalid/boolean/fractional/unit-bearing/out-of-range
  references without creating states, rows, bonds or stable molecule inventory.
  Row count remains fixed, including empty declared rows. Import declarations or
  explicit graph reconstruction can supply the inventory; no new component-row
  allocation/removal API is introduced in this slice.
- A changed membership declaration records partial completeness (unavailable if
  every membership is unknown) and user_defined evidence. It does not certify
  consistency with the bond graph or change connectivity completeness. Explicit
  rebuild_components retains its existing graph/participation criterion.
- Transfer metadata only when the new component's entire atom set equals an old
  full set. Labels follow sets across index permutations; changed/merged/split or
  ambiguous empty/unknown sets receive missing IDs/names/types. The shared exact
  matching primitive now handles unknown destination membership without negative
  indexing, retaining its full-source cardinality proof for extraction/rebuilds.
- Label setters accept None and string labels (integer IDs normalize to strings).
  Lexical IDs such as '001' and '1 nm' remain opaque labels, never quantities.
  Atom projections update whole component rows. Reject unknown membership and
  conflicting values for selected atoms of one component before publishing.
- Membership, metadata correspondence and owner invalidation are staged together.
  Failure preserves original field/table/analysis identities. Changed membership
  invalidates all named analyses, including evaluated-empty scope; labels preserve
  observations. Empty and identical membership edits are no-ops. Other states,
  reference, history, associations, atom properties, bonds and geometry stay intact.
  Multi-attribute calls remain separate per-attribute edits.

Private assembly's existing low-level _set_component_indices remains distinct:
its construction staging may precede row creation. The new public declaration
uses a checked existing-inventory path. Caller migration/removal remains C6 work;
these helpers do not promise complete pure-Topology/MolSys/Builder cutover.
Completeness/evidence fields remain readable declarations rather than unrestricted
public setters that could silently certify a complete graph.

Verification in the existing Linux/Python 3.14.7 environment:

- Extended migration regression, including shared matching, component helpers,
  conversions/extraction, affected setters/digesters and H5MSM: **5,142 passed**,
  exit 0, **102.42 s**, 776 warnings, Pytest Receptor with **12 workers**.
- Final focused component/state assignment, graph-edit, query and direct-form
  selection: **331 passed**, exit 0, **7.00 s**. This includes 57 new cases
  (52 native and five direct-form), with literal expected sets, labels, dtype/null
  shapes, bounds, failures and H5MSM 0.5 round trips. Counts overlap the regression.
- Assignment/native-query/ChemicalStates docstrings: **36 passed**, exit 0,
  **7.21 s**, including executable examples for all seven new setters.
- Original target contract remains **17 passed, 19 failed**, exit 1, **5.53 s**:
  pure Topology, MolSys replacement/Builder/dictionary association and functional
  namespace requirements remain unfinished. No target is skipped or weakened.

A one-million-atom typed declaration with one component is allocated before
tracing. After warm-up, an atom-projected single-label edit must remain below a
1 MB traced allocation allowance. A controlled negative implementation obtains
full membership before selecting the same atom: output remains correct but the
guard rejects **3,011,612 bytes** (expected pytest exit 1; driver exit 0). This is
an allocation regression guard, not RSS, timing qualification or a benchmark for
arbitrary component counts. Label projection reads only selected membership;
staging still scales with the component table being edited. No coordinates or
trajectory payloads are copied.

An initial final-check startup encountered the host's /tmp user quota: pytest
exited 3 before tests ran, and the sandbox launcher also reported quota failure.
Its log is retained separately. Moving only five task-owned scripts and using
repository-local TMPDIR/basetemp recovered the same selection without changing
expectations, timeouts or the environment. Other processes' temporaries were not
deleted. Successful task test payloads were removed; compact evidence is retained
in ignored qualification cache. The host's general /tmp quota is not claimed fixed.

```bash
mkdir -p .pytest_cache/chemical-domain-255-qualification/temporary
TMPDIR="$PWD/.pytest_cache/chemical-domain-255-qualification/temporary" \
  python -m pytest --receptor=llm -n 12 \
  tests/native/test_chemical_component_assignments.py \
  tests/native/test_chemical_state_assignments.py \
  tests/native/test_chemical_state_public_assignments.py \
  tests/native/test_chemical_state_field_queries.py \
  tests/native/test_chemical_state_edits.py tests/form/molsysmt_ChemicalStates
```

Foundations, Toolbox/API notes, the Set tutorial, Common Core 10 and the group-free
Cookbook now explain the same declaration/label boundary. Their three new
examples execute (23.0 s, 13.0 s and 8.2 s), preserving every previous code cell and
updated output/fingerprints. Sphinx HTML succeeds with the established diagnostic
static-assets exclusion and two pre-existing static README toctree warnings;
rendered component sections, lexical labels and partial examples are inspected.
All 97 adapter structural/delivery-ratchet checks, the maintained 156-module course
validator, Ruff/formatting, docstring fidelity, optional-import checks, 277-symbol
registry and signature comparison against
`fac01d2718b0a1048211bca08b9f1768aaf05cee` pass. The native binary, dependency floors
and four unrelated RST edits are unchanged; no installation, main merge or release.

**Next:** ChemicalStatesDict and predicate/catalogue delivery, then mixed-domain
MolSys/Builder routing and authority, pure Topology and functional/codec cutover.
The full P3 phase, #255, C6/C7 client receiving and release qualification remain open.

### P3 fifth slice: direct typed dictionary reads

Development commit
[`a74218508c318588417916dc8c2c8adc0610f143`](https://github.com/uibcdf/molsysmt/commit/a74218508c318588417916dc8c2c8adc0610f143)
extends ChemicalStatesDict with the shared native get/info experience and direct
form getters for stored chemical axes and nullable atom/bond/component fields.
The dictionary schema and public query signatures do not change. This slice is
**Contract-tested** and **Parity-tested**, not a new chemical-perception method.

Both `payload.get(...)` and `msm.get(payload, ...)` read typed values and null masks
directly. They do not decode a ChemicalStates collection, construct storage states
or Topology, infer missing chemistry, or visit unrelated states/preparation history.
Native and dictionary providers share state-index resolution, context-local scope,
incidence/membership projection and nullable field assembly. Each storage provider
owns reading and validating its own requested columns. No second graph algorithm
or hidden full-state cache is added.

The supported contract includes:

- Explicit/reference state selection, selected-state bounds and ordered/repeated
  atom, bond and component positions. Collection inventory remains collection-wide;
  masks retain basic.get's existing intersection semantics. Invalid/ambiguous state
  selection rejects without changing the reference or payload.
- None for an absent atom column, preserved nullable edge/stereo-reference shapes,
  unknown component membership, known zero/False values, string labels, and the
  distinction between zero states and a declared edge-free graph. Requested table
  lengths, value types, null masks and endpoint/membership references are checked.
- Native `.info()` reference-state summaries with existing signatures; no new info
  state selector. A successful query does not certify the entire payload, its
  unrelated records or its preparation history. Full conversion remains explicit.
- Small field selections slice values/masks before result assembly. Cardinality
  queries do not enumerate atom positions. Incidence queries still use the shared
  graph projections; no universal constant-time adjacency or performance claim.
- Raw `.data` edits remain outside controlled mutation. Dictionary setters and
  general predicate/catalogue delivery are pending. For edits, explicitly convert
  to ChemicalStates, apply supported native methods/setters and encode again.

#### Executed qualification — 2026-10-29

The shared Linux/Python 3.14.7 development environment is retained, with
`--receptor=llm -n 12` and task-owned repository-local TMPDIR/basetemp:

- New dictionary cases plus common native query tests: **151 passed**, exit 0,
  **6.65 s**. Literal expectations cover counts, selected incidence/membership,
  rich nullable properties, empty/ambiguous states, masks, independent scopes,
  errors and source/result ownership. Poisoned native constructors/conversion
  routes and inaccessible unrequested records guard the direct-read boundary.
- The broad native/basic-get/select/set/extract/remove, topology, H5MSM, component,
  ChemicalStates/Dict form, digest and chemical-template selection reports
  **5,246 passed**, exit 0, **109.23 s**, 777 warnings, no skips or xfails. This
  explicitly excludes the unfinished final-separation target module below.
- Allocation guards trace warmed reads on a preallocated million-atom payload:
  selecting two atom charges/component labels and querying zero-state atom
  cardinality each stay below 1 MB additional traced allocation. A deliberate
  negative control retains correct values but expands the entire column before
  slicing: the small-query guard fails at **17,010,616 bytes**, pytest exit 1.
  Its enclosing experiment verifies that expected rejection. These are bounded
  allocation guards, not a general RAM/disk benchmark or full-process RSS measure.
- Changed native query/ChemicalStates/Dict docstrings: **11 passed**, exit 0,
  **7.58 s**. Common Core 4, the Get tutorial and the group-free Cookbook execute
  cleanly (7.7 s, 15.4 s and 8.0 s), retaining every prior code cell/order and
  refreshed outputs/fingerprints. Foundations, Toolbox, API and course inventory
  describe the same direct-read/explicit-edit boundary.
- The original final-separation target remains **17 passed / 19 failed**, exit 1,
  **8.40 s**, without relaxed expectations or skip markers. Failures still require
  pure Topology, independent MolSys/Builder authority, the new functional module
  and dictionary domain composition; this slice does not claim those exits.

Reproduction of the new cases:

```bash
mkdir -p .pytest_cache/chemical-domain-255-qualification/temporary
TMPDIR="$PWD/.pytest_cache/chemical-domain-255-qualification/temporary" \
  python -m pytest --receptor=llm -n 12 \
  tests/form/molsysmt_ChemicalStatesDict/test_queries.py \
  tests/native/test_native_queries.py \
  --basetemp="$PWD/.pytest_cache/chemical-domain-255-qualification/dict-focus"
```

The broad selection additionally covers tests/native (excluding the target above),
tests/basic/get, tests/basic/select, tests/topology, tests/form/file_h5msm,
tests/form/molsysmt_Topology, tests/form/molsysmt_ChemicalStates, the complete Dict
form directory, tests/element/component, tests/_private/argdigest, all
`test_chemical_template*.py` in tests/physchem, all `test_set*.py` in tests/basic,
and the explicit extraction/removal/public-structure-boundary controls used in the
previous slice, including component hydrogen reinsertion.

Sphinx HTML succeeds with the established static-assets diagnostic override and
the two pre-existing static README toctree warnings. The new Foundation page,
course section and inherited method links are checked in the rendered output.
Ruff/changed-file formatting, optional-import validation, 97 adapter structural/
delivery checks, course structure, docstring fidelity, 277-symbol registry and
signature comparison against `430e5676caca78f7a77c99ed97b6cc1ff489198a` pass.
Dependency floors, the native binary and four unrelated RST edits are unchanged.
No dependency installation, main merge, tag, release or installed-candidate claim.
Successful task payloads/build outputs are removed after review; compact logs
remain in ignored qualification cache. The shared /tmp quota remains outside
this slice; other processes' temporary resources are preserved.

**Next:** complete dictionary/predicate capability dispatch, then mixed-domain
MolSys/Builder routing and authority, pure Topology, the functional module and
versioned codec cutover. P3, #255, C6/C7 receiving and release qualification remain
open; the declared final-separation failures are still work to do.

## Acceptance matrix

| Boundary | Required independent observation |
| --- | --- |
| Pure inventory | Bare/attached Topology cannot supply hidden bonds, states or components; stable groups/chains/IDs remain queryable and copyable. |
| Missing versus empty | Absent domain, zero states, unknown connectivity and complete edge-free graph remain distinguishable. |
| State selection | State-local indices/counts follow the requested state; invalid/ambiguous/mixed requests fail without reference mutation. |
| Stable hierarchy | Two states may have different components while topology molecules/chains stay fixed; no forced molecule/component equality. |
| Component evidence | Participation flags, incomplete knowledge and metadata-transfer rules survive rebuilds and bond edits. |
| Source axes | Extraction/permutation/growth maps atoms and every dependent domain coherently; IDs remain labels and strings. |
| Partial systems | State-only, structures-only, group-only, topology-only and supported composed inputs preserve absence and prerequisites. |
| #518 inventory | Empty/repeated FASTA occurrences, zero atoms, caps, alphabetical chain IDs and ordered/shared chain/group membership survive. |
| Mutations | Controlled edits update the intended state and preserve other states; failed edits are not partially published. |
| Interactions | Sparse relations, occurrence indices, evaluated-empty coverage, producer history and established invalidation stay correct. |
| Copies | Source/clone ownership and aliases are correct; pure Topology copying does not traverse chemistry, MolSys retains one chemical authority. |
| Chemistry/geometry | Original independent scientific controls, coordinates and active PyUnitWizard policies retain their meaning. |
| I/O | New dictionaries are versioned; legacy inputs migrate faithfully; H5MSM 0.5 layers/maps remain valid and projected reads stay bounded. |
| Clients | Real receiving calls run against identified compatible sources; unavailable public packages are not advertised as delivered. |

Use tests mirrored under `tests/native`, `tests/basic`, `tests/form` and the new
`tests/chemical_states` area as appropriate. Existing scientific controls are to
be ported, not replaced by self-consistency-only or weakened assertions. Select
the final guard from an existing executable test node at actual closeout; none
is claimed today.

## What is inspected, executed and still assumed

Inspected source: `71fbe4f46d3c70e4e973c8025f01752a8c9b1084`, including native
Topology/ChemicalStates/MolSys/Builder, query resolution/providers, dictionaries,
H5MSM layers, component inference and current topology exports.

Read-only Python probes in the development environment establish the current
coupling, not the proposed behavior. They were run on 2026-10-28 with
Linux/Python 3.14.7; these probes do not invoke an optional chemistry engine:

```bash
python - <<'PY'
import molsysmt as msm
from molsysmt.native import Topology
from molsysmt._private.smonitor import ArgumentError
states = msm.ChemicalStates(n_atoms=2)
states.append_state()
print(states.get(n_atoms=True), len(states.get_bonds()))
print(msm.has_attribute(states, 'n_bonds', include_none=True))
print(msm.has_attribute(states, 'component_index', include_none=True))
try:
    states.get(n_atoms=True, chemical_state=0)
except ArgumentError:
    print('explicit-state native query rejected')
topology = Topology(n_atoms=2)
print(topology._chemical_states_domain.n_chemical_states)
print(type(topology._chemical_states_domain._states[0]).__module__)
print(topology.copy()._chemical_states_domain is not topology._chemical_states_domain)
PY
```

Observed at the inspected source: `2 0`; both advertised attribute checks are
False; the explicit-state query raises ArgumentError; bare Topology creates one
state whose storage class is defined in `molsysmt.native.topology`; copying clones
the collection. Private access above is a diagnostic reproduction, not proposed
public usage. No new tests or refactoring had been executed at that original
planning checkpoint; the dated execution receipt records subsequent work.

Bounded Python searches of fetched `origin/main` identify concrete consumer
callers, not a complete compatibility audit:

| Repository/source inspected | Relevant observation |
| --- | --- |
| `uibcdf/molsysviewer` at `8903f0659f2833cc979e4072cf60d17e8bcc6ef9` | Native-array loader reads `molsys.topology.bonds`; caller validation inventories retain moved paths. |
| `uibcdf/dockingmt` at `aa2f317c132e255470b0512649c3691c56364ed9` | Symmetry, torsion classification, covalent blocks and rigid-fragment callers. |
| `uibcdf/pharmacophoremt` at `87de52f1a13913ed1d941c3a0a6425a979a64b1f` | Maintained diagnostic support calls topology SMARTS. |
| `uibcdf/topomt` at `6e88237e7e71dcf569613a4a860eaa1d12bcb79d` | No match in this bounded search; this does not certify absence of indirect dependencies. |

Sibling status was refreshed using the suite status tool. Several local clients
are behind/divergent and Viewer has unrelated edits; these were preserved.
Implementation must refresh this receipt before coordinated changes. Expected
clarity and workload benefits remain hypotheses until measured; this is neither
an installed-candidate nor a new platform qualification.

## Alternatives rejected and risks to keep visible

- Removing only public properties leaves chemical implementation, private
  ownership and query dependencies in Topology; that is not the accepted target.
- Moving files without state-aware paths/quartets leaves implicit-reference
  behavior. Changing scientific rules during the move obscures regressions.
- Duplicating component membership in groups/topology creates competing state
  authorities. Rebuilding molecules on every state edit changes stable identity.
- Wrapping every operation in a full MolSys conversion/copy defeats native and
  projected-reader contracts. New compiled kernels are not a prerequisite.
- Reusing old JSON schema versions for new layouts, or silently dropping legacy
  chemistry, makes conversion unreviewable. Historical producer records cannot
  be rewritten to current reader versions.
- Closing #255 only after #254's final 1.0 recertification would create a scheduling
  cycle. Its implemented independent-domain foundation is available; #255 source
  closeout precedes the new #254/#334 final-candidate qualification.

The remaining engineering uncertainties are the exact constructor/cutover and
wire-format details in P0/P6 and executed client compatibility. Resolve these in
their phase receipts rather than expanding the scientific scope or inventing
completion claims. No deadlines or performance ratios have been measured.

## Related decisions and final release boundary

[Independent-domain record](promote_chemical_states_to_a_native_molsys_domain.md)
(#254) supplies the implemented foundation. Its final-candidate obligations
remain open. [Identity/scaffold proposal](molecular_identity_and_scaffold_overlap_annotations.md)
(#447) uses the new namespace after this migration; it is not implemented here.
The [scope decision](../release_1_0_scope.md),
[roadmap](../roadmap.md) and [release ledger](../release_1_0_status.md) point here
for the work breakdown, rather than keeping separate detailed task lists.

At closeout, report changed user contracts, actual guards and consumer evidence.
Do not close #254/#334 merely because the namespace moved. Preserve original
published/staging files, tags, commits, hashes and old receipts; qualify a new
candidate after the final source changes and communicate actual compatible
package availability through the owning release/consumer issues.
