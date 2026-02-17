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

## Peptide Builder Performance Notes
`build_peptide(engine="MolSysMT")` relies on repeated non-bonded heavy-atom
distance evaluations during geometry optimization. The hot loops must stay in
reusable JIT kernels under `molsysmt/lib` (for example,
`molsysmt.lib.math.minimum_distance_masked_not_bonded` and
`molsysmt.lib.math.minimum_distance_between_coordinate_sets`) and be called
from Python orchestration code in `molsysmt/build/build_peptide.py`.

This split is intentional:
- Python layer: topology/template logic and search strategy.
- JIT layer: tight numeric loops (distance scans, masks, bonded exclusions).

### Nested kernels and signature rules
- Nested JIT calls must resolve against compiled dispatchers, not Python
  wrappers. The lazy compiler binds only symbols actually referenced by the
  function bytecode.
- For optional `None` arguments in signatures, use the `[numba_type, None]`
  pattern through `make_numba_signature(...)`. This is translated to
  `numba.optional(numba_type)` and must not be handled as `Omitted(None)`.

## Warmup
Provide explicit precompilation with:
```
molsysmt.warmup_numba()
```
This precompiles registered kernels and avoids first-use latency.

## First-use Warning
The first JIT compilation triggers a one-time SMonitor warning to inform
users about the expected delay.
