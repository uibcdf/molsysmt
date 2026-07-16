# Digestion and Dependencies

## Argument Digestion (`arg_digest`)
- Public functions that accept user-facing values requiring normalization should
  validate them with `@arg_digest`; classes, predicates, compatibility wrappers,
  and thin helpers follow their local contract.
- The ArgDigest configuration lives in `molsysmt/_argdigest.py`.
- Place `@dep_digest` **below** `@arg_digest` so it works on normalized args.
- For quantity strings, digesters must parse with `puw.parse.parse(...)`
  (not `puw.parse(...)`), following the current PyUnitWizard API layout.

Important scope rule:

- `@arg_digest` is the normalization boundary for public and semi-public API
  entrypoints;
- it is not the place to encode all kernel-facing preparation needed by hot
  numerical wrappers;
- when a hot wrapper needs shape normalization or paired-unit alignment before
  entering `molsysmt.lib`, that logic should live next to the kernel layer
  rather than being forced into generic public digestion.

This rule was clarified during the March 2026 performance pass. The motivating
example was structural coordinates:

- public digestion remains responsible for validating external inputs;
- `basic.get()` remains responsible for user-facing retrieval semantics;
- `molsysmt.lib.structure._kernel_inputs` now holds the extra preparation
  required specifically by structure kernels.

### Digestion boundaries

Public functions and adapter entry points use `@arg_digest` when they accept
user-facing values requiring normalization. Small private helpers must remain
focused and should not be decorated merely to satisfy a blanket rule. Trusted
internal calls may use passports or `skip_digestion=True` only after their
inputs have been normalized at a clear boundary.

### 🎫 The Passport Protocol (`ValidatedPayload` Bypass)

To avoid crippling overhead when a decorated public function internally calls another decorated function, MolSysMT implements the **Passport Protocol** utilizing `argdigest`'s `ValidatedPayload`.

#### 1. What is the Passport Protocol?
When an object is validated once at the entry boundary of the public API, it can
be wrapped in a `ValidatedPayload` (a passport). A compatible digester can then
bypass the applicable repeated normalization. This reduces work but is not a
literal zero-latency guarantee.

#### 2. How to Use It
If you have already validated or normalized an object (e.g., coordinates, box, or selection thresholds) and need to pass it to an internal delegate or another public API:

```python
from argdigest.core.contract import ValidatedPayload

# Wrap your validated object in a passport
coordinates_passport = ValidatedPayload(
    value=coordinates_qty, 
    unit="nm", 
    dtype="float64", 
    ndim=3
)

# Pass the passport to the subsequent decorated function
result = another_decorated_function(molecular_system, coordinates=coordinates_passport)
```

#### 3. Performance evidence

A May 2026 benchmark pass measured a 1.51x improvement for one threshold case.
That result is environment- and workload-specific. Use `ValidatedPayload` only
where profiling identifies repeated normalization and tests prove that the
payload metadata is correct.

#### 4. Passports (`ValidatedPayload`) vs. `skip_digestion=True`

- **`skip_digestion=True`** is a coarse-grained override. It bypasses digestion for *all* arguments of a function call. It is useful in very low-level internal kernels, but it is fragile because it disables all type safety and requires manual propagation down the call stack. 
  The decorator provides a direct fast path for `skip_digestion=True`; it still
  incurs ordinary Python call overhead and must not be described as zero cost.
- **`ValidatedPayload` (Passports)** is a fine-grained, value-level bypass. It only bypasses validation for the specific arguments that have already been validated, leaving other arguments (such as new selections or flags) subject to normal validation. It reduces repeated work but still has Python dispatch and contract-check overhead.
- **Audit Rule**: Avoid passing `skip_digestion=True` in internal calls if the only reason was to avoid double-digesting a specific heavy argument (like coordinates). Instead, wrap that argument in a `ValidatedPayload` and let normal validation run for other parameters. Use `skip_digestion=True` only when *none* of the arguments in the call need any validation or normalization whatsoever.

## Dependency Policy
MolSysMT distinguishes **hard** vs **soft** dependencies:
- Hard: required for core functionality.
- Soft: optional features; must be lazily imported.

Rules:
- Never import soft dependencies at module top-level.
- Use `@dep_digest(library)` to guard optional functionality.
- Validate architecture with `devtools/scripts/validate_dependencies.py`.

### Package lazy loading
MolSysMT uses lazy loading to reduce import work without promising a fixed
startup time across environments:

1. **Package-Level PEP 562 Lazy Loading**: The package entry point uses PEP 562
   `__getattr__` and `__dir__` for the registered public surface. Core startup
   configuration and diagnostics are still imported eagerly. A May 2026 run
   measured a reduction from 3.34 seconds to approximately 500 ms; reproduce
   that benchmark before treating it as current.
2. **Lazy converter registry**: `_convert_to` currently accepts callables and
   strings naming converter modules. Prefer strings where importing the
   converter would eagerly load optional or expensive code. Existing callable
   entries remain valid and should be migrated only with tests.
3. **Dynamic Resolution**: `molsysmt.basic.convert` and the package-level
   `__getattr__` resolve registered code on demand and cache package attributes
   after successful resolution.

### ♨️ Unified Preheating Engine (`molsysmt.warmup()`)
To support clean performance profiling and JIT compilation, MolSysMT exposes a unified preheating API:

*   **`molsysmt.warmup(numba=True, modules=True, strict=False, return_report=False)`**:
    - **`modules=True` (default)**: Attempts to resolve all registered lazy
      attributes.
    - **`numba=True` (default)**: Pre-compiles all registered Numba JIT kernels.
    - **`strict=True`**: Propagates unexpected lazy-import failures for QA.
    - **`return_report=True`**: Reports compiled kernels, loaded attributes,
      expected optional-dependency skips, and unexpected failures.
*   **Deprecation Alias**: The old `warmup_numba()` function is preserved as a deprecated legacy wrapper that issues a warning and delegates to `warmup(numba=True, modules=True)`. Always use `molsysmt.warmup()` in new scripts and benchmarks.

The default return value remains the number of compiled kernels for backward
compatibility. Missing soft dependencies are recorded as skipped capabilities;
other failures emit `WarmupFailureWarning` unless strict mode propagates them.

## Single Source of Truth
Dependency status and form mapping live in `molsysmt/_depdigest.py`.

Key configuration fields:
- `LIBRARIES` (hard vs soft)
- `MAPPING` (form directory → library)
- `SHOW_ALL_CAPABILITIES`
- `EXCEPTION_CLASS`

## Maintenance
When moving a dependency from hard → soft:
1) Move imports inside functions.
2) Add `@dep_digest`.
3) Update `_depdigest.py`.
4) Ensure form mapping exists.
5) Prefer lazy string converter entries when they avoid eager optional imports.

## PyUnitWizard Interaction Policy

The current ecosystem split after the March 2026 audit is:

- PyUnitWizard provides reusable quantity extraction and conversion services;
- MolSysMT uses those services at the API boundary and, where necessary, inside
  local kernel-input helpers;
- MolSysMT should not fork PyUnitWizard semantics locally, but it may add
  kernel-specific preparation steps when PyUnitWizard's generic extraction is
  not sufficient on its own.

This is why MolSysMT now depends on PyUnitWizard's expanded extraction API
(`value_type`, `dtype`) while still keeping its own shape and pairing helpers
for structure kernels.
