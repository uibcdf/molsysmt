# Performance and JIT

## Import Strategy (Lightweight Startup)
`import molsysmt` must remain fast. Performance-heavy kernels are loaded and
compiled lazily. Avoid importing heavy modules or soft dependencies at module
top-level.

## Numba Policy
Numba kernels live in `molsysmt/lib`. Use the `lazy_njit` helper for all JIT
functions to ensure compilation happens on first use, not on import.

### Rules
- Do not use `@nb.njit` directly in library modules.
- Use `lazy_njit(signature, cache=True)` from `molsysmt._private.jit`.
- Avoid heavy global initialization in `molsysmt/lib` modules.

## Warmup
Provide explicit precompilation with:
```
molsysmt.warmup_numba()
```
This precompiles registered kernels and avoids first-use latency.

## First-use Warning
The first JIT compilation triggers a one-time SMonitor warning to inform
users about the expected delay.
