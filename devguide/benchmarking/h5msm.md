# H5MSM Performance Benchmarks

**Role:** operational benchmark guide. The executable case compares a private
H5MSM 0.5 selective reader with the public `molsysmt.h5msm.write_layers` and
`read_layers` path. It uses interaction-only files. The public `file:h5msm`
conversion route also reads and writes H5MSM 0.5, but this case does not
benchmark that route or a complete molecular-system file.

## Run the interaction case

From the repository root:

```bash
python benchmarks/h5msm_interactions.py --output /tmp/h5msm-interactions.json
python benchmarks/h5msm_interactions.py --atoms 100000 --structures 10000 \
    --relations 10000 --occurrences 2 --queries 10 \
    --output /tmp/h5msm-interactions-large.json
```

The second command is a scaling experiment. Its construction and full-load
paths hold the synthetic result in memory, so run it only where that fits.
The script creates a temporary interaction-only file, compares selected
coverage, occurrences, relation descriptors, evidence, and distances between
file-backed and loaded queries outside timed regions, and
records raw latency samples in JSON. The generated trajectory contains
evaluated-empty and unevaluated structures, with relations reused across
structures. Repeat runs on the same machine before acting on small timing
differences.

The report separates:

| Field | Meaning |
| --- | --- |
| `storage.write_s`, `file_bytes` | Whole-result write time and HDF5 file size. |
| `storage.first_open_and_query_s` | Opening a file and querying one structure after the write. The filesystem cache may be warm. |
| `storage.full_load_s` | Loading the complete named analysis once. |
| `queries.*.open_file_reader` | Repeated queries through one open HDF5 reader. |
| `queries.*.loaded_memory` | Equivalent queries on a fully loaded result, including `to_dict()` materialization. |
| `storage.loaded_numeric_array_bytes` | Sum of top-level numeric NumPy arrays in the loaded result; excludes Python objects and allocation overhead. |
| `storage.python_tracemalloc_*` | Incremental Python allocation peaks for read paths in the same process; excludes already constructed results, native HDF5 buffers, and filesystem cache. |
| `public_h5msm.first_*` | First public write or read call in the process, including any lazy dispatch and import work. |
| `public_h5msm.warm_*` | Repeated public write or read call in the same process. Filesystem cache state is uncontrolled. |
| `public_h5msm.queries_after_load` | Queries on an analysis loaded by the public `read_layers` API. |

The query cases cover one structure, eight nonconsecutive structures, one
atom restricted to eight structures, and one atom across the entire trajectory.
The current file reader uses frame offsets to select structures and then
filters their relations for an atom. It has no on-disk atom-to-occurrence
posting index. An entire-trajectory atom query therefore still examines
occurrences across the requested trajectory. Keep this distinction visible
when assessing MolSysViewer, TopoMT, or other clients.

The public `read_layers` path loads the selected named analysis in full before
querying. It does not expose the private selective reader. The benchmark
checks selected coverage, occurrences, descriptors, evidence, and distances
for both paths before measuring queries. The first and repeated read times
are measured without `tracemalloc`; a separate traced read reports a Python
allocation peak. Do not compare that peak with process RSS.

## Recorded probe

The [2026-09-29 small-case snapshot](../../benchmarks/baselines/h5msm05_interactions_probe.json)
was run with 1,000 atoms, 1,000 structures, 100 distinct relations, 1,582
occurrences, and 30 requests per ordinary query case. It records the exact commit, dirty checkout state,
Python, NumPy, h5py, CPU, and input parameters. The checkout was dirty and
the temporary storage/cache state was uncontrolled, so these numbers are
local diagnostic evidence, not release targets or portable speed ratios.

| Operation | File reader, median | Loaded result, median |
| --- | ---: | ---: |
| One structure | 0.760 ms | 0.106 ms |
| Eight nonconsecutive structures | 0.896 ms | 0.183 ms |
| One atom in eight structures | 0.981 ms | 0.210 ms |
| One atom in all 1,000 structures | 9.315 ms | 3.674 ms |

