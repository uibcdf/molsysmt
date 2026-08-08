# ArgDigest Guide (Canonical)

Source of truth for integrating and using **ArgDigest** in this library.

Metadata
- Source repository: `argdigest`
- Source document: `standards/ARGDIGEST_GUIDE.md`
- Source version: `argdigest@0.10.0`
- Last synced: 2026-08-07

## What is ArgDigest

ArgDigest is a lightweight toolkit for **auditing, validating, and normalizing** function arguments in scientific libraries. It decouples complex input-handling logic from scientific code by providing a standardized orchestration layer.

It covers **two axes**, and an integration is only complete when both are declared:

| Axis | Question it answers | You declare |
| --- | --- | --- |
| **1. The function argument contract** | *May this function receive this argument at all, and does it have what it needs?* | `FunctionContract` and `Domain` |
| **2. The argument value contract** | *Given an argument name, is its value valid and in canonical form?* | one digester per argument name |

Axis 2 has always been the visible half. Axis 1 arrived in `0.10.0`, and without it
function-dependent rules have nowhere to live: they end up scattered across per-argument
digesters, one `if caller == ...` at a time, and the contract of a function is never
written down in one readable place.

## Why this matters in this library

- **Consistency**: All functions share the same argument-handling logic.
- **Interoperability**: Coerces heterogeneous inputs (dictionaries, strings, etc.) into canonical internal objects.
- **Diagnostics**: Produces consistent error messages with actionable hints.
- **Traceability**: Integrates with `smonitor` to provide execution breadcrumbs.

## 1. Required Configuration (`_argdigest.py`)

Create a file named `_argdigest.py` in your package root. ArgDigest uses the module name of the decorated function to find this file automatically.

```python
# MyLibrary/_argdigest.py

# Axis 2 -- the value contract of each argument.
DIGESTION_SOURCE = "MyLibrary._private.argdigest.argument"
DIGESTION_STYLE = "package"
STRICTNESS = "warn"            # missing digester for a declared parameter

# Axis 1 -- the argument contract of each function.
FUNCTION_SOURCE = "MyLibrary._private.argdigest.function"
DOMAIN_SOURCE = "MyLibrary._private.argdigest.domain"
UNKNOWN_ARGUMENT = "error"     # keyword outside the function's contract

# Declared aliases, applied before both axes.
NORMALIZATION_SOURCE = "MyLibrary._private.argdigest.normalization"
```

`STRICTNESS` and `UNKNOWN_ARGUMENT` answer different questions and address different
people. A missing digester is a to-do for the library author, so `warn` is right. A
keyword nobody declared is a mistake by whoever made the call, and warning is not enough:
warnings are routinely filtered off exactly where users read output.

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

## 4.3 Declared normalization (argument-name aliases)

A library should accept the names its users type. Declare them as data, one module per
family of rules in `NORMALIZATION_SOURCE`:

```python
from argdigest import AliasTable

# everywhere
table = AliasTable(aliases={'residue_index': 'group_index'})

# only in one function, or a family
AliasTable(applies_to='mylib.basic.compare.compare',
           aliases={'attributes_type': 'attribute_type'})
AliasTable(applies_to='mylib.form.*', aliases={'idx': 'index'})

# guarded on another argument of the same call
AliasTable(applies_to='mylib.basic.get.get', when={'element': 'atom'},
           aliases={'name': 'atom_name', 'index': 'atom_index'})
```

Tables compose most-specific-first, renaming is a single pass, and argument order is
preserved.

**Scope the table to the callers where the alias means what it says.** A name that is an
attribute in one function is often an ordinary parameter in another; declaring an
attribute synonym globally in MolSysMT rewrote a real adapter parameter and broke 76
tests.

**Write the tables out; do not generate them.** A `{element}_{name}` template is shorter
and admits names that do not exist -- it produced six attributes nothing defines, so a
wrong name failed far from where it was written.

Normalization runs **before** the function contract, so declaring a contract never breaks
a library's aliases, while a genuine typo survives unchanged and is refused.

The `standardizer` hook still runs, after the declared tables, and remains the escape
hatch for a rename that cannot be stated as a table. Its contract is
`(caller, kwargs) -> mapping`, checked at both decoration and call time.

## 4.4 Caller-aware optional semantics

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

Caller-keyed digesters remain the right tool for **value** semantics that depend on the
callable. What does *not* belong there is which arguments a function accepts at all: that
is axis 1, and it has its own place since `0.10.0`. See section 4.5.

## 4.5 The function argument contract (axis 1)

### Why the default is strict

Plain Python raises `TypeError` for an unexpected keyword. **ArgDigest must never end up
more permissive than the language it wraps**, so `UNKNOWN_ARGUMENT` defaults to `error`.
This restores parity rather than inventing a policy, and it closes a defect class that is
the worst kind in a scientific library: a mistyped argument that runs with the default and
returns a plausible wrong answer.

### What you get for free

| Your function | Its default contract | You declare |
| --- | --- | --- |
| closed signature | held to its own parameters | nothing |
| declares `**kwargs` | admits anything | a domain, or it stays permissive |

A closed signature already *is* a domain, so most functions are protected without a line
of configuration. A function with `**kwargs` opened its door deliberately and ArgDigest
cannot guess what it meant.

### Declaring a domain

