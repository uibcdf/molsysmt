---
summary: Provide supported bounded pairwise pose RMSD and geometric clustering.
issue: uibcdf/molsysmt#604
status: active
opened: 2026-11-08
closed:
verification: measured
area: [structure, units, performance, tests]
guard:
normative:
blocked_by: []
supersedes: []
---

# Bounded pairwise pose RMSD and distance clustering

## What, how and why

DockingMT needs a supported provider for comparing existing poses in a common
rigid receptor coordinate frame and grouping their geometric dissimilarities.
The initial consumer population is at most 32 poses; this is not a universal
MolSysMT population limit. See uibcdf/dockingmt#79 and uibcdf/molsysmt#604.

Implement two experimental general tools in `structure`: `get_pairwise_rmsd`
for one declared common atom axis, and `get_distance_clusters` for a physical
distance matrix. Separate saved systems must first be mapped/prepared explicitly;
composition is not evidence that their chemistry or Cartesian frames agree.
Neither operation fits, images, repairs or authenticates a molecular population.
This work does not expand the frozen initial 1.0 integration gates.

## Design and acceptance plan

1. Return a detached unit-bearing dense RMSD matrix, original structure/atom
   indices, unique caller member keys and scientific/execution provenance.
   Preserve requested structure order and repetitions. Empty and singleton
   populations have defined shapes. Nonempty populations require selected atoms.
2. Offer positional ordering and chemically constrained symmetry comparison.
   Reuse public chemical correspondence construction/validation and existing Rust
   positional RMSD kernels. Build chemical evidence once, not once per pair.
   A shared symmetry map set must contain identity and every map's inverse;
   reject directional sets rather than silently averaging or inventing reverse
   distances. Retain complete/anchored/supplied-map search scope. Store mapping
   witnesses only for the explicitly documented query/reference pair orientation.
3. Read only the selected coordinate population through existing projected block
   delivery. The selected coordinates and dense output remain resident: chunked
   input is not an out-of-core result. Preflight numeric RAM and work estimates;
   enforce the declared enumeration, selected-coordinate and output bounds.
   Python chemistry objects, source ownership and total process RSS remain
   outside numeric estimates and must be controlled by the execution environment.
4. Cluster finite, nonnegative, exactly symmetric length matrices with zero
   diagonal. Use explicit inclusive cutoff, complete or single linkage, and
   deterministic earliest-member ties. Return compact member offsets, cluster
   membership, diameter and first/medoid representatives. Score interpretation
   remains downstream. Single linkage may form a chain exceeding the cutoff.
5. Implement the bounded primitive agglomerative algorithm: repeated global
   minimum and max/min distance updates. The mathematical definition follows
   Müllner (2011), sections 2.1 and 2.4, figures 1–2,
   <https://arxiv.org/abs/1109.2378>. It is not his optimized generic, nearest-
   neighbor-chain or MST implementation. The bounded implementation has cubic
   scan work and quadratic resident distance storage. Credit this source through
   documentation, detached references and optional Ackredit. Do not credit SciPy
   as executed software. New compiled clustering is conditional on measurements.
6. Validate analytic translations without fitting, nonconsecutive/repeated
   structures, atom order and symmetry, map rejection, finite-input failures,
   no mutation/aliasing, nm/pm/angstrom and session output units, chain linkage,
   cutoff equality/ties, empty/singleton, work/RAM rejection before large reads,
   optional attribution and bounded saved-file input. Add public API stability
   entries, docstrings, User Guide, Cookbook and course coverage.

## Limits and handoff

The tools operate in caller-declared common Cartesian axes without periodic
reconstruction. Equal atom counts, IDs and source labels cannot prove chemical
or frame equivalence. Positional comparison makes no chemistry claim. A symmetric
restricted-map dissimilarity need not satisfy the triangle inequality.
Cluster populations do not measure probability, free energy, independent sampling,
affinity or biological validity. Member keys preserve labels, not authentication.

DockingMT owns independent receiving of its saved E2 population and installed
dependency profiles. No consumer fallback, source pin update, Viewer addon intent,
candidate publication or new 1.0 gate is implied by provider implementation.

## Execution record

At opening, source and contracts have been inspected; implementation and execution
are pending. Use the shared-host monitored 1 CPU / 2 GiB cgroup route, starting
with small synthetic controls. Preserve at least 2 GiB host available RAM and
terminate this task's execution proactively below 2.5 GiB. Never overwrite attempt
receipts. Report actual checks, failures and measured resources before closing.


### Implemented source and first receiving — 2026-11-08

Both public tools, ArgDigest boundaries, optional DepDigest/RDKit condition,
SMonitor errors, shared attribution helper, experimental API registry and complete
User Guide/Cookbook/course coverage are implemented. Source is not delivered yet.

The first directed run failed on a new fixture/docstring's incorrect root import
of `Structures` (27 passes, 15 failures). Correcting the public import exposed two
fixture expectations: native coordinates are read-only, and unit conversion can
put an intended exact boundary slightly above the computed cutoff (40 passes,
two failures). The finite-input fixture now assigns a new coordinate quantity;
the unit-policy test uses a declared margin, while a separate exact/nextafter test
retains strict inclusive-cutoff coverage. No production tolerance was inserted.
The next directed runs passed 42 and 50 checks respectively.

Integrated receiving passed **2,599 cases**, including the complete `structure`
area, chemical correspondence, optional attribution, three hosted addon preflight
modules, four documentation examples and both public doctests. Peak charged
memory was **735,211,520 bytes**, host available memory stayed above
**14,018,969,600 bytes**, and no OOM/cap/pressure/reserve stop occurred under
1 CPU / 2 GiB. This was a dirty source checkpoint, not exact-commit, installed
or complete-suite qualification. Existing warnings deliberately exercise legacy
format, precision fallback, unavailable GPU and tiny-budget diagnostic paths.

Three new notebooks and the new common-course fragment executed through a real
Jupyter kernel. Existing code cells and outputs in all four comparison modules
and the common structural-operations module remain unchanged. The two new tools
are deliberately not exposed as unreceived Viewer wrappers: the source inventory
lists exactly those two missing routes under #421.

A serial synthetic 25-atom pilot used one warmup and three measured samples for
32/128/256 structures. Positional RMSD medians were approximately
7.1/23.0/84.7 ms; complete-linkage medians 1.65/4.85/16.77 ms; single-linkage medians
1.50/4.59/17.01 ms. All linkage runs requested every merge. Output matrices were
8,192/131,072/524,288 bytes. This shared-host Linux/Python 3.14.7, NumPy 2.4.6
pilot includes validation/units/attribution and checks analytic translations;
it is not a production chemistry benchmark or cross-platform performance claim.
Its aggregate peak was 150,233,088 bytes. Numeric estimates remain estimates,
not measured RSS. Existing compiled RMSD is retained; this bounded workload does
not justify introducing a new compiled clustering backend.

A generic attribution attachment was moved to its owning private scientific
attribution module after the integrated run; exact-source affected checks,
fast gates, rendered documentation inspection and public delivery remain pending.


The pilot also observed that source-overlay calculations inherit another installed
distribution's version string. This pre-existing root bootstrap ambiguity is
tracked separately in #657; exact source manifests/import origins remain the
receiving authority. No installed-package provenance qualification is claimed.
