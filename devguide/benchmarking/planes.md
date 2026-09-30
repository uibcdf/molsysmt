# Plane fitting

This operational guide records geometric preparation for uibcdf/molsysmt#265.
It does not measure pi-pi detection, energy, aromatic chemistry or disk I/O.

## Reproduction

Run sequentially, without tests or other benchmarks in parallel:

```bash
python devtools/scripts/benchmark_plane_fitting.py \
  --atoms 100000 --planes 1000 --structures 100 --repetitions 3 \
  --output /tmp/plane_fitting.json
```

The resident native Structures source contains 100,000 atoms and 100 structures
(240,000,000 coordinate bytes). We fit 1,000 disjoint planar six-atom groups,
projecting only their 6,000 atoms and 50 nonconsecutive structures in reverse
source order. Remaining atoms are irrelevant background. Known centers, normals
and zero deviations are checked outside timed calls. This is a synthetic
geometry control, not a molecular trajectory or aromaticity validation.

Each mode has one warm-up and three measured public calls. Fixture construction
and import are excluded. Eager mode reads the whole selection; forced streaming
uses eight-frame blocks with advisory-size scaling disabled. The timed call
includes selection, projection, group-wise NumPy SVD and quantity output. No
Rust/Python comparative claim is tested. SVD already executes in NumPy's compiled
numerical library; a Rust wrapper is not assumed to be faster.

## 2026-09-30 checkpoint

Artifact:
[plane_fitting_100000x1000x100.json](../../benchmarks/baselines/plane_fitting_100000x1000x100.json).
Intel Xeon E5-2630 v4 at 2.20 GHz, Linux; Python 3.13.14, NumPy 2.4.6.
Base commit `508dd18b7` with dirty plane changes; source/script hashes identify
the measured implementation. Thread environment and configured budget are
recorded in the JSON with raw samples and process-memory definitions.

The measured function used the review name `get_plane`; the recorded source
files are preserved in commit `1c60460f0`. The public tool is now named
`get_least_squares_plane`, and the reproduction script uses that name. The
snapshot is historical evidence for the measured implementation, not a new
Rust comparison or a rerun of the renamed API.

| Mode | Median seconds | Returned numeric buffers, bytes |
| --- | --- | --- |
| Eager | 0.684 | 3,256,408 |
| Eight-frame blocks | 1.472 | 3,256,408 |

Block traversal adds repeated group-fitting and projection work in this fixture.
The dense result size is unchanged; streaming controls coordinate/work blocks,
not output residency. This does not establish a universal preferred block size,
an upper runtime bound, or performance on a production molecular trajectory.

Returned bytes exclude Python containers, temporary SVD work and resident source.
Linux VmHWM includes imports, source, warm-ups and preceding modes; both rows
share the same process high-water mark. It is not an isolated allocation delta
and cannot prove that streaming lowers total RSS. The harness assumes Linux
`/proc` and CPU affinity. No regression threshold is established by this control.
