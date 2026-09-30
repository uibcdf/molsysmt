---
summary: Implement ionic interactions with reusable molecular tools
issue: uibcdf/molsysmt#261
status: resolved
opened: 2026-09-30
closed: 2026-09-30
verification: measured
area: [api, attribute, structure, pbc, performance, docs]
guard: tests/scientific_truth/curated/test_ionic_interactions.py
normative: interactions_api.md
blocked_by: []
supersedes: []
---

# Implement ionic interactions with reusable molecular tools

**Reported:** 2026-09-30, following the maintainer's review of additional
interaction families and source inspection of molecular analysis libraries.
**Status:** Resolved for the bounded experimental formal-charge/minimum-distance
method. Reusable chemical, geometric, PBC, and sparse execution tools are
implemented; analytical and independent molecular controls, eager/chunked
parity, persistence, and synthetic/molecular measurements complete the accepted
first delivery. Pi-pi and cation-pi follow as separately scoped families.
Expanded recognition remains `uibcdf/molsysmt#262`; no universal chemistry,
experimental protonation, electrostatic energy, stability, or total RAM guarantee
is claimed.

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
| Sparse analysis, query, attachment, and persistence | Interactions, MolSys.interactions, InteractionsDict, and H5MSM | Existing experimental contract; see the [interaction API](../../interactions_api.md). |

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
are design concepts; the delivered method records source and participant
definition as parameters rather than exposing every source as a selector.
Prefer extending an existing general
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
[charge-center coverage proposal](../../pending_proposals/expand_and_validate_formal_charge_center_recognition.md).
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

This first-tool checkpoint did not deliver the detector, PBC observations,
chunked execution, or Interactions persistence. The subsequent checkpoint
below records the detector delivery separately.

### Eager detector checkpoint — 2026-09-30

The experimental public operation is now
`interactions.ionic.get_ionic_interactions(molecular_system, distance_threshold,
...)`. The threshold is required and unitful. Its `minimum_distance` method
observes opposite formal-charge centers under the recognizer's bounded
definition. It accepts distances at the cutoff with one float64 ULP allowance
for unit-conversion roundoff. This is geometric evidence, not energy or a bond.

Calculation scopes are `selection_mode='internal'`, `'incident'`, or `'between'`.
Between selections must be disjoint and both explicit. Whole-center selections
are required; result queries retain the established atom-set semantics. Repeated
structure indices are deduplicated and evaluated in sorted order, including
zero-occurrence frames. Intramolecular contacts are included, directly covalently
linked centers are excluded, and dative bonds do not impose that exclusion.

The computation delegates sparse atom candidates and MIC images to existing
Rust kernels. Scope planning limits incident/between candidate searches to
pertinent oriented center sets, rather than generating unrelated center pairs
and retaining only their final filtered rows. The reusable grouped-minimum primitive lives in
`structure/_group_minimum_contacts.py`; an anchor-relative whole-participant
image check lives in `pbc/_whole_participants.py`. Both have independent
analytical tests. Integer membership packing moved to a shared private utility
rather than maintaining a copy per feature/detector. The signature guard's
explicit waiver records this unexported helper relocation; the public
charge-center signature is unchanged.

Arrays accumulate occurrence frame indices, center pairs, distances, and
images. NumPy identifies unique relations across frames before direct typed
Interactions construction. There is no Python dictionary per occurrence or
dense atom-pair matrix. One center pair has at most one occurrence per frame,
even when several geometry-reference atom pairs meet the cutoff. Equal minima
select reference indices deterministically; this method does not enumerate all
periodic images.

Periodic observations use one original-box image per whole participant. Any
eligible participant requiring internal anchor-relative MIC shifts is rejected
when pair geometry is evaluated. The guard is a stated bounded condition, not
a general component compactness criterion or an automatic reconstruction.
Tests reproduce measures in diagonal, rotated orthogonal, and triclinic boxes,
and reject a split carboxylate.

