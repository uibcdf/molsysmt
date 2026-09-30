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
**Status:** Active design preparation. The maintainer accepts ionic, pi-pi,
and cation-pi as the next sequence and requires reusable domain tools and
allows additional Rust routines for heavy computation. No new detector or
public primitive is implemented by this record.

## What

Implement an experimental ionic interaction detector using general chemical,
geometric, and periodic-boundary tools. Start with charged participants from
one selected chemical state and an explicit minimum-distance method. Preserve
the existing sparse Interactions contract and scientific provenance. This
first delivery is independently closable; pi-pi and cation-pi follow in
separately scoped implementation issues.

## How

### Maintainer decision: general tools belong to their domains

The detector orchestrates chemical eligibility, candidate generation, and
its named scientific criterion. Reusable capabilities belong in the existing
domain modules. Promote an internal helper to a general public tool when a
concrete second use or a meaningful standalone operation establishes its
contract; provide real implementation, docs, and tests with that promotion.
Do not create placeholder exports.

| Capability | Owner and intended route | Current evidence |
| --- | --- | --- |
| Stored formal charges, aromatic flags, and covalent bond assignments | ChemicalStates, delivered through `basic.get(..., chemical_state=...)` | Implemented; the native MolSys domain owns the state collection. |
| Charge-center identification and charge interpretation | `physchem`; proposed `get_charge_centers`, subject to naming review | New work. `physchem.get_charge` currently provides residue scales and an OpenMM partial-charge route, not this state-specific participant identification. |
| Connectivity traversal, cycles, and reusable functional-group recognition | `topology`, reading the selected chemical state rather than creating another chemical store | Bond graphs and covalent paths exist; a general ring/functional-group contract needs work. |
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
applicable. Record method, thresholds with units, recognition-rule version,
chemical-state choice, exclusions, and calculation-time software versions.
If RDKit supplies chemistry, retain its version as well as MolSysMT's.
An analysis is attached by the caller under an explicit name.

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
   and cutoff boundaries. Scientific evidence labels distinguish analytical
   correctness from comparison with another implementation.
3. One/many/nonconsecutive/repeated structure indices, empty and variable
   occurrence counts, selection scopes, compound membership, and deterministic
   order are tested. Queries by atoms and structures retain original indices.
4. Supported PBC geometry and images reconstruct the reported distance in
   diagonal, rotated orthogonal, and triclinic boxes. Unsupported split
   participants fail explicitly until their serialization contract exists.
5. InteractionsDict and public H5MSM round trips preserve measures, units,
   occurrence indices, scope, producer versions, and source maps. The calculation
   does not attach or replace analyses automatically.
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
RDKit stays optional and lazily loaded. Existing general APIs are extended
only with documented, compatible semantics.

The result is consumable by MolSysViewer under `uibcdf/molsysviewer#114`.
Its initial integration remains independent. Any extension to the shared
image/result contract requires a separate provider/client agreement and
suite coordination when it changes cross-component obligations.
