# Structural attribute resolution ignores the structure axis of the system

**Reported:** 2026-08-03, while designing the fix for
[`iterator_without_explicit_attributes_fails_for_partial_forms.md`](iterator_without_explicit_attributes_fails_for_partial_forms.md).

**Status:** **RESOLVED (archived 2026-08-03).** Implemented and verified; see
*Resolution*.

**Severity:** scientific-integrity risk. A composite molecular system could
silently lose a trajectory, and two structural series of the same system could be
returned with contradictory lengths and no diagnostic.

## Symptom

### Item order silently decides how many structures the system has

```python
msm.get([h5msm, dcd], n_structures=True)   # -> 20
msm.get([dcd, h5msm], n_structures=True)   # ->  1
```

Both lists name the same files, the same molecule and the same trajectory. The
H5MSM file holds one reference structure; the DCD holds twenty.

### That propagates into conversion as data loss

```python
msm.convert([dcd, h5msm], to_form='molsysmt.MolSys')
# n_structures = 1
# warnings emitted: 0
```

Nineteen structures discarded because the items were listed in the other order.
Nothing is reported.

### Structural series of the same system disagree in length

```python
msm.get([h5msm, dcd], time=True)          # -> length 1
msm.get([h5msm, dcd], coordinates=True)   # -> length 20
# warnings emitted: 0
```

A caller plotting `time` against a per-structure observable receives two
incompatible axes with no signal.

## Cause

`where_is_attribute` resolves each attribute independently and documents its
tie-breaker:

> If multiple items contain the same attribute, the last matching one is returned.

That criterion is sound where it applies, and the maintainer confirms it was
adopted as a needed tie-break rather than to preserve any invariant. The defect is
that it is applied between providers that are **not interchangeable**: an item
holding one reference structure and an item holding a twenty-structure trajectory
are not two ways of supplying the same series.

There is no reordering that could rescue it. `digest_molecular_system`
(`_private/argdigest/argument/molecular_system.py:44-61`) normalizes paths and
validates; `assess_molecular_system` returns the list untouched. Item order is
whatever the caller typed.

## The decisive precedent

The library already refuses to guess on the *atom* axis, and stays silent on the
*structure* axis:

```
[psf(78974 atoms), dcd(4369 atoms)]         -> StructuralInconsistencyError
[h5msm(1 structure), dcd(20 structures)]    -> silence, n_structures = 20
```

`_private/molecular_system_validation.py:144-151` raises when complementary items
disagree on `n_atoms`, and `:102-108` rejects two items providing a primary
topology. **The structure axis is the only axis of a composite molecular system
with no consistency contract.** This report is about completing that contract, not
about introducing a new policy.

## Accepted rule

1. The **structure axis of the system** is the largest `n_structures` among the
   items carrying structural data. It does not depend on item order.
2. A structural attribute may only be delivered by an item that **spans** that
   axis. Among those, the existing tie-break applies unchanged: the last matching
   item wins.
3. An item below the axis holding `None`, zero or one structure is a **reference
   conformation**. Its structural series are dropped and the drop is reported with
   `StructuralAttributeOffAxisWarning`.
4. Two items each holding **more than one** structure, of different lengths, give
   no basis for choosing. That raises `StructuralInconsistencyError`, pointing at
   `molsysmt.concatenate_structures`, which accepts exactly such a list.

### Why the asymmetry with the atom axis is correct, not an exception

Different atom counts mean the items describe **different molecules**. Different
structure counts usually mean one item is a reference and the other a trajectory,
which is legitimate and ordinary: a PDB has one structure, and `[pdb, xtc]` is the
most common composite in molecular dynamics. Measured:

```
psf -> None      pdb -> 1      bcif.gz -> 1      h5msm -> 1      dcd -> 5 / 20
```

A rule requiring agreement would break that workflow. The cut at "one structure
versus more than one" is the physical distinction: a single structure cannot be a
trajectory.

## Acceptance

- `msm.get(items, n_structures=True)` returns the same value for every permutation
  of the same items.
- `msm.convert([dcd, h5msm], ...)` preserves the twenty structures.
- `msm.get` never returns two structural series of one system with lengths that
  contradict `n_structures`.
