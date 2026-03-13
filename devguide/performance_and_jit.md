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

## Structure Kernel Input Preparation

During the March 2026 performance pass, we clarified an important design
boundary:

- `molsysmt.basic.get()` is a public convenience API and structures its output
  for users;
- `molsysmt.lib.structure` kernels are numeric kernels and are unit-agnostic;
- therefore, hot structure wrappers must prepare kernel inputs without changing
  the user-facing unit policy of the public API.

This means we must not force a canonical unit such as `nm` merely because a
kernel is hot. The working unit carried by the public wrapper remains the unit
that will be used to reconstruct the public quantity after the kernel returns.

The accepted pattern is:

1. public wrapper retrieves coordinates with `get(...)`;
2. wrapper prepares kernel inputs through helpers in
   `molsysmt.lib.structure._kernel_inputs`;
3. helper normalizes rank/shape, requests the numeric value in `float64`, and
   aligns paired inputs to a shared working unit when needed;
4. wrapper rebuilds the public output using the carried working unit and then
   applies the usual public standardization policy.

Current helpers:

- `extract_coordinates_value_and_unit(...)`
- `align_coordinates_values_and_unit(...)`

Why they exist even after recent PyUnitWizard improvements:

- PyUnitWizard now exposes more explicit extraction control (`value_type`,
  `dtype`);
- but MolSysMT still needs domain-specific logic for coordinate rank
  normalization and paired-input alignment before entering Numba kernels.

Current adoption:

- `get_center`
- `get_distances`
- `get_rmsd`
- `get_least_rmsd`
- `least_rmsd_fit`
- `get_angles`
- `get_dihedral_angles`
- `principal_component_analysis`
- `set_dihedral_angles`

Initial measurement snapshot:

- a lightweight baseline now lives in `benchmarks/structure_coordinate_paths.py`;
- the first stable run uses the bundled `particles 4` `XYZ` trajectory to
  isolate coordinate-path cost without mixing in heavier topology rebuilds;
- on that baseline, local kernel-input preparation is not the bottleneck:
  - `extract_coordinates_value_and_unit(...)` is around `6.5e-4 s`;
  - `align_coordinates_values_and_unit(...)` is around `8.2e-4 s`;
  - `structure.get_center(...)` is around `2.13e-1 s`;
  - `structure.get_distances(...)` is around `2.22e-1 s`;
  - `structure.get_rmsd(...)` is around `2.63e-1 s`.

Interpretation:

- the new local helpers are cheap relative to the hot public wrappers;
- this supports the architectural decision to keep kernel-facing preparation in
  `molsysmt.lib.structure._kernel_inputs` rather than trying to eliminate it;
- if more optimization is needed, the next likely bottlenecks are higher in the
  wrapper/public retrieval path rather than in the local extraction/alignment
  helpers themselves.

What remains open:

- decide whether `basic.get()` eventually needs a lighter internal path for hot
  structural consumers, or whether the current split between public `get()`
  and `molsysmt.lib.structure._kernel_inputs` is already sufficient.
- measure heavier `MolSys/HDF5`-based coordinate workflows after the local
  Numba cache-locator issue is resolved for development checkouts; those paths
  must not be conflated with the correctness of the current structure-helper
  architecture.

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
