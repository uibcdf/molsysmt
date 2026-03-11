# MolSysBuilder

## Purpose

`MolSysBuilder` is the native editable form for constructing or editing a
molecular system before materializing it as `molsysmt.MolSys`.

The builder serves two immediate needs:
- programmatic creation of molecular systems from scratch;
- deterministic test fixtures whose topology and structural metadata are
  declared explicitly instead of inferred from external files.

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
builder = msm.build.edit(molecular_system)
```

An alias such as `msm.build.new_molecular_system()` may be added later for
discoverability, but it is not part of the current first slice.

## Digestion policy

The builder methods currently rely on explicit internal validation instead of
`@arg_digest`.

Reason:
- the builder API uses many optional inputs by design;
- the current local digester set does not yet express that contract cleanly
  without forcing artificial constraints on the API.

This is an explicit temporary decision, not an oversight. Builder-facing
digestion should be revisited after the core builder contract is stable.
