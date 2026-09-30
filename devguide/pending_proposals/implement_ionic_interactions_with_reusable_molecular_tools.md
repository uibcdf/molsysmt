---
summary: Implement ionic interactions with reusable molecular tools
issue: uibcdf/molsysmt#261
status: active
opened: 2026-09-30
closed:
verification: inspected
area: [api, attribute, structure, pbc, performance, docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# Implement ionic interactions with reusable molecular tools

**Reported:** 2026-09-30, following the maintainer's review of additional
interaction families and source inspection of molecular analysis libraries.
**Status:** Active implementation. The maintainer accepts ionic, pi-pi,
and cation-pi as the next sequence and requires reusable domain tools and
allows additional Rust routines for heavy computation. The first general
charge-center tool is implemented experimentally; the ionic detector remains
pending.

## What

Implement an experimental ionic interaction detector using general chemical,
geometric, and periodic-boundary tools. Separate charge acquisition, chemical
participant recognition, and the interaction criterion. The proposed first
delivery uses formal-charge participants from one selected chemical state
and an explicit minimum-distance method; this is a bounded implementation
sequence, not a restriction of the architecture to formal charges. Preserve
the existing sparse Interactions contract and scientific provenance. This
first delivery is independently closable; pi-pi and cation-pi follow in
separately scoped implementation issues.

## How

### Maintainer decision: general tools belong to their domains

The local root AGENTS.md now carries this maintainer instruction. Its
suite-wide policy and adoption in other components are tracked by
`uibcdf/molsyssuite#61`; preparing that central proposal does not establish
adoption in every member.

The detector orchestrates chemical eligibility, candidate generation, and
its named scientific criterion. Reusable capabilities belong in the existing
domain modules. Promote an internal helper to a general public tool when a
concrete second use or a meaningful standalone operation establishes its
contract; provide real implementation, docs, and tests with that promotion.
Do not create placeholder exports.

| Capability | Owner and intended route | Current evidence |
| --- | --- | --- |
| Stored formal charges, aromatic flags, and covalent bond assignments | ChemicalStates, delivered through `basic.get(..., chemical_state=...)` | Implemented; the native MolSys domain owns the state collection. |
| Stored partial charges | MolecularMechanics, delivered through `basic.get(..., partial_charge=True)` | Implemented query/storage route. State association, source provenance, and missing-value behavior need review before use by a detector. |
| Charge-center identification and charge interpretation | `physchem.get_charge_centers` | Implemented experimentally for selected-state formal charges with bounded motif rules. `physchem.get_charge` remains the residue-scale/OpenMM partial-charge route. |
| Explicit force-field parameterization and charge assignment | Existing conversions and `molecular_mechanics` for force-field work; extend the owning general tool rather than parameterizing inside a detector | OpenMM System conversion exists. General named charge assignment is separately tracked by `uibcdf/molsysmt#221`; Gasteiger assignment is not force-field parameterization. |
| Element-specific queries and interpretation | `element.atom`, `element.molecule`, and the relevant subtype namespace, including `element.molecule.small_molecule` | The namespaces exist. The molecule-level small-molecule package currently has no exported helpers; group-level small-molecule name/database/bond helpers already exist. |
| Connectivity traversal, cycles, and reusable functional-group recognition | `topology`, reading the selected chemical state rather than creating another chemical store | Bond graphs and covalent paths exist. Private CSR traversal and bounded carboxyl/guanidine candidate recognition now serve the charge-center tool; a public general ring/functional-group contract remains future work. |
| Aromatic eligibility from stored or explicitly inferred chemistry | General chemistry interpretation in `physchem`, using connectivity tools | Stored attributes and RDKit conversion exist; a common aromatic participant provider is new work. |
| Hydrophobicity scales and atom hydrophobic typing | `physchem`, with a named definition and evidence | Residue hydrophobicity scales exist. They do not assign atom-level hydrophobicity. Atom typing would be separate work when a detector needs it. |
| Centers, best-fit planes, planarity, distances, and angular geometry | `structure`, using existing centers and geometric principal axes where appropriate | Centers and geometric principal axes exist, including Rust kernels. A reusable plane result with degeneracy checks and explicit units may need an additional boundary. |
| Covalent reconstruction, MIC conventions, and lattice shifts | `pbc` | `wrap_to_mic` and `wrap_to_pbc` reconstruct covalent blocks with `compact='component'`. Returning per-atom reconstruction shifts and a compactness check would require an explicit additional contract. |
| Spatial candidate search | `structure.get_neighbors` and private shared numerical kernels | Threshold CSR search already uses the bundled Rust cell-list kernel. |
| Sparse analysis, query, attachment, and persistence | Interactions, MolSys.interactions, InteractionsDict, and H5MSM | Existing experimental contract; see the [interaction API](../interactions_api.md). |

Participant atom sets are chemical motifs, not additional native residue
groups. Their local row indices must not be presented as `group_index`, and
all member values are atom indices rather than element IDs. Preserve maps
when a provider extracts or reorders atoms.

### Charge acquisition, participant definition, and detection are separate

**Design clarification — 2026-09-30:** The maintainer identifies physicochemical
definitions, stored MolSys charges, and force-field parameterization as useful
routes. Keep all of them in the design. `physchem` is a property interpretation
boundary, ChemicalStates and MolecularMechanics are data domains, and
parameterization produces data. These are not interchangeable detector methods.

Each calculation must distinguish:

1. **Charge source:** a named physicochemical definition, selected-state formal
   charges, stored partial charges, or an explicitly requested parameterization.
2. **Participant definition:** atom typing, connected chemical motifs, or
   explicitly inferred residue templates, with rules for delocalization,
   protonation, and the atoms used for geometric measurements.
3. **Detection method:** minimum distance, another named geometric definition,
   or an independently specified electrostatic energy model.

Argument names such as `charge_source`, `participant_definition`, and `method`
are proposed concepts, not exported API. Prefer extending an existing general
API when its semantics fit; do not introduce a second generic charge getter
merely to serve the detector.

| Route | Existing foundation | Additional detector requirements |
| --- | --- | --- |
| Named physicochemical definition | `physchem.get_charge` provides residue tables | A supported definition must identify center atoms and state its chemical assumptions. A residue-level scalar alone is insufficient. |
| Selected-state formal charge | `basic.get` exposes formal charges from the selected chemical state | A general center recognizer must group delocalized motifs and distinguish ionic centers from neutral charge-separated motifs. |
| Stored partial charge | MolSys mechanical queries delegate partial-charge access to MolecularMechanics | Require complete finite values, units, axis alignment, and a declared association with the state being analyzed. Apply an explicit participant definition rather than classifying every opposite-sign atom pair as ionic. |
| Explicit force-field parameterization | MolSys-to-OpenMM-System conversion and the OpenMM route of `physchem.get_charge` | Reuse general preparation/conversion tools, record the actual parameterization, and verify atom-to-particle correspondence before deriving atom-aligned charges. |

Source inspection of `physchem/groups/charge.py` shows that `physical_pH7`
contains fractional values, including 0.1 for HIS, and that `collantes` is
documented as an electronic charge index. Neither table is proof of atom-level
formal charge or ionic-center membership. In particular, the Collantes index
must not be consumed as a signed net ionic charge merely because the existing
getter returns it through a charge-shaped interface. The detector needs a
definition whose meaning is suitable for its claimed interaction type.

Formal-charge semantics belong to ChemicalStates and partial-charge parameters
to MolecularMechanics. Historical formal-charge fields still exist in
MolecularMechanics; their presence does not authorize a competing chemical
state or silently override selected-state charges.

For the proposed fixed-charge route, parameterization is explicit and occurs
once per unchanged chemical state and parameter set, not once per structure.
Geometry-dependent or polarizable charge models need a separate contract;
they must not inherit this caching assumption. Reuse stored charges when
that source is requested. Do not parameterize automatically when a stored-source query
fails, substitute partial for formal charges, or substitute a residue table
for either. Such substitutions change the scientific definition.

Charge acquisition validates the required chemistry, missing/nonfinite values,
units, atom order, and available provenance. Atom counts alone do not establish
alignment. Added hydrogens or virtual sites need explicit correspondence;
unsupported particle mappings fail clearly. Stored charges whose producing
method or version is absent remain of unknown origin; the current calculation
must not fabricate that history. Require an explicit declaration where the
requested method needs information that the stored domain does not supply.

Opposite-sign partial charges can occur within neutral molecules. A detector
using them must distinguish a named polar-contact definition from a method
that establishes ionic centers. Likewise, an electrostatic energy method must
specify dielectric assumptions, exclusions/scaling, units, and periodic
treatment. A geometric cutoff is not an energy calculation, and a bare
charge-product-over-distance expression is not automatically the force-field
electrostatic energy. Existing nonbonded-energy tools are candidates for reuse
after a separate contract review; their existence does not establish the
needed ionic energy semantics or trajectory-scale performance.

### Proposed delivery sequence

1. Specify and implement the general `physchem` charge-center operation for
   selected-state formal charges, with its own chemistry fixtures and typed
   output. This route avoids an obligatory force-field backend and gives
   explicit control of the analyzed protonation state.
2. Implement minimum-distance ionic detection over those centers, using shared
   neighbor/PBC kernels and the existing Interactions output. The first route
   must not claim support for every charge source in the preceding table.
3. Add named inferred physicochemical definitions and stored-partial-charge
   interpretations as separately tested routes. Reuse center geometry, scope,
   queries, and persistence while retaining each method's distinct evidence.
4. Connect explicit parameterization through general tools when its mapping
   and provenance contracts are ready. Coordinate generic charge assignment
   with `uibcdf/molsysmt#221`; its current post-1.0 schedule is not silently
   changed by this proposal. Energy-based methods need their own scoped work.

Steps 1 and 2 define the proposed first implementation under this issue.
The other sources remain valid planned routes, rather than rejected
alternatives or closure requirements for this first method. The cutoff and
recognition-rule coverage of the detector still need explicit scientific decisions
before its public export; no universal threshold is settled here. The proposed first
method requires an explicit distance threshold with units rather than choosing
an unvalidated universal default.

The general center result should use typed arrays and offsets for atom
membership, plus charges with explicit units, definition/evidence, source
axis maps, state association, and classification coverage. Separate the atoms
used to recognize a motif or account for its charge from the atoms used for
the named distance criterion when these sets differ. The detector translates
the documented participant set into Interactions and preserves query semantics.
Center row indices are local indices, never native molecular `group_index`.
This result layout is now an experimental standalone dictionary contract,
not a new native domain or a new class.

### Implementation checkpoint — 2026-09-30

The first delivery step is implemented as
`physchem.get_charge_centers(..., definition='formal_charge')`. It reads the
selected chemical state, recognizes bounded carboxyl/guanidine motifs, combines
directly covalently connected charged atoms, and omits neutral groups. It does
not change source chemistry, parameterize, or substitute a residue definition.
Atomic and generic cluster labels report formal-charge evidence; they are not
a universal ionic classification. Phosphate, sulfate, aromatic delocalization,
and alternative resonance representations outside the documented rules are
not grouped by this version.
Expansion and scientific validation of these rules are tracked separately in
`uibcdf/molsysmt#262`; see the
[charge-center coverage proposal](expand_and_validate_formal_charge_center_recognition.md).
That expansion is not a closure requirement for this first bounded ionic method.

The result packs whole-center membership and separate distance-reference
membership into int64 arrays and offsets. It records elementary-charge units,
selected and examined atom indices, the current source axis, state index,
recognition-rule version, completeness evidence, and the recognition software
version. A stored chemical-state provenance index remains a reference to that
source; absent historical charge-preparation provenance is not invented.
This chemical-feature dictionary is not an InteractionsDict or an occurrence
analysis and is not automatically attached to MolSys.

Recognition requires explicit elements, formal charges, covalent/dative bond
relationships, and supported covalent bond orders. Incomplete or unknown
connectivity fails by default. The caller can explicitly declare complete
connectivity with `assume_complete_connectivity=True`; the result records that
assumption without altering source metadata or filling bonds. Recognition
examines the full state before filtering centers. A selection cutting a
nonzero compound center fails, and source atom indices are never renumbered
or confused with IDs. Structure-assigned states currently require the
requested structures to share one state.

Evidence for this checkpoint:

- `tests/physchem/test_get_charge_centers.py`: 32 deterministic cases covering
  charge-localization variants, neutral nitro/N-oxide controls, zwitterions,
  state changes, compound selections, dative bonds, missing prerequisites,
  explicit completeness assumptions, optional RDKit source chemistry, and
  a public H5MSM 0.5 source round trip. This is bounded contract and analytical
  evidence, not validation of all chemical groups.
- The focused run including existing `tests/physchem/get_charge` passes:
  **36 passed**. The new public docstring doctest passes: **1 passed**.
- The new User Guide tutorial and Cookbook recipe were executed successfully.
  All four Module 39 course paths received conceptual guidance and links;
  their existing network-dependent code cells were preserved, not re-executed.
- The API is registered as experimental. Documentation, digestion, Ruff,
  dependency, API-stability, and devguide checks accompany the delivery.

The minimum-distance detector, occurrence scope, PBC image evidence, chunked
trajectory execution, Interactions persistence tests, and performance
measurements remain pending. No detector throughput, memory bound, or
scientific stabilization is claimed by this first tool.

### Element-specific tools

**Maintainer clarification — 2026-09-30:** Consider the existing `element`
hierarchy when placing reusable tools. A capability whose contract is specific
to atoms belongs in `element.atom`; one specific to small molecules may belong
in `element.molecule.small_molecule`. For example, a query assessing the
chemical prerequisites of a selected small molecule can be a meaningful
subtype-specific tool when needed by both preparation and interaction workflows.
This is an ownership option, not a new export or an additional required feature.

Keep the native hierarchy explicit: `element.group.small_molecule` operates
at the group/residue level, whereas `element.molecule.small_molecule` is the
molecule-level namespace. The inspected group helpers recognize known names
and consult local group databases; they do not establish complete chemistry
or recognition coverage for arbitrary ligands.

General charge interpretation remains in `physchem`, connectivity operations
in `topology`, and geometry/PBC operations in their existing domains. An
element-specific convenience query delegates to those tools when appropriate;
it does not duplicate them. Follow `molsysmt/element/AGENTS.md`: public element
queries can support multiple forms, while native rebuild/inference paths use
internal native-data helpers rather than calling the public query layer.

### Ionic scientific contract

- Resolve an explicit state, or the existing unambiguous reference-state
  policy. Record the source chemical-state index and the recognition rules.
  `chemical_state='structure'` initially requires all requested structures
  to resolve to one state, matching current basic-query behavior. Multiple
  states need separate analyses until their scope and provenance are designed.
- Identify actual positive and negative charge centers. Delocalized centers
  may contain several atoms, such as carboxylate oxygens or guanidinium
  nitrogens. Specify atom membership and relevant charge evidence per rule.
- Start with minimum distance between the defined interaction-center atoms
  of two opposite-charge participants. A cutoff observation is geometric
  evidence; it does not report an interaction energy or an authoritative bond.
- A simple, explicit charged atom is a supported special case. Distinguish
  a charge-separated functional group from a net ionic center; do not treat
  every positive/negative formal-charge SMARTS match as an independent ion.
- Keep formal charge, partial charge, residue-scale charge, and ionizability
  distinct. Residue templates, if offered, are named inferred definitions;
  missing source chemistry does not silently select a template or assume pH.
  Histidine protonation must not be inferred solely from the name `HIS`.
- Define self, overlapping-participant, directly bonded, and intramolecular
  policies. A same-residue or same-component exclusion is not automatically
  inherited from a visualization implementation.
- Select and document default thresholds using analytical controls and real
  examples. The previously discussed 0.4 nm example and Mol*'s 0.5 nm default
  are reference choices, not agreed defaults or independent scientific truth.

### Proposed public surface

The first family route is
`interactions.ionic.get_ionic_interactions`. Common arguments include
`molecular_system`, `selection`, `selection_2`, `structure_indices`,
`chemical_state`, `method`, `pbc`, `syntax`, and `output_type`. The proposed
initial output is `molsysmt.Interactions`, with existing conversion to
`molsysmt.InteractionsDict`. Precise names and defaults require docstring and
digestion review before export. Current detector defaults remain as documented.

Define calculation scopes for internal, incident, and between searches rather
than conflating a calculation selection with filtering an existing result.
Between sets are initially disjoint. A selection cutting a compound
participant initially raises a clear error; it neither truncates that group
nor silently expands the evaluated atom universe. Querying a full result by
one member atom continues to use the existing incident/internal/cross semantics.

Each result retains full system axes and source maps, evaluated structures
including zero-occurrence frames, the actual eligible atom universe,
positive/negative participant roles, nm distances, and periodic images where
applicable. Record charge source, participant definition, method, thresholds
with units, recognition-rule version, chemical-state choice, exclusions,
parameterization details when used, and calculation-time software versions.
Distinguish the software performing detection from any known software that
previously produced stored charges; do not overwrite historical provenance
with the version installed at detection or load time.
If RDKit supplies chemistry, retain its version as well as MolSysMT's.
An analysis is attached by the caller under an explicit name.

Persist the resulting observations and their provenance in Interactions/H5MSM
0.5. This does not promise persistence of the full MolecularMechanics domain
or source force-field parameter arrays: that domain remains experimental and
its H5MSM incorporation remains deferred to 0.6.

Required missing or ambiguous chemistry fails visibly before claiming
complete coverage. A verified empty eligible universe can return evaluated
empty frames. Never use an empty result to hide failed classification.

### Periodic geometry and reconstruction

Reuse the existing PBC reconstruction tools. `pbc.unwrap` restores temporal
continuity per atom; it is not the single-frame covalent reconstruction
operation needed here. A general compactness assessment must state whether
it checks bondwise MIC consistency, a connected participant, or another
geometric property; these are not interchangeable for large molecules.

Reconstructing a compound participant can shift its individual atoms by
different lattice vectors. The present Interactions image field applies one
shift to every atom in a participant. Therefore reconstruction alone does
not make an occurrence reproducible on the original coordinates. Before
supporting split participants, either agree and test an additive, versioned
per-atom image representation under #251/#252, or restrict delivery to whole
participants and reject unsupported observations explicitly. Detection,
query, and display must use the same observed geometry. Do not silently modify
the source coordinates to make the encoding fit.

### Computation and Rust

Reuse compiled neighbors, MIC observations, and geometric kernels before
introducing another numerical implementation. Further Rust kernels are
allowed for expensive graph traversal, reconstruction, grouped geometry,
candidate acceptance, or typed result packing when profiling identifies
them as useful. Python owns public validation, units, method parameters,
dependency checks, and orchestration. Kernel boundaries use typed arrays
and offsets and avoid a Python call or dictionary per observation in the
trajectory-scale path. Compile the reusable primitive, not a duplicated
private copy inside each detector.

Recognition may be reused across structures within an unchanged state.
Caches must be scoped to a controlled calculation or explicitly invalidated
after chemistry edits; the current mutable domains are not automatically
revision-tracked. Rebuild spatial candidates for each structure or use a
proven conservative update policy. A first-structure neighbor filter does
not establish complete trajectory coverage.

Use ChunkedExecutor for large trajectories, with a sparse reducer and typed
accumulator. Plan for candidate and output memory as well as coordinates.
Processing coordinate blocks bounds working memory, not total result memory:
the current Interactions load is eager and it has no public incremental
writer. Delivery beyond RAM needs the separately tracked serialization work
under #252 and a measured budget policy. Do not advertise an out-of-core
detector merely because its input can be iterated.

Follow the [Rust optimization guide](../rust_kernel_optimization_guide.md)
and [heavy-trajectory contract](../SCALABILITY.md), preserving deterministic
MIC ties, frame provenance, and fail-fast execution.

## Why

Ionic, pi-pi, and cation-pi share chemistry and geometry with other molecular
workflows. General tools let the library serve those workflows and let
detectors remain small enough to review scientifically. Existing Rust,
chemical-state, PBC, and result infrastructure already provides much of the
foundation. This is an architectural judgment supported by source inspection,
not a measured claim that a particular new kernel is faster.

## What is measured and what is assumed

**Inspected:** MolSysMT at `f9f4c1a5f`; basic chemical-state resolution,
physchem charge/hydrophobicity functions, topology connectivity, geometric
principal axes, PBC reconstruction, Rust adapters, ChunkedExecutor/Reducer,
and the Interactions constructor and codec. No new detector was executed.

**Inspected for the charge-source clarification:** MolSysMT at `490b29eee`;
`physchem/get_charge.py`, `physchem/groups/charge.py`, the MolSys formal/partial
charge getters, `native/molecular_mechanics.py`, MolSys-to-OpenMM-System
conversion, and the existing nonbonded-energy function. The existing charge
test module was read, not executed during this documentation update. These
inspections establish existing routes, not parity between their scientific
definitions or validation of a new detector.

**Inspected external references:** Mol* `480717958`, MDTraj `80f7cf2d`,
MDAnalysis `9531c6e15`, and RDKit `a24ed4f06`, from the local source checkouts
on 2026-09-30. Relevant upstream files are
[Mol* charged features](https://github.com/molstar/molstar/blob/480717958/src/mol-model-props/computed/interactions/charged.ts),
[MDTraj pi stacking](https://github.com/mdtraj/mdtraj/blob/80f7cf2d/mdtraj/geometry/pi_stacking.py),
[MDAnalysis hydrogen bonds](https://github.com/MDAnalysis/mdanalysis/blob/9531c6e15/package/MDAnalysis/analysis/hydrogenbonds/hbond_analysis.py),
and [RDKit base features](https://github.com/rdkit/rdkit/blob/a24ed4f06/Data/BaseFeatures.fdef).
These implementations have different chemical and geometric definitions;
agreement is meaningful only after aligning a chosen method.

**Assumed:** Shared tools will reduce duplicated work and benefit subsequent
families. Performance and recognition coverage need benchmarks and fixtures.
No detector latency, speedup, peak RAM, or new serialization measurement is
claimed in this design record.

## What was refuted

The following are rejected design shortcuts, not eliminated benchmark
candidates:

- Embedding reusable hydrophobic typing, reconstruction, or plane geometry
  inside an interaction family obscures ownership and duplicates contracts.
- Residue hydrophobicity scales do not directly type individual atoms.
- RDKit ionizable features do not prove the selected state has that charge.
- Opposite signs of atom partial charges do not establish ionic participants;
  neutral polar motifs are required negative controls for that interpretation.
- A force-field route is not a fourth independent detection criterion: it
  produces parameters consumed by an explicitly named participant/method pair.
- Missing charges do not justify silent reparameterization or a switch to a
  different charge definition.
- Successful RDKit sanitization does not prove the source state was explicit
  and chemically sufficient; see the [readiness proposal](diagnose_ligand_chemical_readiness_for_a_selected_molecular_state.md).
- Mol* and its NGL antecedents do not form two independent scientific oracles.
- Compacting coordinates does not preserve internal images in today's result
  encoding automatically.
- Rust or coordinate chunking alone does not prove end-to-end speed or bounded
  output memory.

## Scope and exclusions

This issue delivers the first ionic method and the reusable tools concretely
required by it. Ring, plane, and hydrophobic tools listed above are ownership
decisions for later needs, not an obligation to implement every one here.
All charge-source routes are retained in the design; only the selected-state
formal-charge/minimum-distance route is required for this issue's first
delivery. Inferred definitions, partial-charge methods, generic charge
assignment, and electrostatic energy calculations are independently scoped.
Pi-pi and cation-pi are the next separately scoped families. Halogen, metal,
hydrophobic, and water-mediated analyses require their own method decisions.

Release timing is separately scheduled. This work does not add closure gates
to #250 or to MolSysViewer's initial hbonds/disulfide integration. Existing
Interactions/H5MSM acceptance remains tracked under #251/#252. New family
implementation does not claim that the result contract is already stable.

## Acceptance criteria

1. General charge-center tools have a standalone documented API, typed atom
   membership, explicit state/definition/evidence, and tests independent of
   ionic detection. Newly required topology/PBC primitives have their own
   domain tests and lifecycle documentation.
2. Analytical ionic fixtures cover atomic and delocalized centers, neutral
   and charge-separated groups, protonation differences, missing chemistry,
   and cutoff boundaries. Include a neutral polar motif and a zwitterionic
   example with local ionic centers despite a zero total molecular charge.
   Missing source data must not trigger a different definition or a backend
   parameterization. Scientific evidence labels distinguish analytical
   correctness from comparison with another implementation.
3. One/many/nonconsecutive/repeated structure indices, empty and variable
   occurrence counts, selection scopes, compound membership, and deterministic
   order are tested. Queries by atoms and structures retain original indices.
4. Supported PBC geometry and images reconstruct the reported distance in
   diagonal, rotated orthogonal, and triclinic boxes. Unsupported split
   participants fail explicitly until their serialization contract exists.
5. InteractionsDict and public H5MSM round trips preserve measures, units,
   occurrence indices, scope, charge-source/participant/method provenance,
   producer versions, and source maps. The calculation does not attach or
   replace analyses automatically.
6. Eager/chunked parity is tested where supported. Reproducible measurements
   separate recognition, candidates, acceptance, result packing, queries, and
   serialization; include total peak RAM and output density. Use real systems
   plus scale controls, and state support limits instead of extrapolating.
7. Public exports/digestion/stability registry, docstrings/doctests, User Guide,
   Cookbook, and affected Four Paths modules reflect delivered behavior.
   Ruff, dependency, governance, and applicable scientific gates pass.
8. Closure identifies executable scientific/contract guards and moves the
   durable domain contracts into maintained documentation before archiving.

## Dependencies and risks

Related work: `uibcdf/molsysmt#250`, `uibcdf/molsysmt#251`,
`uibcdf/molsysmt#252`, and `uibcdf/molsysmt#217`. Partial chemistry and compound
periodic images are substantive limits, not reasons to fabricate defaults.
General charge assignment is tracked by `uibcdf/molsysmt#221`; it is related
future work and not a dependency of the first formal-charge method. A later
force-field route must establish state/atom/particle correspondence and avoid
claiming full parameter persistence in H5MSM 0.5.
RDKit stays optional and lazily loaded. Existing general APIs are extended
only with documented, compatible semantics.

The result is consumable by MolSysViewer under `uibcdf/molsysviewer#114`.
Its initial integration remains independent. Any extension to the shared
image/result contract requires a separate provider/client agreement and
suite coordination when it changes cross-component obligations.
