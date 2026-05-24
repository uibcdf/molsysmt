# Performance & Benchmarking

MolSysMT is engineered with a strict **performance-first** mindset. To ensure that our safety layers (argument validation and physical unit checks) do not compromise numerical efficiency, we maintain a comprehensive regression-tested benchmarking suite.

---

## Interactive Performance Dashboard

Below is our interactive performance dashboard, compiled dynamically from the latest benchmarking baseline runs. It compares MolSysMT against established packages (`MDTraj`, `MDAnalysis`) in terms of execution speed and memory footprints, and tracks the latency profiles of our internal validation layers.

```{eval-rst}
.. raw:: html

   <iframe src="../../_static/benchmarks_dashboard.html" 
           style="width: 100%; height: 950px; border: none; border-radius: 16px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3); overflow: hidden;"
           scrolling="no">
   </iframe>
```

---

## Benchmarking Philosophy & Telemetry

Our benchmarking harness is designed around three primary tenets:
1. **Isolated Resource Telemetry**: Benchmarks are executed inside ephemeral, isolated child subprocesses. This ensures that peak memory footprint metrics (Resident Set Size - RSS) start at a clean, consistent baseline (~477 MB) rather than inheriting cumulative high-water mark footprints from previous tasks.
2. **Safety vs. Speed Diagnostics**: We systematically separate micro-benchmarks (checking `@arg_digest` and `PyUnitWizard` latency in microseconds) from macro-benchmarks (assessing Numba JIT math kernels and out-of-core file loaders).
3. **Rigid Regression Gates**: Any code changes committed to the repository must undergo a regression audit. Our CI performance gate ensures that execution times on standard hot-paths do not degrade by more than **15%** against the baseline.

---

## Running the Benchmark Suite

Developers can execute the benchmark harness and compare results locally using the following CLI procedures.

### 1. Generating a Performance Run
To execute all micro and macro benchmarks and export the results to a JSON session file:
```bash
python benchmarks/harness.py --output current_run.json
```

### 2. Auditing for Regressions
To audit your current run against the reference baselines (located under `benchmarks/baselines/`):
```bash
python benchmarks/compare_runs.py --baseline benchmarks/baselines/competitor_matrix_session.json --current current_run.json --threshold 0.15
```

If any hot path has degraded by more than the 15% permitted limit, `compare_runs.py` will exit with a non-zero code, failing the CI validation gate.
