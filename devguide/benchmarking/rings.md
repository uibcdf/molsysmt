# Ring participant preparation

This operational guide describes the chemical preparation benchmark supporting
uibcdf/molsysmt#265. It measures two experimental reusable tools, not a pi-pi
detector, trajectory calculation, energy model, or file-format benchmark.

## Reproduction

Run from the repository root, without tests or other benchmarks in parallel:

```bash
python devtools/scripts/benchmark_ring_participants.py \
  --atoms 100000 --rings 1000 --repetitions 3 \
  --output /tmp/ring_participants.json
```

The synthetic source has 100,000 atoms: 1,000 disjoint six-atom covalent cycles
with explicitly aromatic flags, plus a 94,000-atom acyclic chain. Connectivity
is declared complete. No molecular aromaticity inference is being validated.
Analytical memberships and offsets are checked outside each timed call. Source
construction and import are excluded from timings. Each tool has one complete
warm-up followed by three measured public calls, run sequentially in one process.

The JSON records raw samples, median, host/CPU, Python/library versions, thread
environment, memory size, source/script hashes, base commit and dirty flag.
No file I/O is timed. The harness assumes Linux `/proc` and CPU affinity APIs.

## 2026-09-30 checkpoint

Recorded artifact:
[ring_participants_100000x1000.json](../../benchmarks/baselines/ring_participants_100000x1000.json).
Intel Xeon E5-2630 v4 at 2.20 GHz, Linux x86_64; Python 3.13.14, NumPy 2.4.6,
pandas 2.3.3 and NetworkX 3.6.1. Base commit `9acf67517` with dirty ring changes;
the artifact's source and script hashes identify the measured code precisely.

| Tool | Median seconds | Membership buffers, bytes | All returned NumPy buffers, bytes |
| --- | --- | --- | --- |
| get_rings | 1.486 | 56,008 | 2,456,008 |
| get_aromatic_rings | 0.635 | 56,008 | 2,456,008 |

Both tools return 1,000 memberships without a dense atom-by-atom matrix.
The small membership buffers do not measure total process memory. Returned axis
arrays account for most result bytes in this fixture. Python dictionaries,
NetworkX workspace, source tables and imports are excluded from numeric totals.
Linux VmHWM is also recorded, but includes the process since startup, source,
warm-up, and preceding tool; it is not an isolated allocation delta. The second
tool's high-water mark must not be compared as its own peak increment.

## Interpretation and limits

Cyclic biconnected blocks avoid treating the full chain as a minimum-basis
subproblem. The aromatic tool additionally omits all nonaromatic edges. These
are measured graph-preparation routes for one sparse control, not proof that
NetworkX outperforms Rust, RDKit or every other ring algorithm.

The explicit cyclic-block size guard bounds an individual basis problem. It
does not bound total graph memory or time. Dense, highly fused or tied graph
families, atom permutations, alternative aromatic definitions, geometric plane
fitting, neighbor searches, pi-pi measurements, trajectory memory and persistence
still need evidence appropriate to those contracts. Pi-pi detector benchmarks
remain pending in #265. No performance regression threshold is established here.
