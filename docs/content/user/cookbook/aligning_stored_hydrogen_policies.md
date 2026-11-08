(cookbook-aligning-hydrogen-policies)=
# Aligning stored hydrogen policies

*Applying an explicit common representation before strict correspondence.*

A conversion and fixed-state H generator may retain the same indexed H but
different implicit-H permission flags. Those flags are part of the declared
chemical graph. The following synthetic example creates that difference
deliberately; its optional SMILES input route uses RDKit. The policy operation
itself reads native assignments.

## Declaring the difference

```python
import molsysmt as msm

molsys_A = msm.convert('smiles:[2H]O')
molsys_B = msm.copy(molsys_A)
msm.set(molsys_A, selection="atom_type=='H'", allows_implicit_hydrogens=True)
msm.set(molsys_B, selection="atom_type=='H'", allows_implicit_hydrogens=False)
before = msm.chemical_states.get_atom_correspondences(
    molsys_A, selection=[1], reference_molecular_system=molsys_B,
    reference_selection=[1], max_matches=16,
)
assert before['search_complete']
assert before['atom_correspondences'].shape == (0, 1, 2)
```

Atom 1 is oxygen. Selecting it still retains its unselected chemical environment,
including the indexed deuterium. Zero admitted maps is a refusal to establish
correspondence; it is not a zero RMSD or an invitation to ignore stored fields.

## Applying an explicit policy

```python
result_A = msm.chemical_states.normalize_indexed_hydrogen_policy(molsys_A)
result_B = msm.chemical_states.normalize_indexed_hydrogen_policy(molsys_B)
normalized_A = result_A['molecular_system']
normalized_B = result_B['molecular_system']
assert result_A['report']['status'] == 'normalized'
assert result_B['report']['status'] == 'unchanged'
after = msm.chemical_states.get_atom_correspondences(
    normalized_A, selection=[1], reference_molecular_system=normalized_B,
    reference_selection=[1], max_matches=16,
)
assert after['search_complete']
assert after['atom_correspondences'].shape == (1, 1, 2)
```

The {ref}`policy's admission rules <Tutorial_Normalize_Indexed_Hydrogen_Policy>`
are mandatory. Unknown counts, charged/radical or unsupported H relationships
remain errors. Isotopes, stereo, H-parent edges and heavy-atom assignments stay
explicit; genuine chemical differences can still give zero maps. No molecular
equivalence, pose quality or docking result follows from this example.

## Saving the declaration

```python
msm.h5msm.write(normalized_A, 'normalized_policy.h5msm')
restored = msm.h5msm.read('normalized_policy.h5msm')
record = restored.chemical_states.get_preparation_history()[-1]
assert record['report']['method'] == 'closed_neutral_terminal_hydrogens'
assert record['report']['changed_atom_indices'].tolist() == [0]
assert record['report']['atom_correspondence'] == {'indices': 'identity', 'n_atoms': 2}
```

Each successful call records its original source axes and producer version,
including an unchanged result. Older history survives. Subsequent extraction
does not reinterpret those historical indices as current positions. Native
outputs share protected geometry blocks through deferred copying; mutable
chemistry is independent. Changed chemistry invalidates analyses only on the
returned system. See {ref}`cookbook-migrating-h5msm` for file layers and resident
load boundaries.

The real P59 regression uses two unmodified pinned AutoDock Vina SDFs, their
existing native/RDKit interpretation, fixed-state H generation, both normal and
pm/fs/coulomb policies and H5MSM. That provider composition is tested separately
from any consumer's complete docking workflow or installed artifact.

:::{seealso}
:class: dropdown

- {ref}`Tutorial_Normalize_Indexed_Hydrogen_Policy` — explicit policy and limits.
- {ref}`Tutorial_Get_atom_correspondences` — strict graph correspondence.
- {ref}`Tutorial_Fixed_State_Hydrogens` — independent H coordinate generation.
:::
