---
summary: Implement pi-pi interactions with reusable ring and plane tools
issue: uibcdf/molsysmt#265
status: resolved
opened: 2026-09-30
closed: 2026-10-01
verification: measured
area: [api, attribute, structure, performance, docs, tests]
guard: tests/scientific_truth/curated/test_pi_pi_interactions.py::test_protein_observations_match_exhaustive_covariance_reference
normative: devguide/interactions_api.md
blocked_by: []
supersedes: []
---

# Implement pi-pi interactions with reusable ring and plane tools

**Reported:** 2026-09-30, following the validated ionic detector and the user's
request to continue with pi-pi and later cation-pi calculations.
**Status:** Resolved. The experimental detector, reusable foundations, bounded
scientific/performance evidence and public documentation are implemented.

## What

Implement an experimental pi-pi detector producing the common sparse Interactions
contract. Prepare general chemical and geometric tools in their owning modules,
so cation-pi and other workflows can reuse them. MolSysViewer is the concrete
consumer; coordination continues through uibcdf/molsysviewer#114.

## How

1. `topology.get_rings` prepares an unweighted minimum cycle basis from the
   selected state's complete covalent graph. Dative bonds cannot close a cycle.
2. `physchem.get_aromatic_rings` prepares a basis from the explicitly aromatic
   covalent bond subgraph. Unknown atom/bond flags fail; no geometry-based
   aromaticity or residue-name inference is introduced.
3. `structure.get_least_squares_plane` fits planes with centroids, unoriented normals and
   orthogonal RMS/maximum deviations. PBC validation uses the shared PBC layer.
4. The detector uses explicit geometry thresholds, bounded neighbor
   searches, projected coordinate blocks and typed sparse accumulation. It must
   retain state, source axes, evaluated empty frames, complete participants,
   parameters, producer version and observed periodic images. No auto-attachment.

Public functions accept any supported molecular-system form providing the
needed attributes and an existing conversion route. Chemistry is converted once
to native Topology or ChemicalStates when necessary. Typed ChemicalStatesDict
and topology-free MolSys can supply the atom domain and chemical graph directly.
H5MSM 0.5 uses the shared metadata reader;
coordinates and saved analyses are not loaded for ring recognition. Existing
form capabilities must deliver actual chemistry; missing metadata is not
invented. Rich external selections can convert to native MolSys separately.

## Why

The ionic implementation already separated chemical features from observations.
Pi-pi needs the same separation and provides reusable ring participants for later
cation-pi work. Existing principal-axis and PBC machinery needs review before
adding geometry. This is a modular-design decision, not a measured performance
advantage over all alternatives.

## What is measured and what is assumed

**Implemented:** Two public experimental ring tools, common graph/membership
helpers, fixed producer versions and complete-ring selection semantics. The
public experimental plane tool provides form-agnostic unweighted least-squares
geometry, source memberships/indices, finite/unique-normal validation, strict
whole-participant PBC checks and bounded coordinate blocks with resident output.

**Contract-tested:** The combined checkpoint passed 289 tests; the final
preparation/selection refinement passed 61 focused tests. Known memberships,
fused cycles, dative exclusion, missing/contradictory flags, state changes,
empty outputs and metadata-only H5MSM loading are covered.
Native collections, typed dictionaries, RDKit, MDTraj connectivity, topology-free
MolSys and H5MSM inputs are covered, including nonconsecutive structure indices
distinct from structure IDs. The H5MSM guard contains coordinates and a saved
analysis, and fails if either unrelated layer is materialized.

**Scientifically validated, bounded:** The simple/fused aromatic fixtures compare
memberships with independently obtained RDKit SymmSSSR cycles where every cycle
bond is aromatic. This establishes those fixtures, not a universal equivalence.
A controlled nonaromatic fusion-bond graph separately requires its aromatic
perimeter to remain a participant.

**Benchmarked, bounded:** The sequential 100,000-atom / 1,000 isolated-cycle
control is recorded in [the ring guide](../../benchmarking/rings.md), with exact
source hashes, raw timings and separate returned-buffer/process-memory definitions.
Membership arrays occupy 56,008 bytes; source/selected/examined axes bring total
returned NumPy buffers to 2,456,008 bytes. This is not a trajectory detector
benchmark or a total allocation guarantee.

