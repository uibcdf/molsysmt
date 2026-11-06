(Tutorial_Get_Atom_Name_Correspondence)=
# Matching an atom-name inventory

*Retaining both source index axes through an exact label correspondence.*

Use `msm.topology.get_atom_name_correspondence()` when you explicitly know that
two selected inventories use the same unique atom names. It checks names and
elements through form-agnostic queries. Coordinates and chemical assignments
are not required; it works on pure native `Topology` and supported files or
dictionaries that supply the inventory.

:::{versionadded} 1.0.0
:::

:::{admonition} API documentation
:class: dropdown

{func}`molsysmt.topology.get_atom_name_correspondence`
:::

## Retaining source indices

```python
import molsysmt as msm
from molsysmt.native import Topology

molsys_A = Topology(n_atoms=3)
molsys_A.atoms['atom_name'] = ['C1', 'O1', 'N1']
molsys_A.atoms['atom_type'] = ['C', 'O', 'N']
molsys_B = Topology(n_atoms=3)
molsys_B.atoms['atom_name'] = ['N1', 'C1', 'O1']
molsys_B.atoms['atom_type'] = ['N', 'C', 'O']
pairs = msm.topology.get_atom_name_correspondence(
    molsys_A, reference_molecular_system=molsys_B)
assert pairs.tolist() == [[0, 1], [1, 2], [2, 0]]
```

The detached `int64` array has shape `(n_selected_atoms, 2)`. Column zero is the
query's full source atom index; column one is the reference's full source atom
index. Rows follow query selection order. Atom IDs are labels, not these indices.
Names are case-sensitive and are not trimmed, renamed or guessed. Elements use
MolSysMT's `atom_type` convention, not force-field atom types.

## Restricting each inventory

```python
pairs = msm.topology.get_atom_name_correspondence(
    molsys_A, selection=[2, 0], reference_molecular_system=molsys_B,
    reference_selection=[1, 0])
assert pairs.tolist() == [[2, 0], [0, 1]]
```

Each selection can use positional indices or a supported selection string and
`syntax`. A missing reference input uses the query system; a missing
`reference_selection` uses `selection`, even with a different reference input.
Use `reference_selection='all'` explicitly when that is the intended scope.
Two empty selections return an array of shape `(0, 2)`.

Missing or duplicate names, different selected name sets, incompatible elements,
and repeated or invalid positional indices raise before producing a map. Names
can repeat elsewhere in the system: restrict each selection to the intended
component. Neither input is modified.

## Checking chemistry separately

This tool checks a label correspondence. It does not establish chemical identity,
isotopes, bond connectivity, charge, hydrogen policy or stereochemistry. It does
not choose between ambiguous chemical graphs or replace
`msm.chemical_states.get_atom_correspondences()`, which requires complete declared
chemical context.

For {ref}`template application <Tutorial_Chemical_Templates>`, pass the template
as the query and the observed system as the reference. The result then has the
required `(template_index, observed_source_index)` column order. Explicitly pass
the observed selection as `reference_selection` and use the unchanged public
assessment to verify every mapped atom and the stored graph before application.

:::{seealso}
:class: dropdown

**Related Tools & References**

- {func}`molsysmt.physchem.assess_chemical_template` — Checking the chemistry of an explicit map.
- {func}`molsysmt.chemical_states.get_atom_correspondences` — Enumerating complete-context chemical correspondences.
:::
