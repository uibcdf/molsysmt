# PyUnitWizard Guide (Canonical)

Source of truth for integrating and using **PyUnitWizard** in this library.

Metadata
- Source repository: `pyunitwizard`
- Source document: `standards/PYUNITWIZARD_GUIDE.md`
- Source version: `pyunitwizard@bc69459`
- Last synced: 2026-08-15

## What is PyUnitWizard

PyUnitWizard is a "Quantities and Units Assistant" designed to provide a unified API over multiple Python unit backends. It allows libraries to work with physical quantities regardless of their internal representation (`pint`, `unyt`, `openmm.unit`, `astropy.units`, or `string`).

## Why this matters in this library

- **Interoperability**: Allows this library to accept and return quantities in any format chosen by the user.
- **Consistency**: Centralizes unit conversion, standardization, and validation logic.
- **Transparency**: Integrates with `smonitor` to provide traceable unit operations.

## Dependency Management

PyUnitWizard follows a strict separation between Hard and Soft dependencies:

- **Hard Dependencies**: `numpy` and `pint`. These are always available.
- **Soft Dependencies**: `unyt`, `openmm.unit`, `astropy.units`. These are optional and managed via `depdigest`.

## Minimum initialization (required pattern)

All libraries in a process share **one** PyUnitWizard kernel. A library that configures it
unconditionally on import therefore overwrites whatever was already there — and with lazy
imports, "whatever was already there" may be a choice the user made twenty minutes ago in
another notebook cell.

So a library configures **only when nobody has decided yet**:

```python
# mylib/_pyunitwizard.py

import pyunitwizard as puw

STANDARD_UNITS = ['nm', 'ps', 'K', 'mole', 'dalton', 'e', 'kJ/mol', 'radians']

if not puw.configure.has_active_policy():
    puw.configure.set_pint_registry_cache(True)
    puw.configure.set_default_form('pint')
    puw.configure.set_default_parser('pint')
    puw.configure.set_standard_units(STANDARD_UNITS, provenance='mylib')

# Fast tracks are named converters, not policy: `to_nanometers` means nanometers
# whatever the active standard units are. Register them unconditionally.
puw.register_fast_track('nanometers', puw.unit('nm'))
```

Declare it **when your package is imported**, not on first use. Reaching the
configuration lazily means `puw.configure.report()` describes an empty session
until something happens to touch it, and a user who calls PyUnitWizard directly
after importing your package gets `NoStandardsError`. The cost is paid once per
process -- a second library declaring the same policy costs about 2 ms -- and
it is a cost the session pays anyway at its first unit operation.

Most of that cost is importing the backend, which is why declaring a policy is
worth pairing with:

```python
puw.configure.set_pint_registry_cache(True)
```

It lets pint cache its parsed definitions on disk, taking registry construction
from about 180 ms to about 17 ms. It must be called **before** anything loads
the pint backend, so it belongs above the standard-unit call. PyUnitWizard
leaves it off by default because writing to a user's filesystem is not
something importing a units library should do uninvited; a suite may reasonably
opt in on its users' behalf. A folder that cannot be written falls back to no
cache rather than failing.

Three rules follow from this, and they are not stylistic:

1. **Importing must not change an active policy.** `has_active_policy()` is the guard. Without
   it, the last import wins and results depend on import order.
2. **Sibling libraries in one suite must declare the *same* policy.** When they agree, who gets
   there first stops mattering. When they disagree, the same call returns `1.0 radian` or
   `57.3 degree` depending on which was imported first — a real defect, observed across
   MolSysSuite before this rule existed.
3. **Identify yourself with `provenance`.** It is what turns "why are my results in degrees?"
   into a ten-second question.

### Authority over the policy

From strongest to weakest:

1. an explicit unit, form, or parser passed to a call;
2. an explicitly entered `puw.context(...)`;
3. the policy chosen by the application, the user, or the session;
4. PyUnitWizard's factory defaults.

**Being imported is not on that list.** A library declares a policy; it does not own one.

### Reading the active policy

```python
puw.configure.report()
# {'default_form': 'pint', 'default_parser': 'pint',
#  'standard_units': ['nm', 'ps', ...], 'provenance': 'molsysmt',
#  'loaded_libraries': ['pint'], 'loaded_parsers': ['pint'],
#  'fast_tracks': ['nanometers', 'picoseconds']}
```

Use it in a notebook to see what is active and who set it, and in tests to assert that
importing your library did not disturb an existing policy.

### Changing it as a user

Permanently, for the session — this outranks any library, and later imports will not undo it:

```python
puw.configure.set_standard_units(['angstrom', 'fs'])
puw.configure.add_standard_units(['angstrom'])   # replace one dimensionality only
```

