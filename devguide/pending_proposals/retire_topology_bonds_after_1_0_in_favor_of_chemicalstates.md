---
summary: Complete ChemicalStates separation from Topology before 1.0.
issue: uibcdf/molsysmt#255
status: open
opened: 2026-09-29
closed:
verification: inspected
area: [native, api, form, topology, chemical-states, docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# Complete ChemicalStates separation from Topology before 1.0

**Role:** accepted migration plan and execution tracker.
**Maintainer decision:** 2026-10-28.
**Implementation status:** Not started. This delivery records the plan only;
no runtime refactoring, public API removal or schema migration has been executed.

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
| P0: contract and baseline | Maintainer decision | Plan recorded; implementation preflight remains | Accepted contracts, frozen source/worktree and impact inventory |
| P1: target/characterization guards | P0 | Not started | Independent expected behavior and baseline evidence |
| P2: native authority | P1 | Not started | Standalone state operations; pure Topology; no hidden recovery |
| P3: query/form dispatch | P2 | Not started | Basic/native/form parity and truthful capabilities |
| P4: builder and lifecycle | P2, P3 | Not started | Coordinated edits/remaps/copies and invalidation |
| P5: functional module | P3; P4 for integration | Not started | Nine moved APIs, state selection and unchanged scientific controls |
| P6: conversions/persistence | P3, P4 | Not started | Versioned payloads, legacy readers, partial and full round trips |
| P7: docs and consumer receiving | P5, P6 | Not started | Lifecycle docs and immutable consumer receipts |
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

### P0: contract and implementation preflight

- [x] P0.1 Record the maintainer-approved ownership, chain boundary and nine-function map.
- [x] P0.2 Record source observations, probe limitations, phase dependencies and acceptance matrix.
- [x] P0.3 Reconcile current roadmap/scope/status references and #447's proposed namespace, without changing runtime contracts.
- [ ] P0.4 Freeze implementation source/worktree, import/native-extension origins and existing changes; create an isolated development branch/worktree as appropriate. Never reset/stash unrelated work.
- [ ] P0.5 Finalize constructor signatures, missing-state behavior, the editing API map, stable group-free molecule membership, remap/state-alignment policy, coherent cutover and wire schemas; resolve the design-review findings above and select baseline workloads before changing them.
- [ ] P0.6 Select/open the owning suite impact and client-receiving issues before rollout. Record actual pins/versions; do not invent a published minimum version.

Exit: reviewable contract and baseline, including any deliberate exception. Routine
engineering decisions within this plan do not create a new permission round;
changes to scientific scope or compatibility promises need an explicit decision.

### P1: meaningful guards before refactoring

- [ ] P1.1 Characterize existing scientific outputs and supported completeness/participation policies with independent expectations; retain original controls.
- [ ] P1.2 Add target guards for pure Topology, absent/zero/unknown/complete chemistry and standalone state-only operations. Tests must detect hidden chemistry even if private attributes are renamed.
- [ ] P1.3 Add two-state controls with different bond/component counts, ambiguous reference, structure associations, nonconsecutive indices and failed resolution without source mutation.
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
public usage. No new tests or refactoring have been executed for this plan.

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