The file occupied 60,686 bytes. Loading it took 6.1 ms, and its top-level
numeric arrays occupied 79,080 bytes. For this small dataset, loading once
paid off quickly for repeated queries. A large analysis may reverse the
practical choice because memory pressure and load time grow with the whole
result. Measure the intended atom count, structure count, interaction density,
number of queries, and storage medium before choosing an access path.

The [larger sparse snapshot](../../benchmarks/baselines/h5msm05_interactions_scale_probe.json)
used 100,000 atoms, 10,000 structures, 10,000 possible distinct relations,
and 15,822 occurrences. Its interaction-only file occupied 235,284 bytes;
the loaded top-level arrays occupied 1,833,832 bytes. Median single-frame
queries took 0.800 ms from the open file and 0.151 ms after loading. The
atom-across-trajectory query took 429.861 ms from the file and 36.193 ms
after loading. This synthetic case has no coordinates, and only a subset of
its atom domain participates. It does not represent a full molecular-system
file or establish performance for every interaction density.

## Public H5MSM 0.5 loaded path

The [small public-path snapshot](../../benchmarks/baselines/h5msm05_interactions_public_probe.json)
and [large public-path snapshot](../../benchmarks/baselines/h5msm05_interactions_public_scale_probe.json)
were recorded on 2026-09-29 with the same generator and benchmark command as
the private snapshots. The JSON records the exact commit, dirty worktree,
hardware, dependency versions, inputs, and raw query samples. The small case
has 1,000 atoms, 1,000 structures, and 1,582 occurrences; the large case has
100,000 atoms, 10,000 structures, and 15,822 occurrences. Neither file
contains coordinates or topology.

| Public operation | Small case | Large case |
| --- | ---: | ---: |
| First `write_layers` | 0.365 s | 0.400 s |
| Repeated `write_layers` | 0.008 s | 0.026 s |
| File size | 60,686 B | 235,284 B |
| First `read_layers` | 0.007 s | 0.108 s |
| Repeated `read_layers` | 0.006 s | 0.105 s |
| Loaded top-level NumPy arrays | 79,080 B | 1,833,832 B |
| Traced Python allocation peak for one load | 184,857 B | 5,473,401 B |
| One-frame query after load, median | 0.110 ms | 0.144 ms |
| One atom across all frames after load, median | 4.096 ms | 36.695 ms |

In the large case, the private open-file reader's one-atom query across all
structures took 431.042 ms median. Loading was faster for this sparse fixture
and repeated whole-trajectory atom query; the public path also retains the
complete analysis in memory. The first public write includes a substantial
one-time startup cost in this process. These observations do not establish
cold-storage latency, peak process memory, or performance for a dense analysis.

## Reading and writing efficiently

- Keep one HDF5 reader open across repeated selective queries; reopening the
  file for every request adds startup and metadata work.
- Use explicit structure indices when the client needs a few frames. The
  query index locates those frames without reading every occurrence.
- Load the analysis once if it fits comfortably in memory and the client will
  make many queries. Include the one-time load cost in the comparison. The
  public `read_layers` path currently follows this model.
- For atom queries spanning most frames, benchmark both routes. The private
  file reader lacks an on-disk inverse atom index today.
- Treat file size, NumPy array bytes, Python allocation peaks, and process RSS
  as different measurements. None substitutes for the others.

## Next measurements before stabilizing H5MSM 0.5

The interaction case is a starting point. The acceptance benchmark needs
separate tests for topology, chemical states, structures, and a complete
`MolSys` file; absent and empty layers; 0.4 migration; selected frame and atom
reads; append/edit workflows; file-backed inverse atom lookup; and bounded
block writing/reading at hundreds of thousands of atoms and tens of thousands
of structures. Measure process RSS, native HDF5 cache, and cold storage reads
in isolated processes. Keep semantic parity checks outside each timed region.

The implementation target and acceptance conditions remain in the
[H5MSM 0.5 modular-layer proposal](../pending_proposals/h5msm_0_5_modular_layers.md)
and `uibcdf/molsysmt#252`.
