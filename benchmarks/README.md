# Coordinate Path Baseline

This directory stores lightweight benchmark scripts for performance work on
hot MolSysMT coordinate paths.

Current baseline script:

- `structure_coordinate_paths.py`: measures small deterministic baselines for
  public structure wrappers and the local kernel-input preparation helpers used
  by those wrappers on the lightweight `particles 4` `XYZ` trajectory.

Run:

```bash
python benchmarks/structure_coordinate_paths.py
```

The script warms common Numba kernels before timing and reports median/min/max
time per call for a small set of representative coordinate-heavy workflows. In
development checkouts it also disables Numba disk cache inside the benchmark
process, because some local source layouts do not provide a stable cache
locator.

At the moment the heavier `MolSys/HDF5` profile is intentionally left out of
the default baseline because a local Numba cache-locator issue interferes with
those paths during development runs. That follow-up remains tracked in
`devguide/performance_and_jit.md`.
