# MolSysSuite Integration Proposals

This document collects architectural improvements for `smonitor`, `argdigest`, `depdigest`, and `pyunitwizard` discovered during the MolSysMT 1.0.0 stabilization sprint.

## 1. Type-Safe Quantity Pipelines (`argdigest` + `pyunitwizard`)

**Problem**: Developers manually cast quantities to `float64` NumPy arrays before calling Numba kernels to avoid type-mismatch crashes. This is repetitive and fragile.

**Proposal**: Introduce a high-level pipeline in `argdigest` (e.g., `as_float64_array(unit='nm')`).
- **Benefit**: The business logic receives a "guaranteed" float64 array.
- **Observability**: If casting fails, `argdigest` attaches the offending data's metadata to the SMonitor `ArgumentError` context automatically.

## 2. Semantic Remediation Registry (`smonitor` + `argdigest`)

**Problem**: Errors often tell the user *what* failed, but not *how* to fix it scientifically.

**Proposal**: A global registry mapping error patterns to "Remediation Hints".
- **Example**: If `argdigest` catches an `UndefinedUnitError` from `pyunitwizard` while parsing a selection, `smonitor` resolves a hint: *"The unit 'X' is not recognized. Did you mean 'nanometers'?"*.
- **Benefit**: Transforms the library from a technical tool into an empathetic assistant.

## 3. JIT Performance Telemetry (`smonitor` + `lazy_njit`)

**Problem**: JIT compilation latency is a "black box".

**Proposal**: `lazy_njit` should emit a `DEBUG` signal with the compilation time and cache status (Hit/Miss).
- **Benefit**: Developers and QAs can audit which kernels are bottlenecks.
- **Self-Healing**: If compilation takes too long, SMonitor could suggest calling `molsysmt.warmup_numba()`.

## 4. Golden Evidence in Probes (`smonitor` + `is_form`)

**Problem**: `is_form` returning `False` is a silent failure.

**Proposal**: Standardize the `MSM-DBG-PROBE-001` signal to include a "Golden Evidence" payload.
- **Content**: A snippet of the data that failed (e.g., the first 100 bytes of a file or the dict keys).
- **Benefit**: Instant debugging of format detection without re-running code.
