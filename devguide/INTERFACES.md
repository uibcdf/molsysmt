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

## Periodic box origin

**The box vectors describe shape and size. The cell they span starts at the origin,
and coordinates live in `[0, L)`.**

Molecules are kept whole, so a few atoms sit just outside the cell where one crosses
a face. That is the correct picture, not a defect: on a solvated 1VII the three
solvation engines leave between 0.9 % and 1.7 % of atoms outside, and MDTraj's
`image_molecules` produces the same signature on the same system.

The convention is not arbitrary. It is what `msm.pbc.wrap_to_pbc` already assumed,
and it is what the ecosystem does: OpenMM's `enforcePeriodicBox` returns a system in
`[0, L]`, and MDTraj's `image_molecules` moves one centred on the origin into `[0, L]`.
NAMD is the exception that proves the point by parameterising `cellOrigin` explicitly.

There is no computational argument either way. The minimum-image kernels operate on
displacement vectors, which are invariant under the choice of origin — see
`mic_vector_ortho` in `rust/src/mic.rs` — and wrapping costs one `floor` or one
`round` per axis whichever convention is chosen. The reason to pick this one is
interoperability: exporting to the majority of forms then needs no translation, and a
translation on every export is a place for defects to live.

Anything that builds a box must land in this convention, and the requirement is on
the result rather than on the route. `msm.build.solvate` reaches it through three
engines that do not agree by themselves: the native one centres the solute before
adding water, while OpenMM's `Modeller` and PDBFixer return a system centred on the
origin, which is a corner of the cell. Left unnormalised that put 86 % of atoms
outside the box, and the notebook that tried to correct it with an atom-wise wrap
stretched 93 bonds of the solute to 6.8 nm.

## Scalar types in returned values

**The nature of the datum decides the container; the container decides the scalar
type.**

- Numeric physical magnitudes — the things computations are performed on — are
  returned as a `numpy.ndarray` with an explicit `dtype`, or as a PyUnitWizard
  `Quantity` when they carry units: `coordinates`, `box`, `b_factor`, `occupancy`.
- Identifiers, labels, categories and relations are returned in Python containers
  with **native Python scalars**: `atom_index`, `atom_name`, `atom_id`,
  `group_name`, `chain_id`, `bond_type`, `bonded_atom_pairs`.
- A single count or measure is returned as a native scalar, or as a `Quantity` when
  it carries units.

Shape decides nothing. `bonded_atom_pairs` is rectangular — *n* rows of two — and is
correctly a `list`, because it is a relation between atoms and not a matrix anyone
computes on. Conversely a ragged numeric magnitude would still not become a list of
floats. Ask what the datum *is*, not what shape it happens to have in one system:
some attributes are rectangular for one molecular system and ragged for the next.

Whatever the container, a NumPy scalar inside a Python one is not a middle ground.
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

Nothing is lost by choosing native scalars in a Python container: `np.array` over a
list of Python `int` infers `int64`, and both types index an array identically.
There is no `dtype` to preserve in a container that holds one object per element.

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
