# Comparable advisory benchmark sessions

This is the supported competitive-session evidence contract from #567, including
#673's common-observable correction and #676's worker lifecycle. It is a developer
tool contract, not a new molecular API or a performance admission requirement.
The [advisory policy](performance_policy.md) remains authoritative: correct tools
stay available and confirmed inefficiency is improvement-issue evidence.

## What is compared

`benchmarks/competitors/run_matrix.py` prepares the actual data and checks all
coordinate values, source selections and geometric observables before timing.
The three families cover:

- complete DCD coordinate reading against its H5 reference, normalized explicitly
  to nm and `(n_structures, n_atoms, 3)`;
- equal ordered source atom indices for the stated queries;
- unweighted centroids, RMSD **without** superposition and full nonperiodic pair
  grids. MDTraj distances execute `compute_distances`, not an operation from
  another package carrying its label.

External payloads and precision differ: a trajectory, an AtomGroup, an array and
a quantity do not have identical construction costs. The route records its actual
provider, call, input precision and output kind. Equality of normalized values
is not equality of all APIs. Cross-session comparison matches a path to the same
path; the printed cross-provider table does not establish a fair speed ranking
without reviewing these semantic and overhead differences. Legacy `jit` keys
identify today's Rust compatibility exports; the displayed label is Rust.

The runner uses an explicit serial CPU/double-precision native policy and the
complete shared MolSysMT unit policy through scoped contexts. External float32
inputs remain declared. Caller policies are restored. No second standard-unit
catalog is maintained in the benchmark.

A newly generated, benchmark-owned reference PDB has only its two volatile
writer-provenance records normalized deterministically. The original records,
raw/prepared hashes, input H5 hash and actual producer version remain in the
session. All scientific records are byte-preserved. Existing input files are
never normalized; an unfamiliar generated provenance layout requires review.
This prevents a clock change alone from making otherwise equal workloads
incomparable without relaxing scientific-input identity.

## Required evidence

The session retains clean product commit/dirty-state information, its native
backend hash and a `comparison_context` with schema
`molsysmt.benchmark-context@1`:

| Boundary | Required facts |
| --- | --- |
| Runtime/hardware | Python implementation/version, OS/kernel, architecture, CPU model, affinity/logical CPU counts and physical memory |
| Resource policy | Effective cgroup CPU/memory/swap limits, including ancestors, and explicit positive numeric thread settings |
| Providers | Versions, actual initializer hashes and origin correspondence, plus a clean explicitly editable Git root or installed RECORD identity |
| Environment | Retained normalized Conda package/build records, or distribution records outside Conda, and their digest; the product under comparison is excluded |
| Configuration | Native CPU/precision/execution policy and explicit unit form/parser/standards |

Before/after host load, memory availability, swap counters and pressure are separate
observations, not fields that must be numerically identical between runs. They
are not resource reservations. Matching metadata is necessary evidence, not
proof of equal contention, frequency, virtualization or causal attribution.
The current qualified route is Linux with readable cgroup-v2 facts; unknown
facts on another runtime remain unevaluable rather than silently equivalent.

Each result has a `molsysmt.benchmark-workload@1` description: actual file hashes,
atom/structure dimensions, prepared array/selection identity, observable, units,
PBC/reference rules, precision, route and benchmark-producer hash. Its timing
record includes actual raw repeat-block means (at least three for comparison),
iterations/repeats, a matching median and the measurement implementation hash.
The warm-up count, timer, GC disposition and worker process model are explicit.
An isolated process high-water RSS is not an allocation attribution or a complete
pipeline memory bound. Startup/preparation, including imports and validation,
remain outside the steady-state timed samples.

## Workers and failures

Competitive cases use importable factories and serializable paths/scalar policy.
Each fresh `spawn` worker constructs its own objects, verifies its prepared
workload against the parent declaration, warms once and measures. Molecular
objects, live registries and locks are never pickled from the parent. The
parent's global multiprocessing start method is unchanged. Python documents
[the inherited-state limitations of fork and the spawn model](https://docs.python.org/3.14/library/multiprocessing.html#contexts-and-start-methods).

All workers have a finite wall-clock budget (120 seconds by default), return
through IPC before the parent joins them, and clean up only their own process.
A failed or expired worker produces no zero timing or completed session. The
old arbitrary-closure/fork route remains explicitly legacy and bounded; its
completion after arbitrary native/threaded parent preparation is not certified.
New competitive cases must use factories. This is not qualification of every
historical macro or operating system.

## Running and interpreting the audit

Set the six thread variables declared in the performance workflow explicitly
(`OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`, `RAYON_NUM_THREADS`,
`OPENMM_CPU_THREADS`, `NUMEXPR_NUM_THREADS`); the controlled protocol uses one.
Use the host's allocated/capped execution route and check available resources
before a campaign. The harness itself does not reserve machine resources.

Write a prospective session separately from the committed baseline:

```bash
python benchmarks/competitors/run_matrix.py --output .pytest_cache/benchmarks/current_session.json
python benchmarks/compare_runs.py --baseline benchmarks/baselines/competitor_matrix_session.json --current .pytest_cache/benchmarks/current_session.json --threshold 0.15 --report .pytest_cache/benchmarks/comparison.json
```

`molsysmt.benchmark-comparison@1` records input digests, reasons, matched numeric
observations, raw samples, provider identity, unreferenced paths and disposition:

| Disposition | Native exit | Meaning |
| --- | --- | --- |
| `observed_within_threshold` | 0 | Complete matching recorded protocol; no median warning |
| `warning` | 0 | Matching protocol and a median slowdown above 15%; correct tools stay available |
| `partial` | 1 | Matched observations exist, but new paths lack reference measurements |
| `unevaluable` | 1 | Missing, malformed or incompatible evidence; no performance approval |

A warning also reports whether the observed sample ranges separate beyond the
threshold. This is not a confidence interval, a correction for shared-host load,
or automatic causal attribution. Confirm repeated, representative product
inefficiency before filing/updating its improvement issue. A direct external
control slowdown is not by itself a MolSysMT defect. No issue is filed or public
function disabled automatically.

The workflow remains advisory while retaining native producer/comparison failures,
JSON reports and logs after success or failure. Invalid results do not become a
scientific pass because the timing job is nonblocking. Input/report destinations
must be distinct; atomic report replacement cannot truncate the reference.

## Historical references and renewal

The committed September reference predates this protocol. It is retained exactly
and is explicitly unevaluable for new automatic comparisons. Earlier failed
campaigns stay failed; no new source result retroactively certifies their ratios.

Renewal is a separately reviewed maintainer action: choose a clean source/backend
and compatible recorded environment, run the unchanged admitted workloads with
full numeric checks and retained repetitions/resource observations, review
precision/payload/warm-up/noise limitations, and retain the raw candidate and
its digest before selecting it as reference. Record the reason, old/new source
and artifact identities and acceptance; never overwrite a baseline during the
current measurement. Synchronize documentation copies only after that review.
No replacement reference or speed claim is produced by the tiny transport tests.