The plane checkpoint passed 119 combined tests and 43 focused tests after the
final scale-independent box refinement. It covers analytical rotations/translation/scale, an independent
covariance oracle for a warped cloud, degeneracy, compound groups, triclinic PBC,
source nonmutation, indices distinct from IDs, projected H5MSM (Structures-only
and alongside saved analyses), native/dictionary/RDKit/MDTraj forms and numerical
budget caps. The executed tutorial includes a bundled phenylalanine ring and a
planarity plot; the executed preparation recipe and all four property course
modules now distinguish chemical participants from fitted geometric planes.

The sequential plane benchmark fits 1,000 groups over 50 selected structures
from a 100,000-atom / 100-structure resident source. Median eager/block times are
0.684/1.472 seconds with 3,256,408 returned numeric bytes; exact hashes and scope
are recorded in [the plane guide](../../benchmarking/planes.md). It does not measure
file I/O, isolated RSS savings or the complete detector.

**Historical checkpoint:** The ring/plane stages did not yet measure pi-pi
detection. The resolution below adds detector geometry, speed, memory and
persistence evidence. General PBC reconstruction and joint viewer loading remain
outside this phase.

## What was refuted

- Filtering the full covalent minimum basis for all-aromatic subrings can miss
  an aromatic perimeter when a nonaromatic fusion bond partitions it. Perceive
  directly on the declared aromatic bond subgraph instead.
- Planarity alone does not supply aromatic chemistry. Do not add a silent
  fallback to residue names, bond-order guesses or spatial inference.
- A cycle basis is not every cycle or a symmetry-preserving ring set. Explicit
  method/version metadata and tied-basis limits prevent that overclaim.
- Full coordinate materialization is unnecessary for chemical participants in
  a modular H5MSM 0.5 file with declared compatible atom axes.
- A declared iterator class alone is not a real structural delivery route.
  General plane fitting uses coordinate getters eagerly for forms with placeholder
  iterators and requests streaming only through declared heavy capabilities.
- Input streaming does not shrink dense output. Smaller blocks trade coordinate
  workspace for repeated group-fitting calls; the plane control measures this cost.

## Scope and exclusions

The current ring tools return packed int64 memberships, source/selected/examined
axes, state index, declared chemistry evidence and producer versions. Each
membership is a sorted atom set, not a cyclic traversal. Complete connectivity
is required or explicitly assumed. The assumption is recorded and never repairs
the source. Selections cutting any perceived ring fail, including shared fused
atoms. The source reference and coordinates remain unchanged.

Minimum bases can change under atom reordering or NetworkX version changes.
A cyclic biconnected block above the explicit default limit of 256 atoms fails
before basis calculation; acyclic chains are not restricted by that limit.
This guards subproblem size, not total RSS or a runtime deadline. General
aromaticity perception, all-cycle enumeration, SymmSSSR, energy interpretation,
new dependencies and a Rust rewrite without profiling are outside this phase.

## Acceptance criteria

- [x] Public form-agnostic ring identification and declared-aromatic participants.
- [x] Analytical plane fitting with explicit units, degeneracy and planarity rules.
- [x] Scientifically explicit pi-pi geometry, selection scope and exclusions.
- [x] Parallel/edge-to-face, near misses, warped and fused rings, evaluated-empty
      frames and periodic image reconstruction tests.
- [x] Native/H5MSM parity, nonconsecutive structures, atom queries and named round trip.
- [x] Independent molecular fixtures and reproducible time/memory measurements.
- [x] Complete detector API, Foundations, Toolbox, Cookbook and four-path documentation.
      Ring/plane docstrings, three executed tutorials, an executed recipe, API registry,
      Foundations and all four physicochemical-property course modules are updated.

The final stage below supplies bounded scientific and execution evidence for
these criteria. Experimental API classification remains explicit; closing the
implementation proposal does not stabilize its physical interpretation.

## References and provenance

- NetworkX minimum cycle basis: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.cycles.minimum_cycle_basis.html
- RDKit aromaticity and ring definitions: https://www.rdkit.org/docs/RDKit_Book.html
- Mol* local reference: `src/mol-model-props/computed/interactions/charged.ts`
  in its upstream repository. Its centroid distance, plane angle and offset
  criteria are reference alternatives, not copied defaults or a parity claim.

The graph implementation uses the existing hard NetworkX dependency. RDKit is
used lazily in optional reference tests; it is not a runtime ring requirement.

## Checkpoint commands