Results default to `molsysmt.Interactions`; `output_type='molsysmt.InteractionsDict'`
returns the existing typed versioned payload. Parameters record threshold units,
recognition definition/version/state and evidence, scope and exclusions, eager
execution, and periodic policy. Measures contain nm distances and elementary
participant charges. Producer software versions and actual images persist in
public H5MSM 0.5 round trips. Attachment remains an explicit caller action.

At the initial eager-delivery checkpoint, coordinates, candidates, and the complete sparse
result reside in memory. It rejects an estimated full source coordinate
footprint exceeding `configure.max_ram_usage`, even for a small frame selection.
For a direct H5MSM 0.5 path, a shared private metadata preflight reads existing
axis cardinalities before materialization; the detector then materializes the
file once. This prevents repeated file loads by downstream basic queries.
The full reader still validates domain associations. Coordinate footprint is
an estimate, not a total RAM bound; chemistry, conversions, existing analyses,
candidates, packing, and output can dominate. Other source conversion routes
may allocate before the estimate and are not claimed streaming-safe.

Delivery evidence:

- `tests/interactions/ionic/test_get_ionic_interactions.py` exercises analytical
  cutoff controls, atomic and compound centers, neutral controls, selections,
  state-dependent charge/connectivity, original frame indices distinct from IDs,
  missing data, producer evidence, images, dictionary/file round trips,
  extraction/remapping, non-default unit sessions, and preflight failures.
- `tests/structure/test_group_minimum_contacts.py` and
  `tests/pbc/test_whole_participants.py` protect the independent general helpers.
- The focused run including the existing charge-center tests passes:
  **80 passed**. Both public docstrings pass together: **2 passed**.
- A focused compatibility run for the existing hydrogen-bond namespace,
  disulfide detector, public H5MSM workflow, and producer provenance passes:
  **21 passed**, with the expected warning for a bundled legacy 0.4 file.
- The new detector tutorial and named-persistence recipe were executed.
  Foundations and the four Module 39 course paths document the bounded route;
  existing course code/outputs were preserved rather than re-executed.

The issue remained active at this eager-delivery checkpoint. The later integration
and measurement checkpoints below supersede its pending chunking/budget work;
real-system acceptance remains open. No throughput, total memory
bound, comprehensive chemistry validation, or stabilization is claimed.

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

### Shared execution checkpoint — 2026-09-30

Preparing the ionic sparse reducer exposed the shared boundary defect
`uibcdf/molsysmt#263`: IDs were delivered as indices and units were stripped
without canonical conversion. The boundary and existing structure consumers
have been corrected. Requested and total frame counts are now distinct,
empty selections do not open the trajectory, and invalid delivery fails
before finalization.

Native iteration also copied the full Structures domain during iterator
construction, then copied the full coordinate series before selecting each
block. The iterator now reads the source domain directly, and the getter
copies only the projected coordinate block. Copy-size and forbidden-extraction
tests protect those properties without claiming a measured peak-RAM reduction.

The shared executor can preflight H5MSM 0.5 dimensions from metadata and use
a projected structural iterator for coordinates, box, time, and structure
IDs. It preserves selected atom order, nonconsecutive/repeated frame traversal,
and partial blocks. Structural metadata validation is reused with the
independent reader. This iterator does not prepare chemical domains or
validate cross-domain atom/state associations.

This shared-boundary checkpoint preceded the ionic integration described
below. Other public H5MSM 0.5 preflight routes can still materialize domains;
the file iterator alone does not establish a whole-pipeline memory guarantee.

### Ionic chunked integration checkpoint — 2026-09-30

**Implemented / parity-tested:** keyword-only `heavy_mode='auto'` uses a
sparse reducer and shared ChunkedExecutor on native MolSys and H5MSM 0.5 with
index selections or `all`. Preparation examines source chemistry once. The
file route reads chemistry/association metadata without structural series or
saved analyses, checks identity atom links, and resolves one selected chemical
state. Coordinate blocks project eligible whole participants. Typed columns
accumulate per block, retaining source structure indices and evaluated-empty
coverage. Group minima use bounded source batches; final observations have
deterministic ordering, scientific provenance, charges, and periodic images.

