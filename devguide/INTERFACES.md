# Interface Contract

This document defines cross-form public behavior. Operation-specific docstrings
and tests remain the authority for arguments and return values.

## Molecular-system forms

A form is an in-memory object, file representation, or recognized string kind
registered under `molsysmt/form`. Public operations discover forms lazily and
delegate to adapters or convert through an available route.

The same public operation should have equivalent scientific semantics across
supported forms, but support is capability-specific. A form being recognized
does not guarantee that it can deliver every topology or structure attribute.
Consult `molsysmt._private.form_tier.FORM_TIERS`, adapter declarations, and delivery
tests.

## Selections

- MolSysMT indices are zero-based.
- The default syntax is `MolSysMT` unless a public signature says otherwise.
- A selection can require topology conversion or adapter getters; identical
  syntax does not imply identical cost across forms.
- Alternative syntaxes are supported only on explicitly implemented paths.
- Unsupported syntaxes or parameter combinations must fail with a typed,
  actionable error rather than being silently reinterpreted.

Selection normalization does not excuse loss of topology. Forms lacking the
attributes required by an expression must fail or use a tested conversion path.

## Attribute delivery

Adapter `attributes` declarations are capability metadata, not proof of working
delivery. Public `get()` may use direct getters or piping to another form. Tests
must therefore exercise the public path and verify values, shapes, units, and
ordering; structural validation of the adapter module is insufficient.

Canonical structural conventions are:

- coordinates: `(n_structures, n_atoms, 3)`, nm;
- box: `(n_structures, 3, 3)`, nm;
- time: ps;
- charge: elementary charge.

## Files, remote identifiers, and iterators

File forms differ in random access, lazy I/O, topology content, and writable
capabilities. Do not infer lazy loading from a binary extension or eager loading
from a text extension. Heavy compatibility requires an implemented
`StructuresIterator`, explicit `_heavy_support`, and operation-level tests.

Remote identifier forms perform network I/O only when a conversion requiring a
download is requested. Download source, priority, cache, and offline behavior
are implementation-specific and must be tested independently; they are not a
universal interface promise.

## Third-party bridges

Third-party adapters are optional and must be imported lazily. A conversion
contract identifies the attributes it preserves. “Conversion succeeded” does
not by itself guarantee bond orders, identifiers, metadata, precision, unit
provenance, or round-trip equivalence.

Every supported bridge needs tests appropriate to its declared fidelity. Lossy
conversions should be documented explicitly and, when scientifically relevant,
emit structured diagnostics.

## Failure behavior

Expected form probes return `False`. Once an operation accepts an item as a
molecular system, unsupported capabilities, malformed content, or conversion
failures must not be hidden as a probe miss or a successful `None` result. See
`error_policy.md` and `DIAGNOSTICS.md`.
