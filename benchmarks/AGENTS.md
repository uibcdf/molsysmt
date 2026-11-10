# Benchmark working instructions

Follow the root `AGENTS.md` and `MOLSYSSUITE_GUIDE.md`. For performance disposition,
follow [the accepted advisory policy](../devguide/benchmarking/performance_policy.md).

- Keep scientifically correct implementations available regardless of relative
  speed. Efficiency measurements are advisory, including comparisons with third
  parties and with earlier MolSysMT versions.
- Preserve the default 15 percent review threshold and require comparable,
  repeated measurements before reporting an attributed efficiency issue. Track
  confirmed shortcomings as improvement issues; do not hide slow measurements.
- Keep incomplete/invalid evidence unevaluable and preserve native diagnostic
  failures, baselines and artifacts. Advisory status is not a scientific pass.
- Keep numerical-correctness and data-integrity assertions mandatory in their
  owning tests. Never remove them to make a timing campaign successful.
