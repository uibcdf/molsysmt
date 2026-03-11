# MolSysBuilder

## Purpose

`MolSysBuilder` is the native editable form for constructing or editing a
molecular system before materializing it as `molsysmt.MolSys`.

The builder serves two immediate needs:
- programmatic creation of molecular systems from scratch;
- deterministic test fixtures whose topology and structural metadata are
  declared explicitly instead of inferred from external files.

The testing motivation is important enough to be explicit. In many converter
tests, a file format such as PDB is otherwise forced to play two roles at once:
- the source under test;
- the source of truth for assertions.

That is weak because the truth then depends on an external parser or on another
conversion path. `MolSysBuilder` breaks that loop. A test can first declare the
exact molecular truth in native editable form, materialize it to `MolSys`, then
export it to a target format such as PDB, and finally test round-trip or
converter behavior against the original declared truth. This is the preferred
strategy for future deterministic converter fixtures.

## Current supported conversion surface

The first slice intentionally keeps the conversion surface narrow:
- `MolSysBuilder()` from scratch;
- `MolSys -> MolSysBuilder`;
- `MolSysBuilder -> MolSys`.

Broader `X -> MolSysBuilder` and `MolSysBuilder -> X` support should be added
later by routing through `MolSys`.

## Native and form roles

`MolSysBuilder` belongs to both:
- `molsysmt/native`, as the native editable class;
- `molsysmt/form/molsysmt_MolSysBuilder`, as the form that integrates the
  builder with `get()`, `info()`, `convert()`, and form discovery.

This split is intentional:
- native code owns declared-state editing and `build()`;
- the form adapter owns MolSysMT integration.

The current form-level integration now covers:
- direct topological attribute getters on declared state;
- direct structural attribute getters on declared state;
- `basic.set()` support for declared labels and structural arrays;
- `info()` over declared builder state;
- `select()` over declared builder state.

## State semantics

`MolSysBuilder` always represents a **declared**, potentially incomplete
molecular system.

It does not have separate "declared" and "resolved" modes. Queries against the
builder must reflect only what has been declared so far.

Consequences:
- `get()` and `info()` on the builder do not apply fallback hierarchy;
- missing molecules or entities remain missing while the object is still a
  builder;
- structural completion and hierarchy fallback happen only in `build()`.

## `build()`

`build()` is the single crystallization point. It always returns
`molsysmt.MolSys`.

During `build()`:
- singleton groups are created for atoms that still lack groups;
- components are derived from bonds;
- missing chains, molecules, and entities are completed using the same native
  fallback rules already defined for `MolSys` and `Topology`;
- structure arrays are validated against the declared topology.

`build()` is not a general converter. Conversion to other forms should happen
after a builder has been materialized as `MolSys`.

## Supported builder operations in v1

Topology declaration:
- `add_atom(...)`
- `add_group(atom_indices=[...], ...)`
- `add_bond(atom_index_1, atom_index_2, ...)`
- `add_chain(group_indices=[...], ...)`
- `add_molecule(group_indices=[...], ...)`
- `add_entity(molecule_indices=[...], ...)`

Structural declaration:
- `set_coordinates(...)`
- `set_box(...)`
- `set_time(...)`
- `set_structure_id(...)`

## Hard API rules

The builder API is intentionally strict:
- `add_atom()` does not accept `atom_index`;
- `add_atom()` does not accept `group_index`;
- `add_group()` accepts existing `atom_indices`, not unresolved references;
- higher-level `add_*()` methods accept existing lower-level indices only;
- `component` is never added manually and is always derived in `build()`.

These rules keep the builder deterministic and avoid silent ambiguity during
construction.

## Discoverability

Creating an empty system is done directly with:

```python
builder = msm.MolSysBuilder()
```

Editing an existing molecular system is done with:

```python
builder = msm.build.editable(molecular_system)
```

Creating an empty editable system can be done either directly with the class or
through the discoverable build helper:

```python
builder = msm.build.editable()
```

An alias such as `msm.build.new_molecular_system()` may still be added later
for discoverability, but it is not part of the current first slice.

## Editing-policy implications for `molsysmt.build`

The builder introduces a single preferred path for explicit topology editing:
- `molsysmt.MolSysBuilder`
- `molsysmt.build.editable(...)`

As a consequence, these legacy explicit-editing helpers are now considered
deprecated for the `1.0` line:
- `molsysmt.build.add_bonds`
- `molsysmt.build.remove_bonds`
- `molsysmt.build.define_new_chain`

This does not weaken the rest of `molsysmt.build`. Higher-level construction,
repair, and chemically-informed editing functions remain valid members of the
namespace.

## Digestion policy

The builder methods use `@arg_digest`, but they rely on caller-sensitive
digesters to accept semantically valid `None` values for optional inputs such as
`molecular_system=None` in `molsysmt.build.editable(...)` or `atom_type=None`
in `MolSysBuilder.add_atom(...)`.

This is intentional. The builder is not a special-case escape from digestion; it
is a valid public API that requires a richer caller-aware digestion contract.
The supporting caller helpers now live upstream in `argdigest.core.caller`.

## Current test checkpoint

The current builder slice is covered by:
- native tests for empty builders, explicit declaration, hierarchy fallback, and
  `MolSys <-> MolSysBuilder`;
- build-helper tests for `molsysmt.build.editable(...)`;
- form-level tests for declared-state `get`, `set`, `info`, and `select`.

This means the builder already participates in the standard MolSysMT API wheel
for the narrow `MolSys <-> MolSysBuilder` conversion surface agreed for v1.