Working estimates and explicit failure limits are normative in
[`SCALABILITY.md`](../../SCALABILITY.md). The complete sparse result is resident;
no incremental writer, checkpoint/resume, or total process RAM bound is
claimed. Conservative candidate bounds may reject actually sparse cases.
Rich string selections retain eager execution and reject forced chunking.

Executable guards are `tests/interactions/ionic/test_chunked_ionic.py`,
`tests/heavy/test_sparse_accumulator.py`, and
`tests/structure/test_group_minimum_contacts.py`, together with the existing
chemical recognition, ionic analytical, public persistence, and shared executor
tests. They compare supported native/file eager/chunked paths, nonconsecutive
and repeated indices, internal/incident/between scopes, compound participants,
triclinic images, state associations, typed empties, budgets, missing data,
and a later-block scientific failure before finalization. User Guide and
Cookbook examples demonstrate execution choices and public persistence; all
four affected course modules describe the delivered scope.

**At this chunked checkpoint, remaining:** real molecular systems with explicit source chemistry,
independent scientific controls, and performance measurements on those systems.
The bounded synthetic measures below do not establish recognition of new
motifs or an acceptable speed at arbitrary charged-center density. Broader
recognition remains independently tracked by `uibcdf/molsysmt#262`.

### Synthetic ionic measurements — 2026-09-30

**Benchmarked:** `devtools/scripts/benchmark_ionic_interactions.py` runs four
sequential worker processes per case (native/file, eager/chunked). Workers
warm geometry with an independent two-atom control, then repeat calculation
three times (two for the largest source). Medians are reported; OS page-cache
state, CPU frequency, and external host activity are uncontrolled. No other
local benchmark or test workload was scheduled during these final samples.
Hardware: Intel Xeon E5-2630 v4, 2.20 GHz, Linux x86_64; Python 3.13.14, NumPy
2.4.6, h5py 3.16.0. Reports preserve environment, calculation samples, source
load cost, stage medians, and hashes of the benchmark/detector/reducer. The
source checkpoint is a dirty implementation based on `c5cd7b13b`; the runtime
package version label alone does not identify this source revision.

Synthetic separated Na/Cl pairs have variable and evaluated-empty frames.
The 100,000-atom case contains only 100 charged atoms; neutral He controls
the full source axis and coordinate size. It is not a biological dataset,
a 100,000-charged-center test, or a 10,000-structure throughput claim.

| Atoms × structures (charged atoms) | Source | Mode / blocks | Median calculation (s) | Worker peak RSS (MiB) |
| --- | --- | --- | --- | --- |
| 1,000 × 300 (1,000) | native | off / 1 | 1.186 | 455.1 |
| 1,000 × 300 (1,000) | native | force / 10 | 1.252 | 449.2 |
| 1,000 × 300 (1,000) | file | off / 1 | 1.781 | 434.8 |
| 1,000 × 300 (1,000) | file | force / 10 | 2.086 | 425.5 |
| 10,000 × 30 (10,000) | native | off / 1 | 5.255 | 462.7 |
| 10,000 × 30 (10,000) | native | force / 4 | 5.827 | 457.0 |
| 10,000 × 30 (10,000) | file | off / 1 | 6.124 | 443.4 |
| 10,000 × 30 (10,000) | file | force / 4 | 6.670 | 432.6 |
| 100,000 × 100 (100) | native | off / 1 | 0.339 | 918.8 |
| 100,000 × 100 (100) | native | force / 7 | 0.342 | 920.2 |
| 100,000 × 100 (100) | file | off / 1 | 0.914 | 446.1 |
| 100,000 × 100 (100) | file | force / 7 | 0.922 | 446.0 |

RSS is Linux `/proc/self/status:VmHWM`, from worker exec through source
loading, calculation, indexing, interaction-layer writing and reading. It
includes the runtime and is not the peak of calculation alone. The separate
`rusage_peak_rss_bytes` can include an inherited pre-exec parent high-water
mark; it must not be used to estimate projected-file memory savings. Parent
fixture generation and combined parent/worker residency are not included.

