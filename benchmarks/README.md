# Coordinate Path Baseline

This directory stores lightweight benchmark scripts for performance work on
hot MolSysMT coordinate paths.

Current baseline scripts:

- `structure_coordinate_paths.py`: measures small deterministic baselines for
  public structure wrappers and the local kernel-input preparation helpers used
  by those wrappers on the lightweight `particles 4` `XYZ` trajectory.
- `rust/bench_release_runtime.py`: runs isolated Rust-only release workloads
  for startup, first versus repeated calls, peak memory, explicit 1/2/4-thread
  scaling, and bounded nested concurrency. Every workload validates its result.

Run:

```bash
python benchmarks/structure_coordinate_paths.py
python benchmarks/rust/bench_release_runtime.py --output /tmp/molsysmt-rust-runtime.json
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