- Dropping a reference item's series emits `StructuralAttributeOffAxisWarning`
  naming the attributes.
- Two trajectories of different lengths raise `StructuralInconsistencyError`
  naming `molsysmt.concatenate_structures`.
- `[psf, dcd]`, `[pdb, dcd]` and single-item systems keep their current results.

## Resolution

`molsysmt/_private/structure_axis.py` holds the rule: `item_n_structures` reads the
count of one item and `structure_axis` returns the axis together with every item's
count, raising when two trajectories disagree.

The anticipated recursion was real and is avoided as planned. `item_n_structures`
calls the form's `get_n_structures_from_system` directly instead of the public
`get`, because the axis is needed by `where_is_attribute`, which is what `get` uses
to resolve every attribute.

Two call sites consume it, and they had to be treated separately because **`convert`
does not resolve attributes through `where_is_attribute`** — it reimplements the
same last-matching-item search three times over its own per-item attribute sets:

- `basic/where_is_attribute.py` restricts the candidates for a structural attribute
  to the items spanning the axis, then applies the existing tie-break among them.
  When the attribute exists only off the axis, both outputs are `None` and
  `StructuralAttributeOffAxisWarning` is emitted. The `Notes` section of the
  docstring documents this.
- `basic/convert.py` prunes off-axis structural attributes from `from_attributes`
  once, in `_prune_structural_attributes_off_the_axis`, before any of those three
  searches runs. One intervention instead of three.

`StructuralAttributeOffAxisWarning` is a new warning
(`MSM-WARN-STRUCT-006`). `StructuralAttributeDropWarning` was not reused: its
catalog text says "discarded during concatenation" and suggests
`attribute_policy='strict'`, neither of which is true here.

`basic/iterator.py` needed no policy of its own. The structure-axis check added
there while this defect was being diagnosed was removed: `where_is_attribute` now
guarantees that every per-item iterator covers the same axis, so advancing them in
lockstep is correct by construction.

### Verification

| | before | after |
|---|---|---|
| `get([h5msm, dcd], n_structures=True)` | 20 | 20 |
| `get([dcd, h5msm], n_structures=True)` | **1** | 20 |
| `convert([dcd, h5msm], ...)` | **1 structure, 0 warnings** | 20 structures |
| `get([h5msm, dcd], time=True)` | **length 1** | `None` + warning |
| `get([psf, dcd], n_structures=True)` | 5 | 5 |
| `Iterator([h5msm, dcd], chunk=10)` | `TypeError` | 2 chunks of 10 |

Guarded by `tests/basic/test_structure_axis.py`, which parametrizes the rule over
`[None, 5]`, `[1, 20]`, `[20, 1]`, `[20, 20]` and `[None, None]`, asserts order
independence for `get` and `convert`, and asserts the rejection message names
`concatenate_structures`.

**7913 tests pass** across `tests/basic`, `tests/form` and `tests/_private`, with 2
skipped. The only failure is a collection error in `tests/form/openff_*`:
`import openff.toolkit.topology` raises `IndexError` inside
`openff/toolkit/utils/ambertools_wrapper.py:64` in a plain interpreter with no
MolSysMT involved — an AmberTools/OpenFF environment breakage, pre-existing and
unrelated.

### Where the rule lives now

The normative statement is in `devguide/forms_and_conversions.md`, section
*Composite molecular systems and the structure axis*. This report is the evidence
and the reasoning; that section is the contract.

### Still open

The precedence policy for **topological** attributes. `[pdb, psf]` and `[psf, pdb]`
need not agree on which item supplies atom names, and nothing here changes that.
Recorded against open decision 1 of the attribute-centric proposal.

## Related

- [`iterator_without_explicit_attributes_fails_for_partial_forms.md`](iterator_without_explicit_attributes_fails_for_partial_forms.md)
  — its remaining open case is a consequence of this defect and closes with it.
- `pending_proposals/attribute_centric_molecular_system_model.md`, open decisions
  1 and 2: the precedence policy between complementary forms delivering the same
  attribute, and mappings between forms with different index spaces. This is the
  measured evidence those decisions were waiting for.