```bash
python -m pytest --receptor=llm tests/topology tests/physchem/test_get_aromatic_rings.py tests/physchem/test_get_charge_centers.py tests/basic/select tests/form/rdkit_Mol tests/interactions/ionic tests/scientific_truth/curated/test_ionic_interactions.py --disable-warnings
python -m pytest --receptor=llm --doctest-modules molsysmt/topology/get_rings.py molsysmt/physchem/get_aromatic_rings.py --disable-warnings
python docs/execute_notebooks.py -q -f -n 2 docs/content/user/tools/topology/get_rings.ipynb docs/content/user/tools/physchem/get_aromatic_rings.ipynb docs/content/user/cookbook/preparing_aromatic_participants.ipynb
python devtools/scripts/validate_course.py
python devtools/scripts/validate_docstrings.py
python devtools/scripts/validate_api_stability.py
python devtools/scripts/validate_dependencies.py
python -m pytest --receptor=llm tests/structure/test_get_least_squares_plane.py tests/structure/get_center tests/physchem/test_get_aromatic_rings.py tests/topology/test_get_rings.py --disable-warnings
python -m pytest --receptor=llm --doctest-modules molsysmt/structure/get_least_squares_plane.py --disable-warnings
python docs/execute_notebooks.py -q -f -n 2 docs/content/user/tools/structure/get_least_squares_plane.ipynb docs/content/user/cookbook/preparing_aromatic_participants.ipynb
python devtools/scripts/benchmark_plane_fitting.py --output /tmp/plane_fitting.json
ruff check molsysmt
```

The combined tests emit expected legacy-file deprecation warnings and deliberate
small-budget memory-pressure diagnostics. These are not silently suppressed
scientific skips. The current course gate is devtools/scripts/validate_course.py;
the older course-local script uses obsolete section/filename expectations.

## Unit-policy audit after plane review

The user's review requested an explicit least-squares name, evidence before a
Rust implementation and confirmation that session length units remain authoritative.
The user selected `get_least_squares_plane`; the experimental public function,
source/test/tutorial files, API registry and maintained examples now use that name.
It replaces the unreleased review name `get_plane`, without adding another alias.

The current numerical boundary explicitly extracts coordinates and boxes in nm.
Returned length quantities are constructed with their actual internal unit and
standardized under the active PyUnitWizard policy. Dimensionless normals are not
rescaled. This does not configure the user's policy or assume that the session
still uses nm. Existing storage and H5MSM wire conventions remain separate from
user-facing output units.

The unit regression suite now uses temporary contexts and covers coordinate
inputs in angstrom, nm, pm and meters; outputs in nm, angstrom, micrometers and
pm; warped-plane deviations, mixed coordinate/box units, eager/native-streamed
paths, nested-context restoration and quantity backends selected by the user.
The tutorial executes a temporary angstrom output policy.
The focused checkpoint passes 60 tests, including all four installed quantity
backends (Pint, OpenMM, Unyt and Astropy); the updated tutorial executes cleanly.
The named public API passes 139 combined plane/center/ring tests and its doctest.

An exploratory cProfile control (1,000 six-atom groups, 50 structures) puts most
cost in geometric preparation/fitting, with substantial NumPy SVD time and Python
per-group work. This is a localization observation, not a Rust comparison or a
new speed claim. Before changing the numerical algorithm, compare bounded
batched SVD and a bundled Rust candidate against the same scaled/degenerate and
unit contracts. Existing principal-axis covariance routines are not assumed to
preserve SVD conditioning or the current singular-value-gap diagnostic.

## Plane kernel decision — 2026-09-30

**Implemented:** the public plane tool now delegates packed groups to the bundled
Rust/Faer rectangular SVD. Units, digestion, form delivery, selection and PBC stay
at the Python boundary. Frame parallelism follows session configuration; groups
within a frame are sequential. Right vectors only are computed. Packed indices
and strided float64 coordinates are borrowed. Degeneracy, sign, output shapes,
source indices and the unweighted scientific criterion are preserved.