Temporarily:

```python
with puw.context(standard_units=['angstrom', 'fs']):
    ...
```

## Consumer decision guide

Choose the narrowest API that still preserves the boundary contract. A fast path
must remove redundant work, not validation that the caller still owes.

| Consumer need | Preferred API | Contract |
|---|---|---|
| Validate a user-facing physical magnitude | `ensure_quantity(...)` | Parses supported strings, rejects bare values, validates dimensionality, and optionally standardizes or converts. |
| Ask whether an object already has one exact unit | `has_unit(...)` | Returns `True`, `False`, or `None` without inspecting the magnitude. It does not validate dimensionality or shape. |
| Normalize repeatedly to a registered canonical unit | `fast_track.to_<unit>(...)` | Uses the registered specialized converter and bypasses conversion when the unit already matches. |
| Produce a specific unit or backend | `convert(...)` | Performs an explicit conversion; it is not a replacement for a consumer's argument-error contract. |
| Extract a value for a numerical or wire boundary | `get_value(..., to_unit=..., value_type=..., dtype=...)` | Converts and shapes the extracted magnitude in one operation. |
| Perform general scientific introspection | `check(...)`, `get_dimensionality(...)` | Use when the question is genuinely broader than exact-unit canonicity. |

The default rule for public argument digesters is simple:

```python
length = puw.ensure_quantity(length, dimensionality={'[L]': 1})
```

`ensure_quantity()` already has a cheap return path for quantities that match the
configured standard. Do not wrap every call in `has_unit()` pre-emptively. Add an
explicit canonical branch only after measuring a remaining hot path, normally when
the consumer also performs local shape or array normalization.

## Essential API for Developers

### 1. Construction
Always use factory functions. Strings are parsed automatically using the default parser.
```python
q = puw.quantity(10.0, 'nm')
q_from_str = puw.quantity('10.0 nm') # Implicit parsing
u = puw.unit('angstroms')
```

### 2. Extraction & Shortcuts
Avoid manual attribute access. Use `get_value_and_unit` for efficient unpacking.
```python
val = puw.get_value(q, to_unit='angstroms')
unit = puw.get_unit(q)
value, unit = puw.get_value_and_unit(q) # Recommended shortcut
```
`get_value` can coerce the output type/shape for you — prefer this over manual
`float(...)` / `np.asarray(...)` wrapping:
```python
r  = puw.get_value(q, to_unit='angstroms', value_type=float)              # Python scalar (errors if non-scalar)
xs = puw.get_value(q, to_unit='angstroms', value_type=list, dtype=float)  # nested list of floats
a  = puw.get_value(q, to_unit='angstroms', value_type=np.ndarray, dtype=np.float32)
```
`value_type` accepts `float`/`int` (scalar), `list`, `tuple`, `np.ndarray` (and
their string aliases); `dtype` sets the array dtype.

### 3. Comparison (Science-Aware)
Never use `==` for quantities. Use the API to handle tolerance and compatibility.
```python
if puw.are_compatible(q1, q2):
    if puw.are_close(q1, q2, rtol=1e-5):
        ...
```

### 4. Conversion & Standardization
Bridge between different formats effortlessly:
```python
# Convert to a specific form and unit
q_openmm = puw.convert(q, to_unit='nm', to_form='openmm.unit')

# Standardize to the project's canonical units
q_std = puw.standardize(q)
```

### 5. Introspection & Validation
Verify inputs without worrying about the underlying backend:
```python
dim = puw.get_dimensionality(q) # Returns e.g. {'[L]': 1}
if puw.is_dimensionless(q):
    ...

if not puw.check(q, dimensionality={'[L]': 1}, shape=(3,)):
    raise ValueError("Expected a 3D length vector")
```

For a measured hot path that only needs to know whether an object already carries
an exact unit, use `has_unit`. It does not inspect the magnitude:

```python
match = puw.has_unit(q, "nanometer")
if match is True:
    normalized = q
else:
    # False means "a different exact unit", not "a compatible unit".
    # None means the cheap predicate cannot decide. Both require the general
    # validation path at a user-facing boundary.
    normalized = puw.ensure_quantity(
        q,
        dimensionality={'[L]': 1},
        to_unit="nanometer",
        standardized=False,
    )
```

The tri-state result is deliberate:

- `True`: the exact unit matches; the consumer may skip unit conversion.
- `False`: the exact unit differs; dimensional compatibility is still unknown.
- `None`: the input or backend cannot answer through the cheap metadata path.

Never interpret `False` as permission to convert without validation at a boundary
whose contract promises a specific argument error. A private adapter may use a
registered fast track directly only when its caller already owns that validation or
the adapter deliberately translates conversion failures into its local error type.

