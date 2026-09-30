# Ionic Calculation Benchmarks

**Role:** operational guide. The measurements are dated checkpoints, not
machine-independent performance guarantees. Scientific method and support
limits are normative in [Interaction Analysis API](../interactions_api.md)
and [Scalability](../SCALABILITY.md).

## Reproducing the molecular controls

Run from the repository root on Linux, sequentially without other benchmark
or test workloads. RDKit is required for fixture preparation:

```bash
python devtools/scripts/benchmark_ionic_interactions.py --dataset trp_cage --repeats 3 --chunk 5 --output /tmp/ionic_real_trp_cage.json
python devtools/scripts/benchmark_ionic_interactions.py --dataset trp_cage --cycles 100 --repeats 3 --chunk 64 --output /tmp/ionic_real_trp_cage_repeated.json
python devtools/scripts/benchmark_ionic_interactions.py --dataset villin --threshold .8 --repeats 3 --chunk 5 --output /tmp/ionic_real_villin.json
```

The fixed manifest `devtools/data/ionic_validation_systems.json` records PDB
hashes, explicit state charges, whole-center membership, reference atoms, and
axis dimensions. Coordinates remain unchanged. The selected state charges
N-termini, Lys and Arg and deprotonates Asp/Glu and C-termini; other atoms
have zero formal charge. This is a declared modeling state, not evidence of
experimental protonation. No state rule is added to production code.

Trp-cage uses 304 atoms and all 38 bundled NMR models. The 3,800-frame case
repeats those 38 models 100 times; it measures scaling at a realistic molecular
geometry and retains only 38 independent structures. Villin uses 596 atoms
and one bundled model. The 0.8 nm villin threshold exercises nonempty output;
it is an explicit control parameter, not a recommended salt-bridge cutoff.

The independent Cartesian oracle enumerates declared positive/negative
reference atoms without calling MolSysMT centers, neighbors, or geometry.
Each molecular worker verifies all observation keys, counts, and distances
outside the timed region. Contract/scientific tests additionally check
RDKit SMARTS membership, selected frames/scopes, empty coverage, controlled
triclinic image reconstruction, and named public H5MSM round trips.

## 2026-09-30 checkpoint

Intel Xeon E5-2630 v4, 2.20 GHz, Linux x86_64; Python 3.13.14, NumPy 2.4.6,
h5py 3.16.0, RDKit 2025.9.5. Source base `0a46e4ca3` with dirty
validation/tooling changes, recorded hashes of detector, reducer, fixture
helper, manifest, and benchmark. Package labels are not source revisions.
Each sequential worker warms compiled geometry on an independent two-atom
fixture and repeats calculation three times. The table reports medians.
OS page cache, host activity, and CPU frequency are uncontrolled.

| System | Source | Mode / blocks | Calculation median (ms) | Occurrences | Worker peak RSS (MiB) |
| --- | --- | --- | --- | --- | --- |
| trp_cage, 38 frames | native | off / 1 | 26.6 | 20 | 429.2 |
| trp_cage, 38 frames | native | force / 8 | 29.4 | 20 | 429.1 |
| trp_cage, 38 frames | file | off / 1 | 114.1 | 20 | 428.5 |
| trp_cage, 38 frames | file | force / 8 | 123.2 | 20 | 428.4 |
| trp_cage, 3,800 frames | native | off / 1 | 1239.1 | 2,000 | 486.7 |
| trp_cage, 3,800 frames | native | force / 60 | 1269.1 | 2,000 | 486.3 |
| trp_cage, 3,800 frames | file | off / 1 | 1923.8 | 2,000 | 456.4 |
| trp_cage, 3,800 frames | file | force / 60 | 2054.1 | 2,000 | 454.8 |
| villin, 1 frames | native | off / 1 | 19.6 | 4 | 428.2 |
| villin, 1 frames | native | force / 1 | 19.6 | 4 | 428.2 |
| villin, 1 frames | file | off / 1 | 106.4 | 4 | 428.3 |
| villin, 1 frames | file | force / 1 | 105.2 | 4 | 427.8 |

Native calculation time excludes the separately recorded source load.
File calculation time includes projected chemistry preparation and structural
reads. Worker peak RSS is Linux VmHWM since exec, through loading, calculation,
indexing, persistence and independent validation. It includes the runtime and
is not calculation-only allocation attribution. Rusage peak is recorded
separately because it can inherit a pre-exec parent high-water mark. Parent
fixture construction and combined parent/worker memory are not measured.

| File/chunked case | Numeric result including indexes (bytes) | Frame / warm atom query (µs) | H5MSM layer size (bytes) | Write / read (ms) |
| --- | --- | --- | --- | --- |
| trp_cage, 38 frames | 7,232 | 71.6 / 33.6 | 59,688 | 9.0 / 6.1 |
| trp_cage, 3,800 frames | 186,224 | 85.9 / 47.4 | 72,853 | 11.2 / 7.4 |
| villin, 1 frames | 10,656 | 78.2 / 37.3 | 59,688 | 9.2 / 6.3 |

Queries are medians of 50 warm calls. First atom-query index construction is
reported separately in JSON. Numeric byte counts omit Python overhead.
Persistence uses public interaction-only `write_layers`/`read_layers`; source
coordinates are not part of these file-size or write/read measurements.

## Choosing an execution route

- For small in-memory ensembles, eager execution avoids block orchestration.
  Trp-cage takes about 27 ms eager versus 29 ms in eight native blocks here.
- For a few models from a file, chemistry preparation can dominate geometry.
  Reading chemistry takes roughly 75–82 ms in these controls. Recognizing
  centers takes about 9 ms in Trp-cage and 13 ms in villin.
- In the repeated 3,800-frame case, neighbor search takes about 0.75 s and
  grouped geometry about 1.15–1.20 s. Packing takes only about 2.4 ms.
  Optimizing packing would not remove the dominant per-frame geometry cost.
- File streaming projects eligible atoms and controls temporary coordinates;
  it does not make the complete sparse result disk-backed or impose an RSS cap.
- Very small blocks can add I/O and call overhead. Choose a block size after
  measuring your chemistry, eligible participants, frames, and output density.

Stage timers are inclusive: consume includes grouped geometry, and grouped
geometry includes neighbors. Derived differences between stage medians are
estimates, not independent additive samples. No latency acceptance threshold
or broad biological classification claim is inferred from these cases.

## Raw results

- [Trp-cage, 38 independent models](../../benchmarks/baselines/ionic_real_trp_cage.json).
- [Trp-cage, 100 repeated cycles](../../benchmarks/baselines/ionic_real_trp_cage_repeated.json).
- [Villin HP35, one model](../../benchmarks/baselines/ionic_real_villin.json).

Earlier synthetic scale controls use 1,000 × 300 and 10,000 × 30 fully charged
atoms/frames, and 100,000 × 100 with only 100 charged atoms. They measure
different candidate densities and isolate source size from eligibility:

- [1,000 × 300](../../benchmarks/baselines/ionic_1000x300.json).
- [10,000 × 30](../../benchmarks/baselines/ionic_10000x30.json).
- [100,000 × 100, dilute charges](../../benchmarks/baselines/ionic_100000x100_dilute.json).

Those snapshots predate molecular fixture support in the script. Their stored
source/hash records remain historical; rerunning the documented dimensions
with a newer script produces a new checkpoint. None establishes behavior for
100,000 charged atoms across 10,000 frames. Expanded motif recognition remains
tracked by `uibcdf/molsysmt#262`. Additional force-field energy methods and
incremental result storage require independent scientific/design decisions.
