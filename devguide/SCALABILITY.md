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

For a path to H5MSM 0.5, executor dimension preflight reads axis metadata.
The file-form iterator projects coordinates, box, time, and structure IDs in
blocks and validates structural-series shapes and units before delivery.
It preserves nonconsecutive and repeated frame indices and requested atom
order, and closes its owned handle on completion or context exit. Other
structural attributes are not supported by this iterator yet. The existing
H5MSM 0.4 file and handler iterators retain their legacy schema route.

This source capability alone does not establish bounded memory for an entire
public operation. Other public preflight calls can still materialize a 0.5
file, and sparse/dense output storage needs its own budget.

### Plane fitting working estimates

`structure.get_least_squares_plane` projects the union of complete selected groups and fills
preallocated dense arrays without accumulating a second list of output blocks.
Native Structures/MolSys and H5MSM support streamed coordinates; eager getter
delivery covers other coordinate-bearing forms. Placeholder iterator classes
do not count as streaming support. Numeric selections on H5MSM 0.5 read only
axis metadata and projected structural series. Rich selections can materialize
the source through ordinary selection.

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
`physchem.get_hbond_sites`, or validates explicit donor-H/acceptor indices. It
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