To **digest a physical-magnitude argument** in one call — the canonical pattern
for argument validators (e.g. ArgDigest digesters) — use `ensure_quantity`:
```python
# Parse strings, accept any recognized quantity form, REJECT bare numbers,
# require [L] dimensionality, and return it standardized (nm) — or in to_unit.
radius = puw.ensure_quantity(radius, dimensionality={'[L]': 1})
r_ang  = puw.ensure_quantity(radius, dimensionality={'[L]': 1}, to_unit='angstroms', standardized=False)
```
`ensure_quantity` raises `ArgumentError` when the value is not a quantity (bare
number) or does not match `dimensionality`. It replaces the hand-rolled
`parse → is_quantity → check → standardize → raise` block. This is how the suite
enforces "physical magnitudes must carry explicit units; bare numbers are not
accepted."

Consumer libraries may translate this exception into their own public error type.
They must preserve the original exception as the cause and retain the argument name
and caller context.

## SMonitor Integration

PyUnitWizard is instrumented with `@smonitor.signal`. Traceable tags include:
- `['construction']`, `['extraction']`, `['comparison']`, `['conversion']`, `['standardization']`, `['validation']`, `['parse']`, `['introspection']`.

## Required behavior (non-negotiable)

1.  **Lazy Backend Checks**: Do not assume optional backends are installed. Use `puw.is_quantity()` or catch `LibraryNotFoundError`.
2.  **No Direct Backend Imports**: Never `import pint` or `import unyt` in your scientific logic. Rely exclusively on the `puw` API.
3.  **Use Contexts for Tests**: When testing unit-sensitive code, use `puw.context` to ensure a deterministic environment.
4.  **Never configure unconditionally on import**: guard with `has_active_policy()`. See "Minimum initialization".

```python
with puw.context(default_form='pint', standard_units=['nm', 'ps']):
    # Test logic here...
    ...
```

## Naming conventions

- **Form names**: Use canonical strings (`'pint'`, `'unyt'`, `'openmm.unit'`, `'astropy.units'`, `'string'`).
- **Dimensionality**: Use standard notation (`'[L]'`, `'[M]'`, `'[T]'`, etc.).

## 6. Performance: Fast-Track Conversions

Generic unit conversion (`standardize`) is powerful but can be slow. PyUnitWizard allows registering domain-specific "Fast-Tracks" for common units.

### 6.1 Registering Fast-Tracks
Host libraries should register their canonical units during initialization (usually in `_pyunitwizard.py`).

```python
import pyunitwizard as puw
puw.register_fast_track("nanometers", puw.unit("nm"))
```

### 6.2 Using Fast-Tracks
Once registered, optimized conversion functions are available under the `fast_track` namespace.

```python
# Instant bypass if obj is already in nanometers
val = puw.fast_track.to_nanometers(obj)
```

### 6.3 Performance Guarantee
Fast-track functions use direct object comparison and "trusted path" guards, making them ideal for high-frequency loops or argument digesters.

Fast tracks do not make a user-facing boundary trusted. Preserve dimensionality,
shape, dtype, and local exception validation unless the caller has already established
those invariants.

## Consumer anti-patterns

Avoid these patterns in new code:

- `check(value, dimensionality=...)` followed by `standardize(value)` when
  `ensure_quantity()` expresses the complete boundary contract.
- `get_unit(value) == unit("nm")` merely to detect an already-canonical input; use
  `has_unit()` for that exact question.
- direct access to backend attributes such as Pint's `.units` in scientific logic.
- identity registries, passports, or mutable-object caches whose only purpose is to
  remember that a quantity was canonical.
- unconditional `standardize()` or conversion of a quantity constructed locally in an
  already-canonical unit.
- adding `has_unit()` to an unmeasured cold path. The general API is clearer and its
  own canonical path may already be sufficient.

## Adoption and regression checklist

Before changing a consumer path:

1. Identify the boundary: public validation, private normalization, numerical kernel,
   backend adapter, or wire serialization.
2. Record the current error, dimensionality, shape, dtype, form, and identity contract.
3. Measure representative canonical and non-canonical inputs with telemetry settings
   stated explicitly.
4. Add a regression test proving canonical input avoids the expensive general route.
5. Add a regression test proving an incompatible unit is still rejected with the
   consumer's documented error type.
6. Preserve shape and dtype normalization; unit canonicity proves neither.
7. Re-run the focused tests and the consumer's normal full-suite gate.

The optimization is successful only when the canonical path becomes cheaper without
changing non-canonical behavior or weakening validation.

---
*Document created on February 6, 2026, as the authority for PyUnitWizard integration; consumer fast-path policy
updated on August 13, 2026; unit-configuration authority added on August 15, 2026.*