Coordinate payloads are 7.2 MB, 7.2 MB, and 240 MB. The first two cases yield
109,980 and 109,998 occurrences; the dilute case yields 3,660. Eager and
chunked modes have the same counts, numeric result sizes, and compressed
interaction-layer file sizes for each case. Full semantic parity is protected
by tests rather than inferred from matching counts.

**Interpretation:** blocks add orchestration/I/O cost on these small selected
coordinate payloads. File mode at 1,000 × 300 rises from 1.781 to 2.086 s,
while worker peak RSS falls from 434.8 to 425.5 MiB. At 100,000 × 100 only
100 eligible atoms are projected, so both file modes already avoid the full
240 MB coordinate payload. Their worker peak is about 446 MiB versus about
920 MiB for the route that first loads the complete native system; that
comparison includes loading and serialization and does not isolate chunking.

For 10,000 charged atoms, grouped geometry takes roughly 5–5.5 s and neighbor
search takes roughly 4.7–5.2 s. Conservative candidate batching can rebuild
spatial data multiple times per structure. The next optimization to evaluate
is a reusable bounded neighbor interface that reuses target spatial data.
For the dilute case, file chemistry reading takes about 0.53 s and recognition
about 0.18 s, compared with about 0.05 s of neighbor search. These are different
bottlenecks; compiling result packing alone would not address either one.

Stage timers are inclusive: consume includes grouped geometry, grouped
geometry includes neighbors. Derived differences between medians estimate
group reduction and validation/acceptance/accumulation; they are not independent
additive measurements. End-to-end time also includes untimed preparation and I/O.

| Case | Numeric result before/after indexes (MB) | Frame query (µs) | Warm atom query (µs) | First atom query (ms) | H5MSM layer size (bytes) | Write/read (ms) |
| --- | --- | --- | --- | --- | --- | --- |
| 1,000 × 300 | 5.768 / 6.668 | 67.5 | 59.7 | 5.09 | 163,936 | 39.0 / 46.2 |
| 10,000 × 30 | 6.160 / 7.240 | 69.8 | 34.8 | 30.54 | 310,201 | 49.6 / 81.6 |
| 100,000 × 100 | 0.996 / 1.826 | 66.5 | 38.9 | 0.94 | 61,736 | 10.3 / 33.6 |

Query medians use 50 repeated calls after index construction. Numeric bytes
exclude Python objects; even a dilute result retains axis-sized maps/index
offsets. Persistence uses public `write_layers`/`read_layers` on interactions
only, validates frames and distances, and is distinct from saving the source
coordinates. Compound images and named full-system round trips are test-covered.

Reproduce sequentially from the repository root on Linux:

```bash
python devtools/scripts/benchmark_ionic_interactions.py --atoms 1000 --frames 300 --repeats 3 --chunk 32 --output /tmp/ionic_1000x300.json
python devtools/scripts/benchmark_ionic_interactions.py --atoms 10000 --frames 30 --repeats 3 --chunk 8 --output /tmp/ionic_10000x30.json
python devtools/scripts/benchmark_ionic_interactions.py --atoms 100000 --frames 100 --charged-atoms 100 --repeats 2 --chunk 16 --budget 2147483648 --output /tmp/ionic_100000x100_dilute.json
```

Raw snapshots:

- [1,000 × 300](../../../benchmarks/baselines/ionic_1000x300.json).
- [10,000 × 30](../../../benchmarks/baselines/ionic_10000x30.json).
- [100,000 × 100, dilute charges](../../../benchmarks/baselines/ionic_100000x100_dilute.json).

Earlier chunked checkpoint validation: **780 passed** across heavy execution, ionic detection,
charge-center recognition, grouped geometry, diagnostic catalog, native form
routes, and public MolSys/H5MSM workflow. Toolbox and Cookbook notebooks were
executed successfully. These measurements leave the issue active until the
real-system scientific and performance acceptance above is completed.

### Molecular validation and closure — 2026-09-30

**Scientifically validated within the declared method/state scope:** bundled
1L2Y coordinates (304 atoms, all 38 NMR models) and 1VII coordinates (596 atoms,
one model) are unchanged. A checksum-pinned independent fixture manifest
specifies every formal charge, complete participant membership, and reference
atoms. RDKit reads source connectivity/orders. The modeling state charges
N-termini, Lys and Arg and deprotonates Asp/Glu and C-termini; all other formal
charges are zero. This is explicitly declared fixture preparation, not a
production protonation rule or experimental protonation measurement.

