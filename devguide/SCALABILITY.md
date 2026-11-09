# Scalability and Heavy-Trajectory Contract

MolSysMT contains an internal chunked-execution framework for trajectories that
should not be loaded into memory at once. This document describes the current
contract, not the complete pre-1.0 design history, which is archived under
`archive/assessments/`.

## Current public scope

The public heavy path is currently integrated into these structure operations:

- `molsysmt.structure.get_center`;
- `molsysmt.structure.get_rmsd`;
- `molsysmt.structure.get_distances`.
- `molsysmt.structure.get_least_squares_plane`.

`molsysmt.interactions.ionic.get_ionic_interactions` also uses this executor
for native MolSys and H5MSM 0.5 paths with atom-index selections or `"all"`.
Its complete sparse output remains resident; input streaming does not imply
disk-backed output.

Eligibility is narrower than the full eager API. It depends on the operation,
selection shape, comparison mode, output, and whether the input form advertises
the required attributes in `_heavy_support`. Unsupported combinations must use
the eager path or fail explicitly; they must not be described as generally
out-of-core capable.

## Decision policy

Resident interaction results can be explicitly compacted after frame edits with
`Interactions.compact()`. This releases references to retired observation blocks
through a new packed snapshot. Allocation includes the packed output, at most
one destination column while freezing it, bounded translation workspace and
frame/run metadata. Old snapshots still keep their data alive. Relation catalog
definitions are preserved, including unused ones. HDF5 saving already traverses
active blocks without compaction; neither operation supplies detector-to-file
accumulation. See [the compaction contract](interactions_api.md#explicit-observation-compaction)
and [the paired measurements](benchmarking/h5msm.md#compacting-resident-interaction-observations).

`molsysmt._private.execution.memory_policy` estimates the coordinate footprint
from atom and structure counts. `heavy_mode` controls the decision:

- `"auto"`: select heavy execution when the estimated footprint exceeds the
  configured RAM budget;
- `"force"`: request heavy execution;
- `"off"`: use eager execution.

`max_ram_usage`, `chunk_size`, `chunk_memory_fraction`, and
`memory_pressure_threshold` configure the policy. The footprint is an estimate,
not a complete peak-memory proof; reducers and outputs may dominate memory use.

## Chunk contract

`ChunkedExecutor` obtains chunks from a form-specific `StructuresIterator` and
builds dictionaries with these keys:

- `coordinates`: read-only `float64` values in nm;
- `box`: read-only `float64` values in nm, or `None`;
- `time`: read-only `float64` values in ps, or `None`;
- `structure_indices`: read-only `int64` source structure indices, in the
  requested traversal order, including repetitions;
- `structure_id`: read-only source identifiers when the iterator was asked
  to deliver them, otherwise `None`. Identifiers never supply indices.

The executor converts quantities explicitly to nm and ps, independently of
session standard units. Public structure reducers wrap their numeric outputs
with the canonical unit before any session-unit standardization. Making chunk
views read-only does not make caller-owned source arrays read-only.

Eager and heavy reducer metadata distinguish `n_structures` (requested count)
from `n_structures_total` (source count). Empty traversals initialize and finalize
reducers without opening the trajectory. A reducer must implement its own
typed empty result if its public operation accepts empty selections. Short,
excess, misaligned, or incorrectly indexed delivery raises before finalization.

Reducers must copy an array before mutating it. Scientific logic belongs in the
reducer; the executor owns iteration, policy, and orchestration.

### Source projections

Native `MolSys` iteration reads its existing `structures` domain directly.
Native coordinate getters select the requested rows before copying. These
paths avoid an additional full-source coordinate copy; the source remains
resident in RAM and the reducer may still accumulate a large result.

For a path to H5MSM 0.5 or experimental 0.6, executor dimension preflight reads axis metadata.
The file-form iterator projects coordinates, box, time, and structure IDs in
blocks and validates structural-series shapes and units before delivery.
It preserves nonconsecutive and repeated frame indices and requested atom
order, and closes its owned handle on completion or context exit. Other
structural attributes are not supported by this iterator yet. The existing
H5MSM 0.4 file and handler iterators retain their legacy schema route.

Public H5MSM 0.5 `get`, `select` and `has_attribute` retain the file form rather
than using the eager compatibility bridge. Counts and numeric selections use
metadata; dense structural getters read only requested fields and atom/structure
positions. MolSysMT expressions reuse scoped native inventory/chemical domains,
and spatial expressions read their requested structures. One lexical query
owns its static decoded domains and closes its HDF5 handles on every exit;
there is no persistent file cache. This is the [#643 query correction](archive/resolved_bugs/h5msm_0_5_queries_read_full_coordinate_series_before_applying_selection.md).

Experimental 0.6 uses the same structural iterator/query primitives. Coordinate
queries do not decode mechanics; mechanical queries decode that resident domain
once per lexical scope, without loading coordinates or other native domains.
Metadata cardinalities can be read through `h5msm.read_axis_sizes` without payload
arrays. This does not make full resident or subset conversion streaming.

This does not establish bounded memory for an entire public analysis. Static
domains and explicit association maps may be decoded in full when required;
sparse alternate-site readers can retain their offset/index vectors. External
selection backends retain their conversion routes. Full resident conversion,
selected-layer loading and sparse/dense output storage need their own budgets.
HDF5 decompression may touch complete stored chunks even when logical selections
are smaller. Tests observe dataset windows, not physical disk bytes or total RSS.

### Whole H5MSM topology conversion

`basic.convert` admits a stored-topology projection from one scalar H5MSM 0.5
path when `to_form="molsysmt.Topology"`, selection and structure indices are
`"all"`, syntax is `"MolSysMT"`, strict/report flags are false,
`from_naming_scheme` is None and no converter kwargs are supplied. It delegates
to public `h5msm.read_layers(..., layers=["topology"])` and the native reader.
The target uses its stored index space without joining other layer axes.
Coordinates, chemical states and interaction payloads are not read. The result
is detached, preserves canonical string IDs and stored naming declarations,
and retains the existing missing-topology error.

Other targets, contextual selections/reports, naming/extra options, composites
and legacy inputs retain their existing routes. Requested topology schema is
validated; unrequested layer schemas are not completely validated. Static tables
can still load in full. This is an I/O exclusion contract, not a whole-file
validation, physical disk-byte, constant-memory or throughput guarantee. Guard:
`tests/form/file_h5msm/test_topology_v05_probe.py::test_default_topology_conversion_reads_no_other_layer_payload`.

### Force evaluation working estimates

`molecular_mechanics.get_forces` constructs one complete model context, filters
atoms after evaluation and streams supported coordinate sources through
`ChunkedExecutor`. A path to H5MSM 0.5 projects declared chemistry and one model
structure before coordinate iteration; it does not load named analyses or the
complete coordinate series. Multiple/competing structural sources require
explicit alignment first. Native structures must share the reference chemical
state. Other unsupported streaming compositions require a bounded eager read
or fail explicitly.

For `N` source atoms and `S` selected atoms, the numerical estimate reserves
`256*N + 64*S + 4096` bytes per structure, plus 16 bytes per output scalar
for the resident float64 result and its unit-presentation buffer. The block size
is bounded by both this remainder and `configure.chunk_size`; preflight rejects
an output that cannot fit with one work block before constructing a context.
This is not a process-RSS or engine-allocation bound: the model, chemistry,
engine buffers and caller-owned storage have additional costs. There is no
checkpoint/resume, output streaming or disk-backed force-result contract.

### Plane fitting working estimates

`structure.get_least_squares_plane` projects the union of complete selected groups and fills
preallocated dense arrays without accumulating a second list of output blocks.
Native Structures/MolSys and H5MSM support streamed coordinates; eager getter
delivery covers other coordinate-bearing forms. Placeholder iterator classes
do not count as streaming support. Numeric selections on H5MSM 0.5 read only
axis metadata and projected structural series. MolSysMT rich selections use
the scoped static/query route; external selection backends may still materialize
the source through their conversion.

The numerical estimate reserves two output-sized buffers for quantities and
standardization, packed memberships and projections, 24 bytes per projected atom
per frame, 192 bytes per atom in the largest fitted group per frame, and 256
bytes per fitted group per frame, 2,048 bytes for aligned factorization scratch
per frame, plus box work. Rust/Faer computes only right singular vectors;
parallelism is across frames and each worker holds one group. Packed memberships
are borrowed and strided float64 coordinates need no contiguous copy. The native
scratch-size guard checks small and large groups against the working estimate.
Output and a one-frame workspace
must fit before reading. Auto mode streams when the selected full work cannot
fit; off mode fails when its estimated eager work exceeds the budget. The
remaining budget determines a cap applied after chunk optimization. These are
working estimates, not an RSS guarantee or an incremental output writer.

### Ionic preparation and working estimates

The ionic route prepares full-source charge centers once. For index selections
on H5MSM 0.5 it loads topology, chemical states, and association metadata,
without loading structural series or named analyses. Atom axes must have
declared identity links. Structure-assigned chemistry must resolve to one
known state across the requested structures. Only eligible participant atoms
enter the coordinate projection. Rich string selections use the eager route;
unsupported chunked requests fail explicitly.

The keyword-only `heavy_mode` preserves existing positional calls. Besides
the full-source coordinate estimate, `"auto"` checks the selected coordinate
working estimate. Ionic execution reserves one quarter of `max_ram_usage`
for coordinate blocks (a factor of four over selected numeric inputs), one
eighth per candidate search, and one half for sparse accumulation and packing.
An operation-specific chunk cap applies after the shared optimizer.

Candidate searches batch source reference atoms using a conservative
possible-pair workspace bound. Even a geometrically sparse search can be
rejected when that bound cannot fit. Rebuilding neighbor data across batches
can add runtime. Sparse columns accumulate as aligned NumPy arrays per
coordinate block, with a packing factor and explicit axis/membership estimates.
Budget failures return no partial analysis. Empty analyses also account for
their source axes.

These are numeric working estimates, not a process RSS limit. Caller-owned
coordinates, full chemistry tables, Python objects, library caches, and the
runtime are outside the estimates. All output occurrences and final indexes
must fit in memory. Ionic delivery has no incremental writer, checkpoint, or
resume contract. Its `execution_records` retain execution mode, block count and memory
policy independently of scientific parameters. Tests cover eager/chunked parity, scope, source indices, empty frames,
periodic images, H5MSM round trips, and failure integrity. Independent molecular
controls are described in [Interaction Analysis API](interactions_api.md);
dated performance evidence and its limits are in the
[ionic benchmark guide](benchmarking/ionic.md), delivered under `uibcdf/molsysmt#261`.

## Reducer protocol

Every reducer implements `initialize(metadata)`, `consume(chunk)`, and
`finalize()`. The following hooks are optional and must be assessed per reducer:

- `estimate_output_shape(metadata)` for disk-backed output allocation;
- `checkpoint()` and `restore(state)` for resumability;
- `merge(other)` for combining independently accumulated state.

The presence of these methods on the base class does not guarantee support.
Their defaults return no checkpoint or raise `NotImplementedError`. In
particular, the distance reducer cannot restore or merge disk-backed state
across process invocations.

The executor is sequential. `merge()` provides a reducer protocol that a future
parallel orchestrator may use; it does not make `ChunkedExecutor` itself a
parallel trajectory engine.

## Persistent results

`PersistentResultHandle` is a NumPy-memmap-backed array-like result. A temporary
backing file is deleted by `cleanup()`; a caller-provided path remains under
caller control. Disk-backed delivery is operation- and size-dependent. It is not
a general return type for every heavy operation.

If mapping construction fails, the automatically allocated file is retired
before the exception propagates. Caller-provided files are not deleted.
Retirement failures stay visible, including the original construction error
as exception context. See [resource ownership](temporary_resource_operations.md).

Callers receiving a handle must manage its lifecycle explicitly and avoid
calling `to_memory()` unless the complete output fits in RAM.

## Failure integrity

Scientific exceptions must not be converted into silent data loss.
`ChunkedExecutor` is fail-fast: exceptions raised by an iterator, chunk
normalization, or `Reducer.consume()` propagate to the caller. The executor does
not return finalized partial results after such a failure. Corrupt-input
recovery is not currently part of the heavy-execution contract; adding it would
require an explicit policy, exact frame provenance, and alignment tests.

Checkpoint files use Python pickle and are trusted local artifacts, not safe
interchange files. Never restore a checkpoint from an untrusted source.

## Evidence required for a heavy-capability claim

For each operation/form combination, tests must cover:

1. eager versus chunked numerical parity, units, shape, and ordering;
2. non-contiguous `structure_indices` and atom selections;
3. first, final, and partial chunks;
4. relevant PBC behavior;
5. unsupported combinations and explicit failures;
6. cleanup and disk-budget behavior for persistent results;
7. checkpoint/restore or merge only when the reducer implements them;
8. propagation of scientific exceptions without partial-success results.

Framework tests with synthetic reducers demonstrate the protocol but do not
certify every public reducer or input form.

## Extension rule

New heavy operations should reuse `ChunkedExecutor` and `Reducer`, declare the
required form attributes, and add operation-level parity tests. Do not expose a
public `heavy_mode` parameter before the complete eligible and ineligible API
surface is defined and tested.

## Pi-pi detector working estimates

For the H5MSM numeric-index/`all` routes, graph preparation must request chemical
domains without structural arrays or saved analyses. This applies also to
cation-pi, attributed hydrogen bonds, halogen bonds, hydrophobic contacts, metal
coordination and water bridges. Geometry is delivered separately by the projected
executor. A block-count assertion alone does not protect this boundary: regression
tests must reject eager structural reads during preparation. Rich spatial
selections retain their explicitly supported structural context and budget checks.

The experimental pi-pi detector prepares ring chemistry once and uses projected
coordinate/plane blocks with the form's declared heavy route. The complete
accepted Interactions analysis remains resident; source streaming cannot make
an arbitrarily large result fit RAM. It does not construct atom-pair tensors.

One quarter of max_ram_usage covers selected coordinates, plane output and
factorization estimates; bounded candidate search reserves one eighth per
search, and sparse accumulation/packing reserves one half. Per-frame plane
work includes the aligned Rust workspace reserve established by the general
plane tool. Every frame is searched, without first-frame pruning. Numeric
estimates exclude caller-owned source arrays, chemistry tables, Python overhead
and total process RSS. The basis limit is per cyclic aromatic block, not total
system size. An unsupported heavy form fails rather than silently loading it.

For exact workloads and measured tradeoffs, see
[the pi-pi benchmark guide](benchmarking/pi_pi.md). Native block processing does
not reclaim a caller-owned resident trajectory; file projection can avoid that
resident source. Query inverse-index construction and compressed disk bytes
are reported separately from the detector's coordinate work.

## Attributed hydrogen-bond working estimates

`interactions.hbonds.get_hbonds` recognizes full-source candidate sites once using
`interactions.hbonds.get_hbond_sites`, or validates explicit donor-H/acceptor indices. It
projects the union of eligible sites and queries bounded spatial candidates per
frame. Incident scope partitions donor-H rows into selected-role and external-role
searches, so an observation is not duplicated. Between scope requires all three
roles within the disjoint selection union and participation on each side.

Native/H5MSM index selections use the shared projected executor. Rich H5MSM
selections need bounded eager loading; unsupported forced routes fail explicitly.
Coordinate/triplet estimates reserve one quarter of max_ram_usage, candidate work
one eighth per search and resident sparse accumulation/packing one half. The
per-frame estimate includes four coordinate-sized buffers, 256 bytes per candidate
site and 4,096 bytes of scratch. Chemistry, caller-owned arrays, Python overhead
and process RSS are outside these numerical estimates. Output remains resident;
there is no incremental output writer or arbitrary-trajectory memory guarantee.

Method geometry determines coherent periodic triplet images. CPPTRAJ requires
whole donor-H coordinates; DA-based profiles reject inconsistent independent DA
and H-centered MIC observations. These checks are scientific failures, not reasons
to silently switch imaging or discard an otherwise qualifying observation.

## Halogen-bond working estimates

The experimental halogen detector prepares full-source ordered chemical pairs
once through `physchem.get_halogen_bond_sites`. It projects D-X-A-R participants,
uses bounded compiled X-A candidate searches and reconstructs coherent adjacent
MIC vectors before measuring both angles. It never materializes an atom-pair
tensor. Different reference neighbors remain separately identifiable relations.

Coordinate/chain blocks reserve one quarter of max_ram_usage, bounded candidates
one eighth per search and resident sparse accumulation/packing one half. The
per-frame estimate is four coordinate-sized buffers plus 256 bytes per chemical
site, 4,096 bytes of scratch and the periodic matrix reserve. Numeric estimates
exclude full chemical graphs, caller-owned arrays, Python overhead and process
RSS. Match caps, candidate exhaustion and resident-result budgets fail explicitly.
Native and H5MSM index selections use the shared executor; rich file selections
require bounded eager loading and reject forced streaming. Output remains in RAM;
there is no incremental result writer or arbitrary-scale performance guarantee.

## Hydrophobic atom-pair working estimates

Full declared chemistry is recognized once through `physchem.get_hydrophobic_sites`.
Coordinate projection covers typed sites in the actual scope. Internal searches
keep one ordered half of symmetric candidates; incident scope separates selected
internal pairs and selected/external pairs. Between mode searches only the two
disjoint typed sets. Existing compiled candidates perform spatial filtering.
Canonical-pair imaging removes search-orientation dependence of periodic MIC ties.

Coordinate blocks reserve one quarter of configured numeric RAM, bounded candidates
one eighth and resident sparse accumulation/packing one half. Per-frame estimates
reserve four coordinate-sized buffers, 256 bytes per recognized site, 4,096 bytes
of scratch and optional box work. Chemistry, caller-owned arrays, Python overhead
and RSS are outside those estimates. Output remains resident; dense candidate
workloads fail explicitly before unbounded result materialization. Numeric-index
H5MSM/native routes stream through the shared executor; rich file selections need
bounded eager loading or reject forced streaming. No atom-pair tensor, incremental
writer, total-RSS guarantee or newly measured Rust speedup is claimed.

## Metal candidates and water paths

Metal candidates reuse complete chemical site recognition, compiled bounded pair
searches, projected coordinate execution and resident sparse packing. Native/H5MSM
index selections stream coordinates without loading saved analyses. The metal
anchors the MIC image. Chemical graphs and accepted output remain in memory.

One- and two-water paths reuse the hydrogen-bond executor and retain accepted legs
while joining same-frame observations by water oxygen. Per-water candidate fan-out
is batched rather than materialized as a dense pair tensor. Two-water paths join
terminal groups only across observed water-water edges, with the same bounded
fan-out. Exact order limits traversal to two waters; no unrestricted network walk
is performed. Resident leg columns, join arrays and bridge packing have a shared numeric working estimate. Dense
output fails its budget explicitly; process RSS and graph overhead are not fully
modeled. `heavy_mode='force'` selects supported leg coordinate streaming, not an
incremental bridge writer. Public file queries/rendering remain separate work.

## Saving resident interaction analyses

HDF5 serialization of an existing `Interactions` result writes active occurrence
blocks in numeric windows without packing invalidated/recalculated columns.
The writer preserves codec-2 records and images in standalone and named H5MSM
0.5 files. This serializes resident data; it does not add direct detector-to-file
accumulation or resumability. Frame metadata, string tables and other molecular
domains have separate memory costs; the window bound is not a process RSS limit.
Typed dictionaries, pickle and remapping can still materialize all active rows.
See [the interaction contract](interactions_api.md#bounded-hdf5-writing) for the
byte policy and [the H5MSM benchmark guide](benchmarking/h5msm.md) for dated evidence.

## Directed vector geometry

`structure.get_vectors` uses ChunkedExecutor for large coordinate-bearing sources,
including independently aligned structure selections from two sources. The second
projection is bounded by the current first block. Rust computes pair or Cartesian
geometry; explicit pairs never create a dense all-pairs index list. Blocks fill
preallocated resident arrays. Final output, unit-presentation copies, source maps
and numeric block workspace are budgeted before execution. Input streaming does
not imply disk-backed vector output or a complete process-RSS bound.

The [geometry contract](structure_vectors.md) defines first-source-box MIC,
strict center-image validation and unit/axis behavior.
[Measured workloads](benchmarking/vectors.md) distinguish native runtime, public
validation/delivery and process RSS. No GPU, checkpoint or incremental writer
contract is provided by this experimental operation.


## PDBQT indexed input

`PDBQTFileHandler(path, storage_mode='indexed')` retains source-bound byte
ranges and one parsed reference model. File-form StructuresIterator uses this
mode automatically; the principal basic.Iterator is unchanged. Every model is
validated before iteration. Working memory includes index/ID metadata, the
reference/preamble, a current model and requested blocks. It does not retain
every parsed model or a complete source text. Source changes reject queries.

These forms supply coordinate chunks to the existing ChunkedExecutor; center
parity is directly guarded. Per-operation heavy eligibility and scientific pair
semantics remain owned by those operations. The uibcdf/molsysmt#441
guard now covers both distance populations and separate structure axes on
indexed PDBQT input. Explicit full outputs and the known-source pose reader remain
materialized. Use an explicit indexed handler context for deterministic early
exit and metadata reuse. See [PDBQT measurements](benchmarking/pdbqt.md).

## Selected scalar distance reduction

The flat same-system heavy route resolves each endpoint through the shared
`structure._geometry_endpoints` delivery tools, also used by vectors. Aligned
structure axes share a coordinate-union read; differing axes request the second
endpoint only for the current first block. Atom and structure orders, including
repetitions, reach the existing Rust scalar distance kernels. PBC uses the first
endpoint box. No vector tensor is allocated to compute scalar norms.

The output planner uses the selected `(n_structures, n_first, n_second)` axes.
Resident output is preallocated; oversized output uses the executor's existing
persistent handle. Per-block unit scaling precedes writes, so changing the active
length standard does not materialize a full disk result. Work blocks account for
the pair slab as well as projected endpoints, and one slab over budget fails
before the kernel. This is not an atom-tiled kernel or a complete RSS guarantee.
Empty axes retain defined shapes. Centers, explicit pairs and two-system
calculations keep their eager route; no general force-mode support is implied.

`tests/structure/get_distances/test_heavy_endpoints.py` guards literal geometry,
selected output bytes, quantity policy, bounded second reads, PBC, metadata and
indexed PDBQT. Vector behavior remains covered independently after extracting
the shared private delivery tools.

## Prepared protonation removal

`build.assess_protonation` reads inventory, naming and stored chemistry without
copying coordinate trajectories on native `MolSys` and modular H5MSM paths.
Modular assessment reads domain metadata and structure-state associations, not
coordinate or interaction payloads. Other forms may require ordinary conversion;
the operation does not promise universally bounded foreign-form conversion.

The process-local assessment holds detached coverage, positional maps, references
and fingerprints, plus weak source references where possible. Memory scales with
atoms, groups, stored bonds/states and structure-axis metadata, rather than with
the coordinate tensor. It is not a complete RSS limit, portable executable token
or resource authentication mechanism. Changed inventory, naming, chemistry or
axes requires reassessment; coordinate edits on unchanged axes remain valid.

`ProtonationAssessment.apply` rechecks those assumptions and stages an ordinary
complete native subset before in-place publication. Source and candidate can
coexist in memory, including coordinates and analyses. Independent no-ops also
copy data; true native in-place no-ops preserve domains. There is no streaming
publication or automatic interaction recalculation. See
[the preparation contract](structure_preparation_pipeline.md) and
`tests/build/test_protonation_assessment.py` for the actual supported boundaries.


## Bounded pairwise pose geometry

`structure.get_pairwise_rmsd` and `structure.get_distance_clusters` are
experimental bounded-population tools, not out-of-core trajectory matrices.
The RMSD tool reads selected coordinates using projected block delivery and
reuses the Rust positional kernel. It retains the selected coordinate population,
a dense symmetric output and compact oriented mapping witnesses. Chemical map
construction/validation is shared once; identity and inverse closure are required
before a symmetric matrix can be returned. Restricted scopes remain explicit.

Preflight reserves at most half `configure.max_ram_usage` for resident numeric
estimates, leaving room for delivery/kernel blocks. RMSD work is unordered pairs
× selected atoms × admitted maps. Map enumeration remains independently bounded.
The complete/single-linkage primitive implementation uses quadratic numeric
storage and cubic scans; its conservative scan estimate is `N*N*max(0,N-1)`.
Both operations reject work above `max_work` before expensive coordinate delivery
or matrix conversion. These estimates exclude caller/source objects, Python
chemistry and total process RSS; shared-host process-tree caps remain necessary.

Coordinates, chemical assignments and periodic images are not changed. Cutoffs
compare computed float64 nm values inclusively, without hidden tolerance.
Both supplied quantities reach that comparison unit directly; argument validation
does not first convert the cutoff to the session's output units. Output policy
controls returned quantities only. Caller conversions performed before the call
can already have rounded the inputs; no bitwise equivalence across different
conversion histories is promised.
Single linkage can chain distant members. Empty/singleton and repeated structure
populations retain typed shapes and original member positions. No numerical result
asserts chemical identity, coordinate-frame authenticity or biological validity.
See the public pairwise and clustering tutorials and the owning #604 report for
receiving evidence and the independent DockingMT handoff.
