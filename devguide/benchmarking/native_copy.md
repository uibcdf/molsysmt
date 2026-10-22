# Resident native-copy benchmarks

**Role:** operational guide for the production-path measurements owned by
[#121](https://github.com/uibcdf/molsysmt/issues/121). The
[implementation record](../archive/resolved_proposals/native_copy_protocol.md) separates
qualified source boundaries, measured limitations and client-adoption follow-ups.

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
are recorded in the [owning proposal](../archive/resolved_proposals/native_copy_protocol.md).
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


## Observables and interaction-heavy profiles

The additional profiles measure the four copy/edit operations only:

```bash
python devtools/scripts/benchmark_native_copy.py --workload mutable_observables \
    --repeats 3 --output /tmp/native-copy-mutable.json
python devtools/scripts/benchmark_native_copy.py --workload many_interactions \
    --repeats 3 --output /tmp/native-copy-many.json
python devtools/scripts/benchmark_native_copy.py --workload many_interactions \
    --warm-atom-index --operation deferred_copy --operation eager_copy \
    --repeats 3 --output /tmp/native-copy-indexed.json
```

`mutable_observables` adds float64 velocities in nm/ps, B factors in nm²,
occupancy and a mutable extension signal with an alias and an owner cycle.
The latter is resident extension data, not a new persistent schema field.
These arrays are copied eagerly in both geometry modes. Reported unique mutable
bytes cover only these named arrays, not every object in the molecular system.

`many_interactions` adds two synthetic typed-column analyses. Each has up to
256 occurrences per evaluated structure, variable counts, empty coverage and a
final unevaluated structure. One catalog is reused; the other cycles through up
to `min(128 * n_structures, n_atoms * (n_atoms - 1))` directed pairs. Only stored
relations/occurrences are allocated. No quadratic atom-pair matrix is created.
The first default case has 640,000 occurrences in each additional analysis.
`--warm-atom-index` builds the atom/relation/occurrence indexes before warm-up,
so copies include independent mutable query caches. Frame checks also warm their
ordinary query state. These are synthetic storage workloads, not scientific
interaction-detector benchmarks.

Every result is checked outside timing against analytical coordinates,
observable values/units, metadata aliases, owners, relation indices,
measurements, coverage and independence. Corrupt observables and deliberately
stale coverage fail the benchmark guards. Editing includes invalidation of all
three named analyses; preparing the independent branch remains outside timing.

### Dated results

The 2026-10-22 Linux/Python 3.14.7 snapshots use three timed samples, one same-shape
warm-up and a separate tracemalloc pass per fresh worker. Numeric thread counts
are one. The JSON records CPU, package versions, base commit, dirty state and
implementation hashes. MB below means decimal MB of traced incremental peak,
not total RSS. No timing threshold or confidence interval is claimed.

| Workload | Atoms × structures | Deferred ms | Eager ms | Deferred peak MB | Eager peak MB |
| --- | --- | ---: | ---: | ---: | ---: |
| Mutable observables | 62 × 5,000 | 10.11 | 14.20 | 14.98 | 22.79 |
| Mutable observables | 10,000 × 1,000 | 93.81 | 249.60 | 401.70 | 641.81 |
| Mutable observables | 100,000 × 100 | 95.63 | 236.74 | 405.88 | 645.90 |
| Many interactions | 62 × 5,000 | 2.35 | 3.78 | 0.12 | 7.92 |
| Many interactions | 10,000 × 1,000 | 19.00 | 166.60 | 0.96 | 240.80 |
| Many interactions | 100,000 × 100 | 9.36 | 159.05 | 8.95 | 245.81 |
| Atom indexes built | 62 × 5,000 | 3.35 | 5.45 | 10.48 | 18.28 |
| Atom indexes built | 10,000 × 1,000 | 19.50 | 164.91 | 6.06 | 246.16 |
| Atom indexes built | 100,000 × 100 | 8.46 | 154.25 | 8.95 | 248.72 |

Source snapshots:
[mutable](../../benchmarks/baselines/native_copy_mutable_20261022.json),
[many interactions](../../benchmarks/baselines/native_copy_many_20261022.json),
[indexed](../../benchmarks/baselines/native_copy_indexed_20261022.json).
The corresponding `*_before_catalogs_20261022.json` snapshots retain the controls
before the immutable-string-tuple optimization. Tool hashes match across each
comparison. A profiling pass identified tuple traversal as the dominant cost;
the 10,000 × 1,000 deferred interaction-heavy median changes from 104.00 to
19.00 ms, and the indexed case from 108.70 to 19.50 ms. This is one local
campaign, not a universal speedup. Repeated elements are exact built-in strings;
string subclasses and mutable tuple members keep their copy protocols.

The remaining approximately 400 MB extra allocation in the large mutable
profile follows the current eager-observable contract. Exploring broader
protected storage is tracked after 1.0 in
[uibcdf/molsysmt#405](https://github.com/uibcdf/molsysmt/issues/405). Atom indexes
also have a real independent-copy cost; immutable occurrence columns do not make
all analysis metadata/caches free. Edit peaks exclude branch preparation and
must not be presented as the total cost of making and editing a molecular copy.

## Source client qualification

```bash
python -m devtools.scripts.qualify_topomt_native_copy \
    --output /tmp/topomt-native-copy.json
```

The [2026-10-22 probe](../../benchmarks/baselines/topomt_native_copy_20261022.json)
executes both `Topography.copy(deep=False)` and `deep=True`, preserving independent
feature registries, native owners, metadata and geometry/coverage edits. It also
checks eager/deferred coordinate storage and parallel observation identity.
The checkout is not modified. TopoMT HEAD is
`c3f72a9177ab8a205b69fefc2963800a2d0b4feb`, clean but one commit ahead and two
behind its fetched origin/main; the four inspected copy/feature files are
identical to that remote reference. This does not qualify the complete remote
application, InputContext recovery, its scientific engines or installed packages.
Reported development version strings can describe an earlier editable build;
the exact source SHA, status, import paths and code hashes identify this probe.
Further owner-local adoption remains in uibcdf/molsyssuite#122 and its linked
client issues. Exact installed-pair release qualification remains in
uibcdf/molsysmt#334.
