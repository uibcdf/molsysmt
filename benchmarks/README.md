# Coordinate Path Baseline

This directory stores lightweight benchmark scripts for performance work on
hot MolSysMT coordinate paths.

Current baseline scripts:

- `contact_pair_projection.py`: compares current bounded Python pair-list
  packing with a reviewed immutable helper from Git. Eight deterministic
  Boolean-map cases cover dense/sparse, mapped, rectangular and noncontiguous
  inputs. It verifies exact index results, alternates timing order, retains
  raw repetitions and context, and measures additional traced allocation.
  No coordinate search, molecular geometry, cold-start or RSS speedup is
  measured. Run under an OS resource limit with six explicit thread caps:
  `python -m benchmarks.contact_pair_projection --output .pytest_cache/contact-projection.json`.
  The baseline option executes repository code from that reviewed commit;
  choose a fresh output so earlier evidence is preserved.
- `../devtools/scripts/benchmark_native_copy.py`: measures production resident
  `MolSys` copying, controlled edits/invalidation, selected/full coordinate reads,
  iteration, Rust distance consumption and public H5MSM 0.5 write/load in isolated
  workers. It separates immutable geometry bytes, traced allocations and process
  RSS; see the [native-copy benchmark guide](../devguide/benchmarking/native_copy.md)
  and the dated `native_copy_resident_20261021.json` snapshot. The older
  `study_native_copy.py` snapshots compare prototypes, not these production paths.
  The `native_copy_h5msm_refined_20261021.json` snapshot remeasures public
  persistence after the fresh-load and coordinate-chunk refinements.
  `../devtools/scripts/study_h5msm_structure_chunks.py` retains explicit automatic
  and aligned-layout controls, including private selected-reader measurements;
  it does not define a public selective-file API.
- `native_queries.py`: validates small synthetic expected results and measures
  current native/general queries under issue #128. Includes `MolSys`,
  `Topology`, `Structures`, `ChemicalStates`, `Interactions`, `MolSysBuilder`
  and their supported dictionary representations. Adapter/property timings
  have narrower contracts and are not implemented native-query speedups.
  The dated `native_queries_20261021.json` baseline and the resident/scalar
  comparisons retain separate source commits and benchmark hashes. Compare
  fully validated native/general routes within a campaign; property/trusted
  timings remain narrower references.
  See the [native-query study](../devguide/pending_proposals/native_query_shortcuts.md).
- `h5msm_interactions.py`: checks parity and measures private selective H5MSM
  0.5 queries alongside public `write_layers`/`read_layers`, file size, and
  queries after a public load.
  See the [H5MSM benchmark guide](../devguide/benchmarking/h5msm.md).
- `structure_coordinate_paths.py`: measures small deterministic baselines for
  public structure wrappers and the local kernel-input preparation helpers used
  by those wrappers on the lightweight `particles 4` `XYZ` trajectory.
- `../devtools/scripts/benchmark_ionic_interactions.py`: measures synthetic
  ionic calculation stages, eager/chunked native/file paths, sparse query costs,
  and public H5MSM 0.5 interaction-layer persistence in isolated workers.
  Run cases sequentially without other benchmark jobs. It records Linux
  address-space peak RSS separately from the possibly inherited rusage peak.
  The dated checkpoints are in `baselines/ionic_*.json`; molecular fixtures,
  independent checks, reproduction commands, and interpretation are described
  in the [ionic benchmark guide](../devguide/benchmarking/ionic.md).
- `rust/bench_release_runtime.py`: runs isolated Rust-only release workloads
  for startup, first versus repeated calls, peak memory, explicit 1/2/4-thread
  scaling, and bounded nested concurrency. Every workload validates its result.

Run:

```bash
python benchmarks/structure_coordinate_paths.py
python benchmarks/native_queries.py --iterations 3 --repeats 5 --output /tmp/native-queries.json
python benchmarks/rust/bench_release_runtime.py --output /tmp/molsysmt-rust-runtime.json
```

## Competitive-session evidence and baseline ownership

To measure a new competitive session without renewing the committed reference,
choose a separate output explicitly:

```bash
python benchmarks/competitors/run_matrix.py --output .pytest_cache/benchmarks/current_session.json
python benchmarks/compare_runs.py --baseline benchmarks/baselines/competitor_matrix_session.json --current .pytest_cache/benchmarks/current_session.json --threshold 0.15 --report .pytest_cache/benchmarks/comparison.json
```

The runner gives each campaign an owned temporary reference PDB and removes it
on completion or failure. It does not reuse or remove a pre-existing
`solvated_villin.pdb` in the checkout. Omitting `--output` retains the historical
manual baseline-generation destination; baseline renewal remains a separate
reviewed operation. A CI result must not replace its reference before comparison.

The comparer requires [versioned comparable-session evidence](../devguide/benchmarking/comparable_sessions.md),
including known runtime/provider/resource/unit identities, actual molecular
inputs and observable/precision descriptions, and raw repeat samples agreeing
with the median. Identical missing metadata is not compatibility. Complete
compatible observations return zero, including advisory warnings above 15
percent. Partial/invalid/historical/incompatible evidence remains unevaluable
and returns a diagnostic failure; it never approves performance.

Scientifically correct implementations stay available. Confirm representative,
repeated comparable product inefficiency before opening/updating its improvement
issue; direct external slowdowns alone do not identify a product defect. Native
numeric equality is checked before timing. Competitive workers construct their
objects through fresh spawn factories, with finite deadlines and bounded IPC
lifecycle; startup/preparation stay outside timed samples. Legacy arbitrary
closure/fork campaigns remain bounded but unqualified after arbitrary native
parent preparation. Baseline renewal is separate and reviewed; September data
and original failed campaigns stay unchanged. The performance workflow remains
advisory, and correctness tests keep their own mandatory roles.

The performance workflow is configured to retain reference/current JSON when produced, the
source commit and producer/comparison logs for fourteen days, including after
measurement or comparison failure. A failed producer can have logs without a
completed current session; this is incomplete evidence, not a passing result.
Shell logging preserves native failures through `pipefail`. Provisioning before
reference acquisition can fail without producing a session artifact. Hosted
upload itself remains subject to the applicable workflow's executed result.

After regenerating `competitor_matrix_session.json` or `macro_kernels_session.json`,
synchronize the copies served by the documentation and verify that they match:

```bash
python devtools/scripts/sync_benchmark_docs.py
python devtools/scripts/sync_benchmark_docs.py --check
```

The coordinate-path script prepares common operations before timing and reports
median/min/max time per call for representative coordinate-heavy workflows.
The Rust release script uses fresh subprocesses to keep startup and memory
evidence separate from steady-state timing. It asserts that no Numba JIT cache
files are created.

The historical Rust-versus-Numba adoption scripts are archived under
`devguide/archive/rust_pilot_benchmarks/`. They are not current release tools.

### Native topology storage

Run `python benchmarks/micro/test_topology_storage.py` to record construction
time, materialized bytes per atom, and the incremental cost of materializing
the optional `formal_charge` chemical-state column. The 1,000- and 100,000-atom
cases make regressions in fixed overhead and scaling visible without treating
the measurements as hard cross-machine limits.