A `Domain` is a named, introspectable set of admissible keyword names. Point it at your
library's own source of truth rather than copying names into a list, so the two cannot
drift apart:

```python
# MyLibrary/_private/argdigest/domain/attribute.py
from argdigest import Domain
from MyLibrary.attribute import attributes, is_attribute

domain = Domain(name='attribute', contains=is_attribute,
                members=lambda: tuple(attributes),
                description='canonical attribute names')
```

`contains` decides membership; `members` enumerates it when possible, which is what
enables near-miss suggestions and introspection. Either is enough.

### A domain that depends on another argument

Sometimes which keywords are admissible depends on a value in the same call: an engine, an
output type, a mode. Declare the table and the argument it keys on:

```python
Domain(
    name='engine_options',
    depends_on='engine',
    by_value={
        'MolSysMT': ('threshold', 'parallel'),
        'OpenMM':   ('threshold', 'platform'),
    },
)
```

`depends_on` may name several arguments, in which case the table is keyed by a tuple.

It is still data: `describe_contract` renders the whole table, so the options each value
accepts can be documented rather than discovered by reading code.

**A value with no entry does not refuse anything.** It means the domain cannot decide for
this call — usually because that value is itself wrong — and the argument carrying it is
about to be rejected by its own digester, which explains the real problem far better than
a complaint about an unknown argument would.

**Key on an argument, not on a derivation.** The table is consulted per call, so the value
must be cheap to read. If deciding the domain requires computing something expensive from
another argument, the mechanism costs more than it saves and the function is better left
permissive with the reason recorded.

### Declaring a contract

```python
# MyLibrary/_private/argdigest/function/get.py
from argdigest import FunctionContract

contract = FunctionContract(
    caller='MyLibrary.basic.get.get',
    admits='attribute',                 # signature + this domain
)
```

A module may declare one `contract`, or several through a `CONTRACTS` list. Beyond
`admits`, a contract can declare `requires_any_of`, `mutually_exclusive` and
`co_required`.

Use `caller_pattern` instead of `caller` to cover a family, with `fnmatch` syntax:

```python
contract = FunctionContract(caller_pattern='MyLibrary.form.*.to_file_h5msm',
                            admits='signature')
```

Resolution is **most specific first**: exact caller, then the longest matching pattern,
then the default.

### Where it runs, and why there

```
bind_arguments -> standardizer -> function contract -> digestion
```

After the standardizer, so an alias that has just become its canonical name is never
mistaken for a typo. Before digestion, because validating the value of an argument that
should not be there is wasted work ending in a confusing failure.

### Reading a contract back

`describe_contract(contract, domains)` renders it as plain data. This is why a contract is
declarative rather than an opaque callable: the accepted domain of a `**kwargs` function
is invisible to `inspect.signature`, and this is what makes it readable again for
documentation, IDEs and agents.

### Known gap

A **delegating** domain, whose admissible keywords depend on values resolved at call time
-- a converter chosen by a `to_form` argument, for instance -- is not expressible, because
a `Domain` decides membership from the keyword alone. Those functions keep the permissive
default.

## 5. Required behavior (non-negotiable)

1.  **Lazy Digestion**: Digestion only happens when the function is called.
2.  **No Top-Level Imports**: Guard optional dependencies (like Pydantic or Beartype) inside your pipelines or use ArgDigest's native support.
3.  **Support skip_digestion**: All decorated functions should allow bypassing digestion via a `skip_digestion` parameter for internal performance-critical calls.
4.  **Argument Dependencies**: Digesters can request other (already digested) arguments by simply adding them to their signature. ArgDigest handles the topological sort and cycle detection.
5.  **Caller-aware Optionality**: Downstream libraries may accept `None` or otherwise relaxed values for specific public callables. These semantics belong in digesters, not in bypasses around `@arg_digest`.
6.  **Use Normalization Passports (`ValidatedPayload`)**: For internal high-frequency calls where inputs are already validated, pass them wrapped in a `ValidatedPayload` (the passport protocol) to bypass redundant digestion and unit-safety check blocks with zero latency.
7.  **Declare both axes**: a function taking `**kwargs` must declare the domain those keywords come from. Leaving it undeclared means the function accepts anything, which is the defect axis 1 exists to prevent. If a domain genuinely cannot be expressed, record why.

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

## 6. Performance: The Normalization Passport (`ValidatedPayload`)

To avoid redundant unit conversions and introspection in recursive function calls, `argdigest` supports a "Passport" protocol.

### 6.1 What is a `ValidatedPayload`?
It is a lightweight container that carries a value along with its verified metadata (unit, dtype, etc.). When the `@arg_digest` decorator receives a `ValidatedPayload`, it bypasses standard digestion if the contract matches.

### 6.2 Emitting Payloads
Scientific pipelines (e.g., `sci:nm_float64_payload`) should return a `ValidatedPayload` instead of a raw array when internal trust is desired.

```python
from argdigest.core.contract import ValidatedPayload
# Inside a pipeline or custom digester
return ValidatedPayload(value=array, unit="nm", dtype="float64")
```

### 6.3 Benefits
- **Zero Latency**: Internal calls skip PyUnitWizard entirely.
- **Contract Safety**: Guarantees JIT-ready data (e.g., float64) across function boundaries.
