# Plane fitting

This operational guide records geometric preparation for uibcdf/molsysmt#265.
It does not measure pi-pi detection, energy, aromatic chemistry or disk I/O.

## Public-call reproduction

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
includes selection, projection, fitting and quantity output. The historical
checkpoint below used group-wise NumPy SVD. The current script uses the bundled
Rust/Faer kernel and records its source and extension hashes. Numeric-kernel
comparisons have a separate harness and are not inferred from this public call.

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

## Kernel comparison — 2026-09-30

```bash
python devtools/scripts/benchmark_plane_kernels.py \
  --repetitions 5 --output /tmp/plane_kernel_comparison.json
```

Artifact:
[plane_kernel_comparison_20260930.json](../../benchmarks/baselines/plane_kernel_comparison_20260930.json).
The same Xeon E5-2630 v4/Linux host uses Python 3.13.14, NumPy 2.4.6 and
Rust 1.97.1, with the locked Faer 0.24.4. The artifact records git base, dirty
status, source/script/extension hashes, BLAS configuration and raw samples.
MolSysMT's version string is the editable installation metadata; git and hashes
identify the actual measured source.

Every case/candidate runs in a fresh sequential subprocess. One complete warm-up
is discarded; medians summarize five timed numeric calls. NumPy BLAS threads
are fixed to one; Rust uses one or four Rayon threads across frames. The rotated
and warped synthetic groups are seeded; validation compares all length columns
with the frozen NumPy control and compares normals without orientation after
timing and the memory snapshot. No selection, units, PBC or I/O is timed here.
Separate analytical and independent-oracle tests establish geometric truth.

The NumPy batch control groups equal-length participants and tiles its work under
an 8 MiB numerical estimate. A single group/frame is the lower bound of a tile;
that floor can exceed the advisory estimate for a sufficiently large group.
The frozen NumPy controls are benchmark code, not runtime fallbacks.

| Workload | Structures | Groups (atoms per group) | NumPy grouped, ms | NumPy batched, ms | Rust 1 thread, ms | Rust 4 threads, ms |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| One plane | 1 | 1 (6) | 0.234 | 0.384 | 0.014 | 0.025 |
| Many groups | 1 | 1,000 (6) | 161.278 | 8.893 | 4.070 | 3.577 |
| Many structures | 5,000 | 1 (6) | 33.427 | 37.329 | 18.487 | 5.792 |
| Groups and structures | 50 | 1,000 (6) | 507.738 | 309.934 | 149.641 | 46.494 |
| Ragged groups | 20 | 240 (3, 6, 12, 128) | 88.602 | 51.227 | 26.377 | 9.659 |
| Large cloud | 8 | 1 (10,000) | 14.591 | 15.656 | 6.552 | 2.901 |

**Decision:** use packed Rust/Faer SVD in production. The single-thread Rust
candidate is faster than both controls in every measured workload, and frame
parallelism helps the multi-frame workloads. Four threads do not parallelize
1,000 groups in a single structure; differences there are run variability.
The public adapter follows the existing session parallel policy rather than
unconditionally creating four-way work.

Linux process high-water marks include imports, the fixture and warm-up. They
are captured before allocating the reference and are not allocation deltas.
For 50 structures and 1,000 groups, peaks were approximately 84.9 MiB for grouped
NumPy, 94.5 MiB for batched NumPy, and 86.0/86.5 MiB for Rust 1/4 threads. Rust
therefore does not lower total RSS in every case. It avoids unused left vectors,
borrows packed memberships and keeps one factorization workspace per worker.
Dense returned buffers have identical sizes for all candidates.

### Accuracy refutation and memory checks

The first Rust/Nalgebra prototype failed the rotated warped hexagon: its maximum
deviation was `0.004995746467550156 nm` versus `0.004995746494075226 nm` from
NumPy and an independent covariance oracle. Normal components differed by up to
`1.36e-10`. RMS agreement alone had hidden the right-vector error. That prototype
was rejected without loosening tolerances; the shipped Faer candidate passes the
component and maximum-deviation regression. Production never forms covariance.

The factorization-scratch guard found that three atoms need 1,600 numeric bytes
including padded matrices and scratch, beyond the prior estimate. The public
budget now reserves an additional 2,048 bytes per frame; a Rust test checks the
matrix padding and actual scratch requirements for groups from 3 to 10,000 atoms.
Tests also cover scale extremes, thin planes, ragged/overlapping groups, source
nonmutation, malformed packed arrays, empty axes, thread determinism, strided
coordinate borrowing and the unit/PBC public routes. These buffer estimates do
not bound thread stacks, allocator metadata or whole-process RSS.

## Integrated public call — 2026-09-30

Artifact:
[plane_fitting_rust_20260930.json](../../benchmarks/baselines/plane_fitting_rust_20260930.json).
The public-call workload and methodology are those stated above: 100,000 source
atoms, 100 source structures, 1,000 selected six-atom groups and 50 nonconsecutive
selected structures. The active auto thread policy and its thresholds are
recorded. Small eight-frame blocks can fall below the parallel threshold.

| Mode | Median seconds | Returned numeric buffers, bytes |
| --- | ---: | ---: |
| Eager | 0.074 | 3,256,408 |
| Eight-frame blocks | 0.176 | 3,256,408 |

The historical NumPy snapshot was 0.684/1.472 seconds; these are separate dated
runs, not a simultaneous public A/B experiment. The controlled numeric comparison
supports the kernel choice, while the integrated run demonstrates the current
public cost. No universal speedup, trajectory-detection throughput or isolated
public-mode RSS reduction follows from these measurements. Pi-pi detection,
chemistry and disk I/O remain outside the benchmark.
