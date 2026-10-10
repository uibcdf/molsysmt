# Directed vectors

**Role:** operational measurements for uibcdf/molsysmt#375.
**Contract:** [directed molecular geometry](../structure_vectors.md).

Run with the development interpreter after building the native **release** profile:

```bash
cargo build --release --manifest-path rust/Cargo.toml --offline
python benchmarks/get_vectors.py --output /tmp/get_vectors.json
```

The imported extension must contain that optimized build. The receipt records its
SHA-256, separate source/version identity and the Python/Rust input-file hashes.
Editable setuptools builds can select the debug profile; a successful build alone
does not establish an optimized runtime. When updating the local extension, stage
a copy and atomically replace it so an existing process's mapped library is not
overwritten. This is a local development action, not a candidate packaging route.

The runner starts one fresh process per case and checks geometry before emitting
data. Native samples compare 1 and 12 threads; public calls measure argument,
selection, delivery, unit and result work in eager and forced-streaming modes.
The first public eager call includes cold registry work; forced-mode first calls
already follow eager initialization. Warm medians use five kernel or three public
samples. Nonperiodic NumPy subtraction is also recorded as a narrower control,
without public validation, units, maps or PBC. It is not an equivalent public API.

The [2026-10-10 receipt](../../benchmarks/baselines/get_vectors_20261010.json)
uses Linux/Python 3.14 and an optimized source-tree extension. The final measurement ran after the focused tests, without concurrent test
execution. Other host load was not controlled; these are observations rather than thresholds or superiority claims.

| Case | Structures × atoms | Comparisons | Rust, 1 thread | Rust, 12 threads | Public eager | Public streamed |
| --- | --- | --- | --- | --- | --- | --- |
| Explicit pairs | 10 × 100,000 | 1,000,000 | 20.00 ms | 11.54 ms | 64.30 ms | 62.39 ms |
| Cartesian product | 4 × 500 | 1,000,000 | 16.47 ms | 11.44 ms | 24.30 ms | 25.63 ms |
| Periodic dictionary | 10 × 10,000 | 100,000 | 16.20 ms | 5.02 ms | 20.53 ms | 20.17 ms |
| Many structures | 5,000 × 62 | 310,000 | 7.47 ms | 2.51 ms | 21.72 ms | 22.48 ms |

Pair/cartesian vector arrays each contain 24 MB; periodic dictionary numeric
arrays contain 6.8 MB, and the many-structure vector array contains 7.44 MB.
Metadata and presentation buffers are additional. Process peak RSS in the raw
receipt includes imports, inputs, retained independent NumPy controls and outputs;
it cannot be interpreted as interaction/vector storage cost alone. These cases
compare execution modes, not a tightly enforced large-trajectory RSS limit.

The measurements justify compiled loops and show that endpoint delivery still
has appreciable cost. They do not show Rust always beating bare NumPy subtraction.
No future acceptor-direction model, chemistry recognition, disk I/O or installed
release artifact is qualified by this benchmark.
