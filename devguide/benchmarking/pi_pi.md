# Pi-pi detector benchmarks

Tracked by uibcdf/molsysmt#265. These measurements cover the experimental
centroid_angle_offset@1 geometric detector, queries and H5MSM 0.5 persistence.
They do not certify energetic interactions, arbitrary aromaticity or viewer RSS.

## Reproducing the controls

Run from the repository root, sequentially and without concurrent tests/builds:

```bash
python devtools/scripts/benchmark_pi_pi_interactions.py --output /tmp/pi_pi_100k_100.json
python devtools/scripts/benchmark_pi_pi_interactions.py --atoms 10000 --structures 1000 --rings 200 --output /tmp/pi_pi_10k_1000.json
```

The first control uses 100,000 atoms, 100 structures and 1,000 six-atom rings.
The second uses 10,000 atoms, 1,000 structures and 200 rings. Each source coordinate
series occupies 240,000,000 numeric bytes. Aromatic atoms form isolated controlled
hexagon pairs; remaining atoms are explicitly nonaromatic. Every fifth frame is
empty, and another frame class removes a third of the contacts. The source has
500/100 possible observed relations and 36,660/73,200 accepted occurrences.
Every count and distance is checked against the prescribed synthetic geometry.
This is a regular sparse scale control, not a real MD ensemble.

Each source/mode combination runs in a separate child process, sequentially.
A tiny independent calculation warms the compiled route. Three full public
calls are timed; preparation, projection, fitting, candidate geometry and sparse
packing are included. Source creation/native loading is excluded from timing,
but included in the process high-water mark. File calculations include metadata
and projected structural reads. OS page-cache state is not controlled.

Raw records retain platform, CPU, Python/library metadata, thread configuration,
base commit, dirty-worktree flag, script/source/extension hashes and every sample:

- [100,000 atoms by 100 structures](../../benchmarks/baselines/pi_pi_100000x100.json)
- [10,000 atoms by 1,000 structures](../../benchmarks/baselines/pi_pi_10000x1000.json)

The editable installed MolSysMT version can lag source development; the recorded
commit and file hashes identify the implementation. The final records include the missing-axis/rich-file diagnostics and the
angular-roundoff cap. Every recorded implementation source hash matches the
published source; the base commit plus dirty-worktree flag records their
pre-commit execution.

## Measured calculation costs

| Source / mode | 100,000 × 100 median | 10,000 × 1,000 median |
| --- | ---: | ---: |
| Native eager | 0.930 s | 1.016 s |
| Native blocks | 1.545 s | 2.858 s |
| H5MSM eager projection | 2.450 s | 3.155 s |
| H5MSM blocks | 3.062 s | 4.393 s |

Forced blocks use 16-frame limits: seven/63 blocks. Eager uses one. Small blocks
cost repeated dispatch and fitting calls; they are not universally faster. The
compiled plane and spatial kernels already support the measured workloads, so
this stage adds no detector-specific Rust rewrite without a localized need.

## Memory and serialization

| Metric | 100,000 × 100 | 10,000 × 1,000 |
| --- | ---: | ---: |
| Result numeric arrays before inverse indexes | 4,330,336 bytes | 6,861,616 bytes |
| After first atom query | 5,475,632 bytes | 7,537,632 bytes |
| Standalone H5MSM interaction layer | 146,896 bytes | 117,715 bytes |
| H5MSM write range across workers | 31–33 ms | 40–42 ms |
| H5MSM read range across workers | 54–65 ms | 41–44 ms |

Disk compression benefits strongly from regular repeated memberships, distances,
evidence and empty frames; these ratios must not be extrapolated to changing
chemistry or uncorrelated geometric measurements. Full coordinate-file size and
system/session saving are not measured by the standalone-layer write timings.

Native workers reach about 954/945 MB process VmHWM in either mode. This includes
materializing the resident source before calculation; forcing blocks does not
reclaim caller-owned coordinates or an earlier loading peak. H5MSM workers reach
519/560 MB with eager projection and 470/451 MB with blocks. VmHWM includes imports,
calculations, indexing, serialization and reload; it is not an allocation delta
or a joint MolSysViewer measurement. Numeric output bytes exclude Python objects,
source arrays and intermediate work. A numerical budget is not a process-RSS cap.

## Query costs

| Query metric | 100,000 × 100 | 10,000 × 1,000 |
| --- | ---: | ---: |
| Visible frame, warmed median | 64–72 µs | 70–78 µs |
| One atom over the trajectory, warmed median | 39–41 µs | 121–128 µs |
| First atom query, including index construction | 5.7–6.2 ms | 2.5–2.8 ms |

Warmed medians use 50 calls per worker. The selected atom participates in a reused
ring relation; these controls do not establish performance for an atom involved
in every changing relation. Each query preserves frame/source axes and evaluated
empty coverage. First-query memory is measured separately from initial result
buffers.

## Limits and next evidence

Coordinates and fitted planes can be streamed, while the entire accepted result
remains resident. Large or dense analyses can exceed the accumulation/packing
budget regardless of block size; tests require an explicit error before partial
finalization. No public incremental writer or checkpoint/resume implementation is
introduced here. No hundred-thousand-atom/ten-thousand-frame coordinate load is
claimed by these controls. Named multi-analysis/viewer loading needs separate
integration measurements.

Molecular geometry correctness is established separately on checksum-fixed
Trp-cage/villin coordinates, with fixed independent aromatic memberships, an
exhaustive covariance-plane oracle, native/file parity and controlled triclinic
image translations. See tests/scientific_truth/curated/test_pi_pi_interactions.py
and devtools/data/pi_pi_validation_systems.json. Those fixtures bound scientific
geometry claims; the synthetic performance control does not replace them.
