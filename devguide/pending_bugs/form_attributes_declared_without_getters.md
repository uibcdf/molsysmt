# Bug: forms declare attributes they cannot deliver

**Status:** pending (inventory taken 2026-07-12; fixes not started)
**Severity:** high — Tier 1 and Tier 2 forms, public `get()` facade
**Location:** `molsysmt/form/*/attributes.py` vs `molsysmt/form/*/get_*_attributes.py`

## Symptom

A form's `attributes.py` declares an attribute as available, but neither the form
itself nor its pipe implements a getter for it. `get()` then raises a raw
`AttributeError`.

```python
import molsysmt as msm
pdb = msm.systems['T4 lysozyme L99A']['181l.pdb']

parmed_structure = msm.convert(pdb, to_form='parmed.Structure')
msm.get(parmed_structure, element='atom', atom_name=True)
# AttributeError: module 'molsysmt.form.parmed_Structure' has no attribute 'get_atom_name_from_atom'
```

This is distinct from
[`get_single_attribute_bypasses_piping.md`](get_single_attribute_bypasses_piping.md):
there the getter exists behind a pipe and `get()` refuses to use it. Here there is
no getter to reach, by any path. Fixing the piping bug will **not** fix these.

`file:inpcrd` was the extreme case — 12 attributes declared, zero getters
implemented, both `get_*_attributes.py` modules left as untouched scaffolding.
That one has already been repaired; the rest of this inventory has not.

## Inventory

Taken by cross-checking each form's declared attributes against the getters it
implements and the getters reachable through its pipes (followed transitively).
Spot-verified against live `get()` calls with the element declared in the
attribute catalog.

### Tier 1

| Form | Declared | Unreachable | Pipes | Examples |
|---|---:|---:|---|---|
| `mdtraj.Trajectory` | 56 | **36** | no | `group_name`, `box_angles`, `bond_id`, all `n_*` counts |
| `molsysmt.StructuresDict` | 15 | 7 | no | `box_angles`, `box_lengths`, `box_shape`, `box_volume`, `occupancy` |
| `file:structures_yaml` | 15 | 7 | yes | same set as `StructuresDict` |
| `openmm.Topology` | 51 | 4 | no | `box_angles`, `box_lengths`, `box_shape`, `box_volume` |
| `molsysmt.MolSys` | 85 | 3 | no | `atom_ff_type`, `formal_charge`, `partial_charge` |
| `molsysmt.Structures` | 16 | 1 | no | `atom_index` |
| `molsysmt.MolSysBuilder` | 32 | 1 | no | `bonded_atom_pairs` |
| `file:pdb`, `file:bcif`, `string:pdb_id`, `string:alphafold_id`, `mdtraj.Topology` | — | 1 each | — | `bond_id` |

### Tier 2

| Form | Declared | Unreachable | Pipes | Examples |
|---|---:|---:|---|---|
| `rdkit.Mol` | 74 | **74** | no | everything, including `atom_name` and `coordinates` |
| `parmed.Structure` | 51 | **51** | no | everything; the form implements 2 getters |
| `MDAnalysis.Universe` | 23 | **21** | no | `atom_name`, `atom_type`, `coordinates` |
| `openmm.Simulation` | 55 | 7 | yes | `box_*`, `forcefield`, `integrator`, `temperature` |
| `openmm.Modeller` | 52 | 4 | yes | `box_angles`, `box_lengths`, `box_shape`, `box_volume` |
| `molsysviewer.MolSysView`, `nglview.NGLWidget` | 72 | 5 each | yes | `bond_id`, `kinetic_energy`, `potential_energy`, `temperature`, `total_energy` |
| `openmm.Context` | 9 | 1 | no | `temperature` |

`molsysmt.Topology`, `file:h5msm`, `molsysmt.MolSysDict`, `molsysmt.TopologyDict`,
`file:molsys_yaml`, `file:topology_yaml` and `file:xtc` are clean.

## Why the support contract did not catch this

`support_tiers.ipynb` reports Yes/Yes for all Tier 1 and Tier 2 forms, and that
remains true: the contract and parity tests exercise **conversion**
(`_convert_to`), which works. The `get()` facade over these same forms was never
part of the verified surface. A form can round-trip perfectly through `convert`
and still be unable to answer `get(item, atom_name=True)`.

## Proposed fix

Per form, one of two remedies, and the choice is a design decision, not a
mechanical one:

- **Declare the missing pipe.** `parmed.Structure`, `rdkit.Mol` and
  `MDAnalysis.Universe` have no pipes at all and only a handful of getters. They
  almost certainly want `piped_topological_attribute = 'molsysmt.Topology'` and
  `piped_structural_attribute = 'molsysmt.Structures'`, the way `file:pdb` does.
  This is the cheap fix and covers most of the inventory.
- **Implement the getter.** Where the attribute is genuinely native to the form
  and cheap to read there, or where no pipe target can supply it (`bond_id`,
  the derived `box_*` quantities, `atom_ff_type`, `formal_charge`,
  `partial_charge`), a real getter is required.

Where neither is warranted, the honest fix is the third option: **stop declaring
the attribute** in `attributes.py`.

The piping bug must be fixed first, otherwise adding pipes changes nothing for
single-attribute calls.

## Prevention

The form adapter conformance linter passes all 92 forms today, `file:inpcrd`
included when it had zero getters, because it never cross-checks the promise
against the delivery. See
[`form_linter_does_not_check_attribute_delivery.md`](form_linter_does_not_check_attribute_delivery.md).