**Benchmarked:** six isolated workloads compare frozen group-wise NumPy, bounded
batched NumPy, Rust with one thread and Rust with four threads. Single-thread Rust
wins every measured workload. In the 50-structure/1,000-group numeric case the
medians are 507.738, 309.934, 149.641 and 46.494 ms respectively. Batched NumPy is
useful but does not justify retaining a second production implementation here.
Four-thread benefits depend on frame count; a one-frame group list remains serial.
The method, raw samples, hashes, versions and memory limits are in
[the plane benchmark guide](../../benchmarking/planes.md) and its linked artifacts.
The final integrated public benchmark records 0.074 s eager and 0.176 s for
eight-frame blocks, with the same 3,256,408 returned numeric bytes. The older
0.684/1.472 s observations remain a separate historical checkpoint.

**Refuted:** the first Nalgebra candidate had inaccurate right vectors in the
rotated warped hexagon despite RMS agreement. It was rejected without widening
tolerances. The Faer candidate passes a covariance-oracle component and maximum-
deviation regression while production retains rectangular SVD conditioning.
The raw prototype discrepancies are preserved in the benchmark guide.

**Memory:** the Rust kernel is not universally lower in process RSS than NumPy.
The 50-by-1,000 case uses about 86.0/86.5 MiB with one/four threads versus 84.9 MiB
for grouped NumPy; the bounded NumPy batch control uses about 94.5 MiB. These are
isolated process high-water marks, not allocation deltas. Actual Faer scratch
requirements exposed an underestimated small-group reserve; 2,048 additional
bytes per frame now cover the aligned workspace. A native guard checks this
estimate against the dependency's required scratch and matrix padding.

**Validated checkpoint:** 190 combined Python geometry/ring/packaging tests,
81 Rust tests, the public plane doctest, and both executed plane/aromatic-preparation
notebooks pass. Unit policies and supported eager/streamed forms retain their
coverage. The four course Module 39 explanations and Structures foundation remain
accurate because the user contract is unchanged; the course validator covers all
156 notebooks. Ruff, production Clippy with warnings denied, Rust formatting,
API/docstring/dependency/developer-guide gates pass. Local non-editable Linux
wheel validation checks all 101 private exports and a public Angstrom-input plane
smoke. This is not a new supported-platform wheel matrix or a stabilized pi-pi API.

Installed-wheel inspection also restored the manifest entry for the already
implemented `get_mic_pair_observations` kernel and factored its return type so the
existing production Clippy gate passes. Generated data caches leaking into a
local wheel were reported and repaired in uibcdf/molsysmt#267, with a real
setuptools resource-preservation guard. No Rust or Python dependency was added.

The next implementation stage remains the pi-pi detector using the shared ring,
plane, spatial-candidate and periodic-image tools. This kernel decision does not
close the detector proposal.

## Detector resolution — 2026-10-01

**Decision:** Accepted and implemented as the experimental
interactions.pi_pi.get_pi_pi_interactions public tool. No new dependency or
feature-specific Rust kernel was justified by this measured stage.

**Implemented:** Explicit distance/angle/offset/maximum-planarity cutoffs,
centroid_angle_offset@1 method version, parallel and edge-to-face evidence,
complete ring_a/ring_b memberships, source indices, evaluated empty frames,
state/evidence/producer metadata, full-versus-eligible scope, observed MIC images,
Interactions/InteractionsDict output and explicit named attachment. Internal,
incident and disjoint between scopes are supported. Self, overlapping/fused and
directly covalently linked rings are excluded; other intramolecular pairs are
included. No energy, attraction, clash or residue/component inference is added.

General plane-pair geometry belongs to structure, whole-participant MIC checks
to pbc, and compound selection membership is now reused by ionic and ring tools.
The detector uses the existing compiled plane/spatial kernels and vectorized
candidate geometry. Every selected frame is searched. H5MSM index selections
prepare chemistry once and read projected blocks without saved analyses.
Rich H5MSM selections require bounded eager materialization and reject forced
streaming before loading the source. Other forms use actual declared streaming
support or their eager coordinate getter/conversion route. Chemistry-only input
without a declared structure axis fails clearly.

**Scientifically validated, bounded:** Fixed independent aromatic memberships on
checksum-preserved Trp-cage/villin protein coordinates agree with RDKit aromatic
SymmSSSR cycles for those fixtures. An exhaustive independent covariance-plane
oracle compares every eligible ring pair and each retained geometric measure,
including native/file and eager/block routes. Controlled triclinic image
translations reconstruct the same observed geometry. A separate analytical suite
covers both classes, near-miss distance/angle/offset cutoffs, warped/degenerate
rings, fused/direct-covalent exclusions, nonconsecutive/repeated frames, full-ring
calculation scopes, atom queries, named/dictionary/image-preserving persistence,
remapping, nondefault length/angle policies and unsupported/invalid routes.
This bounds geometric observations, not universal aromaticity or an energy model.
Evidence categorical codes are local to their label tables: round-trip assertions
compare their logical labels and preserve public occurrence indices.

