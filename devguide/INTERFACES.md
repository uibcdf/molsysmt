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

## Scalar types in returned values

**The container decides the scalar type.**

- Rectangular, homogeneous data is returned as a `numpy.ndarray` with an explicit
  `dtype`, or as a PyUnitWizard `Quantity` wrapping one.
- Ragged, nested, `set` or `dict` data is returned with **native Python scalars**:
  `int`, `float`, `str`, `bool`.

A NumPy scalar inside a Python container is not a middle ground between the two.
NumPy's advantages — contiguous memory, vectorised operations — belong to the
array, not to the scalar. Boxed into a `list` or a `set`, an `np.int64` costs more
memory than an `int` and is slower to traverse, and buys nothing back. Measured on
200 000 integers: `list` of `np.int64` 8.02 MB and 7.7 ms to sum, `list` of `int`
7.22 MB and 2.5 ms, `ndarray` 3.20 MB and 0.2 ms.

Three consequences make this a contract rather than a preference:

- **Serialisation.** `json.dumps` and `yaml.safe_dump` raise on NumPy scalars.
  A caller cannot dump what a public function returned.
- **Type identity.** `isinstance(np.int64(1), int)` is `False` under NumPy 2.x, so
  downstream code that validates with `isinstance` rejects values MolSysMT
  documents as integers.
- **Range.** Python `int` has arbitrary precision; `np.int64` overflows silently.

Nothing is lost by choosing native scalars for ragged data: `np.array` over a list
of Python `int` infers `int64`, and both types index an array identically. There is
no `dtype` to preserve in a container that holds one object per element.

Mixing the two in one container is the failure this rule exists to prevent. It
arises when a structure is assembled by Python-level iteration over arrays instead
of through `ndarray.tolist()`, and it is not cosmetic: it produces containers whose
elements answer `isinstance` differently from one another.

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
