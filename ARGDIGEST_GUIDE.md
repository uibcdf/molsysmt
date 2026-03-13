# ArgDigest Guide (Canonical)

Source of truth for integrating and using **ArgDigest** in this library.

Metadata
- Source repository: `argdigest`
- Source document: `standards/ARGDIGEST_GUIDE.md`
- Source version: `argdigest@0.9.3-dev`
- Last synced: 2026-03-10

## What is ArgDigest

ArgDigest is a lightweight toolkit for **auditing, validating, and normalizing** function arguments in scientific libraries. It decouples complex input-handling logic from scientific code by providing a standardized orchestration layer.

## Why this matters in this library

- **Consistency**: All functions share the same argument-handling logic.
- **Interoperability**: Coerces heterogeneous inputs (dictionaries, strings, etc.) into canonical internal objects.
- **Diagnostics**: Produces consistent error messages with actionable hints.
- **Traceability**: Integrates with `smonitor` to provide execution breadcrumbs.

## 1. Required Configuration (`_argdigest.py`)

Create a file named `_argdigest.py` in your package root. ArgDigest uses the module name of the decorated function to find this file automatically.

```python
# MyLibrary/_argdigest.py

DIGESTION_SOURCE = "MyLibrary._private.digestion.argument"
DIGESTION_STYLE = "package"
STRICTNESS = "warn" # "warn", "error", or "ignore"
```

### Advanced Configuration
You can also load configurations from external files:
```python
from argdigest.config import load_from_file
cfg = load_from_file("rules.yaml") # Supports .py, .yaml, .json
```

## 1.1 Runtime Dependency Contract

ArgDigest requires:
- `smonitor` for diagnostics and telemetry.
- `depdigest` for conditional dependency checks via `@dep_digest`.

Do not replace `depdigest` integration with local no-op fallbacks in runtime code.
If dependency checks are disabled silently, behavior diverges across environments and
diagnostic quality degrades.

## 2. Core API for Developers

### 2.1 The `@arg_digest` Decorator
The primary entry point. It handles both argument-centric discovery and explicit mapping.

```python
from argdigest import arg_digest

@arg_digest(type_check=True) # Optional beartype integration
def my_function(molecular_system, selection='all'):
    ...
```

### 2.2 Explicit Mapping (`arg_digest.map`)
Use this when you need specific pipelines for specific arguments. Global `kind` and `rules` will apply to any argument not explicitly mapped.

```python
@arg_digest.map(
    item={"kind": "topology", "rules": ["is_valid"]},
    value={"kind": "std", "rules": ["to_bool"]}
)
def process(item, value):
    ...
```

## 3. Mandatory Registration Pattern

Define reusable pipelines in your library to ensure consistency:

```python
from argdigest import register_pipeline

@register_pipeline(kind="feature", name="feature.base")
def coerce_feature(obj, ctx):
    # Transformation logic
    return obj
```

**Note**: ArgDigest natively supports **Pydantic models** as rules. If a rule is a class with `.model_validate()`, it will be executed automatically.

## 4. Science-Aware Features

### 4.1 PyUnitWizard Integration
Manage physical quantities by passing a `puw_context`:

```python
@arg_digest(puw_context={"standard_units": ["nm", "ps"], "form": "pint"})
def simulate(time):
    ...
```

### 4.2 Profiling
Enable performance tracking for your digestion pipelines:

```python
@arg_digest(profiling=True)
def heavy_func(data):
    ...

# After execution, access the audit log:
print(heavy_func.audit_log)
```

## 4.3 Caller-aware optional semantics

ArgDigest must support public APIs whose valid input contract depends on the
callable that is being digested. This is not an escape hatch; it is a normal
requirement in scientific libraries with editable builders and staged
construction APIs.

Examples of valid caller-specific optional semantics:
- `molecular_system=None` in a helper that creates a new editable system when no
  input is provided;
- `atom_type=None` in a builder method that infers atom type from `atom_name`;
- `entity_name=None` in a builder method that deliberately leaves the value
  undeclared until a later crystallization step.

The recommended pattern is:
- keep `@arg_digest` on the public callable;
- encode the optional semantics in the digester, keyed by caller;
- use `argdigest.core.caller.normalize_caller`, `caller_matches`,
  `caller_is_one_of`, and `caller_startswith` instead of open-coding caller
  string logic downstream.

Do not push valid public APIs outside digestion just because some arguments are
optional for specific callables. If the API contract is legitimate, ArgDigest
should express it.

## 5. Required behavior (non-negotiable)

1.  **Lazy Digestion**: Digestion only happens when the function is called.
2.  **No Top-Level Imports**: Guard optional dependencies (like Pydantic or Beartype) inside your pipelines or use ArgDigest's native support.
3.  **Support skip_digestion**: All decorated functions should allow bypassing digestion via a `skip_digestion` parameter for internal performance-critical calls.
4.  **Argument Dependencies**: Digesters can request other (already digested) arguments by simply adding them to their signature. ArgDigest handles the topological sort and cycle detection.
5.  **Caller-aware Optionality**: Downstream libraries may accept `None` or otherwise relaxed values for specific public callables. These semantics belong in digesters, not in bypasses around `@arg_digest`.

## SMonitor Integration

ArgDigest is heavily instrumented with `@smonitor.signal`:
- The core decorator uses `tags=["digestion"]`.
- `Registry.run` uses `tags=["pipeline"]`.
- Every digestion attempt is traceable in the global breadcrumb trail.

### Emission Failures

Do not swallow SMonitor emission failures with `except Exception: pass`.
If an emission fails in a non-critical path, emit a fallback warning/log message that
includes execution context and the original exception text.

---
*Document created on February 6, 2026, as the authority for ArgDigest integration.*

## 5. Performance: The Normalization Passport (`ValidatedPayload`)

To avoid redundant unit conversions and introspection in recursive function calls, `argdigest` supports a "Passport" protocol.

### 5.1 What is a `ValidatedPayload`?
It is a lightweight container that carries a value along with its verified metadata (unit, dtype, etc.). When the `@arg_digest` decorator receives a `ValidatedPayload`, it bypasses standard digestion if the contract matches.

### 5.2 Emitting Payloads
Scientific pipelines (e.g., `sci:nm_float64_payload`) should return a `ValidatedPayload` instead of a raw array when internal trust is desired.

```python
from argdigest.core.contract import ValidatedPayload
# Inside a pipeline or custom digester
return ValidatedPayload(value=array, unit="nm", dtype="float64")
```

### 5.3 Benefits
- **Zero Latency**: Internal calls skip PyUnitWizard entirely.
- **Contract Safety**: Guarantees JIT-ready data (e.g., float64) across function boundaries.