Independent RDKit SMARTS establish carboxylate/guanidinium memberships. A
separate exhaustive Cartesian displacement calculation uses the fixed reference
memberships rather than MolSysMT centers, neighbors, or geometry. It checks
observation keys, roles, counts and distances, native/file sources, eager/chunked
execution, and explicit cutoffs. Fixed counts are 20/61 for Trp-cage at 0.4/0.8
nm and 0/4 for villin at those cutoffs; 0.8 nm is a positive-output control,
not a recommended biological threshold. No reference value consumes detector
output. Selected frames `[37, 0, 13, 37]` cover deduplication and empty coverage,
internal/incident/between scopes, combined atom/frame queries, named full-system
H5MSM persistence, occurrence indices, parameters, and producer versions.
Controlled triclinic lattice shifts of whole participants on real coordinates
preserve the independent nonperiodic distances and reconstruct every observation
from the actual serialized image. This is a periodic representation control,
not another molecular dynamics dataset.

**Benchmarked:** the same sequential worker harness measures real Trp-cage,
a 100-cycle repetition (3,800 frames, only 38 independent structures), and
villin at the explicit 0.8 nm control. Each worker validates all observations
against the independent reference outside its calculation timer. Date, hardware,
versions, samples, source/implementation hashes, state definition, warmup,
stage timings, queries, resident bytes, public persistence and Linux VmHWM are
recorded in `benchmarks/baselines/ionic_real_*.json`. The maintained operational
[ionic benchmark guide](../../benchmarking/ionic.md) holds reproduction commands,
numbers and interpretation. Native calculation medians are about 27/29 ms
(eager/chunked) for the 38-model ensemble and 1.24/1.27 s for its repeated control;
file medians include chemical preparation. Chunking is a memory-workspace
choice and does not universally accelerate these cases. Runtime and source
loading dominate whole-worker peak RSS for these small results.

Closure evidence: the combined charge-center, ionic, grouped geometry, whole
participant PBC, sparse accumulator, molecular oracle and provenance selection
passes **129 tests**. The final molecular controls pass **22 tests**, with no
skips. The detector and persistence notebooks execute successfully. Ruff,
public API, docstring, dependencies, course, scientific registry structure and
developer-guide gates pass. Production detector/kernel code is unchanged in
this validation checkpoint. The API remains Experimental; these focused
results are not a release-candidate certificate or validation of other families.

Durable method rules are absorbed by [`interactions_api.md`](../../interactions_api.md),
working limits by [`SCALABILITY.md`](../../SCALABILITY.md), and benchmark procedures
by [`benchmarking/ionic.md`](../../benchmarking/ionic.md). The closure guard is
`tests/scientific_truth/curated/test_ionic_interactions.py`; expected memberships,
counts and Cartesian distances fail if recognition, frame/scope semantics,
periodic images, or persisted observations regress. The earlier pending
real-system statements in dated checkpoints below/above describe their historical
state and are superseded by this closure.

### Public surface and remaining design

The first exported experimental family route is
`interactions.ionic.get_ionic_interactions`. Its arguments include
`molecular_system`, `selection`, `selection_2`, `structure_indices`,
`chemical_state`, `method`, `selection_mode`, `pbc`, `syntax`, `output_type`,
the required `distance_threshold`, `assume_complete_connectivity`, and
keyword-only `heavy_mode`.
Its default output is `molsysmt.Interactions`; the optional
`molsysmt.InteractionsDict` output uses the existing public conversion.
Additional source/method routes need separate docstring and digestion review.
Existing detector defaults remain as documented.

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

Follow the [Rust optimization guide](../../rust_kernel_optimization_guide.md)
and [heavy-trajectory contract](../../SCALABILITY.md), preserving deterministic
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
  and chemically sufficient; see the [readiness proposal](../../pending_proposals/diagnose_ligand_chemical_readiness_for_a_selected_molecular_state.md).
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
