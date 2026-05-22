# Digestion and Dependencies

## Argument Digestion (`arg_digest`)
- All public functions must validate inputs with `@arg_digest`.
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

### Universal Digestion
As of the 1.0.0 stabilization, *every* function in *every* form module (including internal delegates like `get`, `set`, and `extract` inside `__init__.py`) must be decorated with `@arg_digest`. This ensures that data normalization happens even in deep conversion chains.

### 🎫 The Passport Protocol (`ValidatedPayload` Bypass)

To avoid crippling overhead when a decorated public function internally calls another decorated function, MolSysMT implements the **Passport Protocol** utilizing `argdigest`'s `ValidatedPayload`.

#### 1. What is the Passport Protocol?
When an object is validated once at the entry boundary of the public API, it can be wrapped in a `ValidatedPayload` (a passport). When this passport is passed as an argument to another function decorated with `@arg_digest`, the decorator automatically detects it, **bypasses standard digestion entirely (Zero-Latency)**, and forwards the pre-validated value to the function body.

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

#### 3. Empirical Performance Wins
Empirical benchmarking shows that applying the Passport Protocol on even a single simple parameter like `threshold` delivers an immediate **1.51x speedup** on function execution times by completely skipping redundant Pint physical unit validation and type-safety check blocks.

Always use `ValidatedPayload` for high-frequency internal function calls to maintain both API type safety and bare-metal execution speeds.

#### 4. Passports (`ValidatedPayload`) vs. `skip_digestion=True`

- **`skip_digestion=True`** is a coarse-grained override. It bypasses digestion for *all* arguments of a function call. It is useful in very low-level internal kernels, but it is fragile because it disables all type safety and requires manual propagation down the call stack.
- **`ValidatedPayload` (Passports)** is a fine-grained, value-level bypass. It only bypasses validation for the specific arguments that have already been validated, leaving other arguments (such as new selections or flags) subject to normal validation. This keeps the execution safe while achieving zero-latency for heavy objects.
- **Audit Rule**: Avoid passing `skip_digestion=True` in internal calls if the only reason was to avoid double-digesting a specific heavy argument (like coordinates). Instead, wrap that argument in a `ValidatedPayload` and let normal validation run for other parameters. Use `skip_digestion=True` only when *none* of the arguments in the call need any validation or normalization whatsoever.

## Dependency Policy
MolSysMT distinguishes **hard** vs **soft** dependencies:
- Hard: required for core functionality.
- Soft: optional features; must be lazily imported.

Rules:
- Never import soft dependencies at module top-level.
- Use `@dep_digest(library)` to guard optional functionality.
- Validate architecture with `devtools/scripts/validate_dependencies.py`.

### 🚀 High-Performance Lazy Loading (Sprint Decision)
To ensure near-instantaneous `import molsysmt` in all environments (HPC, Cloud, Notebooks), we have implemented a **String-Based Lazy Registry**:

1. **`_convert_to` dictionaries**: In every form's `__init__.py`, the values in the `_convert_to` dictionary must be **strings** representing the function name (e.g., `'to_molsysmt_MolSys'`), not the function objects themselves.
2. **Dynamic Resolution**: `molsysmt.basic.convert` uses `importlib` to resolve these strings only when the specific conversion path is triggered.
3. **Outcome**: This architectural pattern prevents Python from parsing and loading submodule code for soft dependencies (like OpenMM or MDTraj) unless they are actually used.

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
5) Ensure `_convert_to` uses strings.

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