**Benchmarked, bounded:** Isolated sequential controls measure the full detector,
queries, numeric bytes, Linux VmHWM and standalone H5MSM I/O. With 100,000 atoms,
100 structures and 1,000 rings, 36,660 occurrences use 4,330,336 numeric result bytes
before inverse indexing; native eager median is 0.930 s and H5MSM blocks 3.062 s.
With 10,000 atoms, 1,000 structures and 200 rings, 73,200 occurrences use 6,861,616
bytes; native eager median is 1.016 s and H5MSM blocks 4.393 s. Source coordinates
occupy 240 MB in both controls. File blocks lower measured process high-water
marks but cost more repeated calls. The complete result remains resident.
Regular synthetic values compress especially well; disk ratios and reused-atom
query timings are not general workload promises. Raw samples, hashes, hardware,
software/thread configuration and exact memory/I/O scopes are in
[the pi-pi benchmark guide](../../benchmarking/pi_pi.md).

**Documentation:** The public docstring/doctest, experimental API registry,
Foundations, complete Toolbox tutorial, Cookbook persistence recipe, benchmark
methods and all four Module 39 course explanations are updated. Both new
notebooks execute with plots, periodic geometry, explicit outputs, named/public
conversion, file calculation, standalone persistence and frame queries. The
frozen legacy course code/outputs remain preserved; this stage does not certify
unrelated legacy network-dependent exercises.

**Final scientific/native checkpoint:** 283 tests pass across pi-pi, independent
molecular oracles, ionic/shared memberships, ring/plane tools, native boxes and
public MolSys/H5MSM workflows. Deliberate small-budget memory-pressure and
incompatible-box diagnostics remain visible. Over-budget accumulation and invalid
later blocks must raise before finalizing any partial analysis. The new detector
API stays Experimental.

The executed periodic tutorial exposed a pre-existing full-box setter no-op,
separately recorded and repaired in uibcdf/molsysmt#268. Full native/public
assignment now initializes a missing box with explicit units; partial
initialization fails rather than inventing other frame values. This is not a
change to the detector's documented missing-box MIC policy.

**Remaining limits:** General aromaticity perception, all-cycle enumeration,
automatic split-ring reconstruction, energy scoring, an incremental result
writer, arbitrary out-of-core accepted-output sizes and joint viewer/session
measurements are outside this resolved implementation. Cation-pi can reuse the
chemical charge/ring and geometric foundations in a separately tracked stage.

Reproduction commands:

```bash
python -m pytest --receptor=llm tests/interactions/pi_pi tests/scientific_truth/curated/test_pi_pi_interactions.py --disable-warnings
python -m pytest --receptor=llm --doctest-modules molsysmt/interactions/pi_pi/get_pi_pi_interactions.py --disable-warnings
python docs/execute_notebooks.py -q -f -n 2 docs/content/user/tools/interactions/get_pi_pi_interactions.ipynb docs/content/user/cookbook/saving_pi_pi_interactions.ipynb
python devtools/scripts/benchmark_pi_pi_interactions.py --output /tmp/pi_pi_100k_100.json
python devtools/scripts/benchmark_pi_pi_interactions.py --atoms 10000 --structures 1000 --rings 200 --output /tmp/pi_pi_10k_1000.json
```

Final documentation review also checks actual notebook schemas with nbformat:
legacy Module 39 files retain their 4.4 cell schema, so newer cell-id metadata
is omitted. Their scientific code and executed outputs are unchanged. The full
HTML build succeeds; unrelated existing navigation/reference warnings remain
visible in the build log. The new pi-pi API page is part of the API toctree.
Angular roundoff is capped below pi/4; an exact 45-degree acceptance guard
prevents nominally disjoint classes overlapping at the last floating-point bit.

Final form review confirms the composite Topology/Structures calculation route.
Separately supplied ChemicalStates/Structures (including ChemicalStatesDict)
expose an existing generic conversion limitation, recorded in
uibcdf/molsysmt#269. The supported topology-free routes are a native MolSys or
H5MSM containing both domains; the detector does not provide a competing private
domain-composition implementation.
