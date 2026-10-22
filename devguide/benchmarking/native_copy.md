# Resident native-copy benchmarks

**Role:** operational guide for the production-path measurements owned by
[#121](https://github.com/uibcdf/molsysmt/issues/121). The
[active design record](../pending_proposals/native_copy_protocol.md) separates
implemented ownership guarantees from unresolved mutation and table policies.

## Reproducing the campaign

From the repository root, in the existing development environment:

```bash
python devtools/scripts/benchmark_native_copy.py --repeats 3 \
    --output /tmp/native-copy-resident.json
```

The default cases are 62 atoms × 5,000 structures, 10,000 × 1,000 and
100,000 × 100. The latter two hold 240,000,000 coordinate bytes each before
box, topology, chemistry, analysis and object overhead. Several allocations
can coexist during eager copying, reads, validation and file loading. These
are resident-memory benchmarks; do not extrapolate them to a trajectory that
does not fit in RAM.

For a bounded investigation, select cases and operations explicitly:

```bash
python devtools/scripts/benchmark_native_copy.py --case 10000x128 \
    --operation deferred_copy --operation eager_copy --operation edit_one_atom \
    --repeats 5 --output /tmp/native-copy-edits.json
```

Run cases sequentially without competing benchmarks. The tool launches one
fresh worker per case/operation and fixes OMP, OpenBLAS, MKL and Rayon thread
environment variables to one. Each worker performs one same-shape warm-up,
then independent timed samples, then a separate allocation-tracing pass.
Public validation remains enabled. All temporary H5MSM files use managed
directories cleaned on normal completion or Python exceptions.

## What the operations include

| Operation | Measured boundary |
| --- | --- |
| `deferred_copy` | Validated `MolSys.copy(deep=False)`, including eager canonical-table and metadata copies. |
| `eager_copy` | Validated `MolSys.copy()`, additionally allocating independent coordinate/box bytes. |
| `edit_one_atom` | `msm.set` for atom 0 in the middle structure of a fresh deferred branch, including owner invalidation. Branch creation is outside timing. |
| `edit_eight_structures` | One `msm.set` call for atom 0 in up to eight consecutive structures of a fresh deferred branch. |
| `selected_read` | Native `Structures.get` for two atoms and four explicitly ordered structure indices, including a repetition. |
| `full_read` | Full resident coordinate property, including concatenation when multiple blocks exist. |
| `iterate_coordinates` | Public `msm.Iterator` over all coordinates plus a checksum reduction, bounded by the requested chunk size. |
| `rust_distances` | Public all-structure distance calculation between two atoms without PBC, including validation and coordinate preparation. |
| `h5msm_write` | Public complete-system H5MSM 0.5 conversion from the original resident source. |
| `h5msm_read` | Public complete-system resident load while the original source remains alive. The file is prepared before timing. |

Each sample is checked outside timing against analytical coordinates or
distances, owner bindings, chemical-state authority, evaluated coverage,
parallel occurrence identities and producer provenance. Edits must leave the
original unchanged and invalidate only the requested structures of the branch.
The small test suite deliberately supplies stale coverage and wrong coordinates
to ensure that invalid outputs do not qualify as fast results.

The fixture has deterministic linear float64 coordinates in nm, a box and time
series, a canonical atom inventory and one chemical state with formal charges.
One named sparse analysis has two parallel observations every third evaluated
structure, evaluated-empty structures and a final unevaluated structure.
It has no velocities, large mutable metadata, dense interaction inventory or
representative protein/ligand chemistry. In particular, its HDF5 compressibility
does not establish file size or throughput for arbitrary molecular data.

## Reading memory and timing evidence

- `median_seconds` summarizes untraced samples; raw timings are retained.
  Imports and fixture construction are excluded, as is branch preparation for
  the edit operations. These are warm-call measurements, not startup latency.
- `traced_operation_peak_bytes` is a separate incremental `tracemalloc` peak.
  It includes allocations registered with Python's allocator tracing, including
  NumPy's registered buffers, but is not total process RAM or all native HDF5
  allocations.
- `rss_before_bytes` and `rss_retained_bytes` are Linux address-space counters
  around each timed operation with its result still alive. They are unavailable
  rather than zero on unsupported systems. Their difference is not a sampled
  operation peak and can reflect allocator reuse.
- `process_hwm_bytes` includes imports, fixture construction, warm-up and earlier
  samples in that worker. A high-water increase does not isolate all temporary
  allocations of the operation. `rss_after_releasing_result_bytes` may retain
  allocator arenas even after objects are collected.
- `source_and_result_unique_geometry_bytes` counts unique immutable coordinate
  and box backing bytes across those two systems. It excludes Python headers,
  topology/chemistry tables, other series, analyses and allocator overhead.
  Use it to quantify geometry sharing, not as a claim of total RAM usage.
- File size includes the complete saved system. Cache state is warm or
  uncontrolled, and the writer timing does not promise `fsync` durability.

The JSON records the base source commit, dirty-worktree state, relevant source
and tool SHA-256 hashes, timestamp, hardware, interpreter and package versions.
A development snapshot with local tool changes is evidence for those recorded
bytes, not an installed release or another platform. No timing threshold is a
test gate, and these measurements alone do not establish an optimal block size,
general table copy-on-write, direct-domain owner notification or client adoption.

## Recorded production checkpoint

The [2026-10-21 snapshot](../../benchmarks/baselines/native_copy_resident_20261021.json)
contains the three default cases. Its interpretation and remaining decisions
are recorded in the [owning proposal](../pending_proposals/native_copy_protocol.md).
The older `native_copy_20261021.json` and `native_copy_reads_20261021.json`
measure experimental layouts in `study_native_copy.py`; they are not production
native-path measurements and must not be substituted for this campaign.

## Comparing HDF5 coordinate chunks

The layout study keeps the coordinate payload and native transfer blocks fixed
and changes only the initial HDF5 coordinate dataset's physical chunks:

```bash
python -m devtools.scripts.study_h5msm_structure_chunks \
    --output /tmp/h5msm-structure-chunks.json
python -m devtools.scripts.study_h5msm_structure_chunks \
    --case 10000x1000 --case 100000x100 --layout auto \
    --layout aligned_256k --repeats 2 --output /tmp/h5msm-structure-chunks-large.json
```

The default bounded cases are 62 × 512, 10,000 × 128 and 100,000 × 16.
The [bounded snapshot](../../benchmarks/baselines/h5msm_structure_chunks_20261021.json)
compares automatic HDF5 chunks with 64 KiB, 256 KiB and 1 MiB candidates.
The study explicitly forces its `auto` control even after a runtime layout
change. Other candidates keep xyz together, cap uncompressed chunk bytes and
choose a temporal extent dividing both resident block size and the codec's
256-row transfer limit. It patches dataset creation only in an isolated study
worker. It does not modify the original file, runtime configuration or schema.

Each case/layout has an independent worker, same-shape warm-up, untraced timing
samples and separate allocation tracing. Public write/load include the complete
synthetic system. Two additional reads open a fresh HDF5 handle and use the
**private structures codec**: one complete structure, or two atoms in four
explicitly ordered/nonconsecutive/repeated structures. These are not public
selective-file APIs. Opening each handle resets its HDF5 raw chunk cache;
the OS cache is warm/uncontrolled. Values, shapes, units, owner bindings,
provenance and coverage are checked outside timing as applicable.

Compare file size, public write/load and both selected reads together. A layout
with faster bulk transfer may worsen sparse reads, and smaller compressed
chunks can increase file overhead. The linear fixture's compressibility is not
a universal molecular-data model. A chosen runtime budget remains an internal
policy, not a user-visible chunk-shape guarantee or a proven global optimum.
Append retains an existing dataset's layout; its first/last writes can be
partial chunks when the old structure count is not chunk-aligned.

The [larger controlled snapshot](../../benchmarks/baselines/h5msm_structure_chunks_large_20261021.json)
compares automatic layout with 256 KiB on both 240 MB coordinate cases. The
runtime adopts that provisional compromise for new coordinate datasets; the
normative [geometry I/O contract](../h5msm_format.md#resident-geometry-io) defines
its scope. The 64 KiB alternative remains relevant if sparse-file queries
dominate a future workload; 1 MiB worsened the two-atom query in the bounded
100,000-atom case. Do not select a layout from bulk timings alone.

After adoption, repeat the unmodified public production paths:

```bash
python devtools/scripts/benchmark_native_copy.py --operation h5msm_write \
    --operation h5msm_read --repeats 2 --output /tmp/native-copy-h5msm-refined.json
```

The [refined production snapshot](../../benchmarks/baselines/native_copy_h5msm_refined_20261021.json)
uses the runtime default, without a dataset-creation patch. It records writes
of 5.243/5.742 s and resident loads of 0.951/1.532 s for the two 240 MB cases.
The traced incremental load peaks are 242.582/259.747 MB, compared with the
original 482.608/501.228 MB before eliminating the second native snapshot.
Those peaks are not total process RSS; full resident data still needs RAM.
