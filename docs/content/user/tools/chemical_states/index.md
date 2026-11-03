# Chemical States

`molsysmt.chemical_states` provides form-agnostic tools over a selected stored
chemical graph. Bonds, atom assignments and state-local components belong to
`molsysmt.ChemicalStates`; stable inventory belongs to Topology. A complete MolSys
combines those domains without storing the same chemistry twice.

`chemical_state` selects a positional state or the unambiguous reference.
`chemical_state='structure'` requires compatible explicit or admitted implicit
associations for the requested structures. Selecting a state never changes the
reference. A missing domain, a present collection with zero states, unknown
connectivity and a complete graph without edges remain different conditions.
Tools needing atom names, groups or coordinates require that context explicitly;
state-only graph operations do not create fake topology or coordinates.

| Tool | Purpose |
| :--- | :--- |
| [Get bondgraph](get_bondgraph.ipynb) | Querying stored induced connectivity and source atom indices. |
| [Get covalent blocks](get_covalent_blocks.ipynb) | Partitioning the stored graph with explicit cuts. |
| [Get covalent paths](get_covalent_paths.ipynb) | Finding walks matching an ordered atom pattern. |
| [Get dihedral quartets](get_dihedral_quartets.ipynb) | Recognizing standard torsion-defining atom quartets. |
| [Get rings](get_rings.ipynb) | Perceiving a sparse covalent cycle basis. |
| [Get rotatable bonds](get_rotatable_bonds.md) | Classifying torsion candidates and explicit exclusion reasons. |
| [Get rigid fragments](get_rigid_fragments.md) | Partitioning connectivity at declared active cuts. |
| [Get substructure matches](get_substructure_matches.ipynb) | Matching complete chemical SMARTS with declared prerequisites. |
| [Get atom correspondences](get_atom_correspondences.ipynb) | Comparing declared chemical graphs independently of Cartesian alignment. |

For typed in-memory interchange, convert a collection to ChemicalStatesDict:

```python
import molsysmt as msm

states = msm.ChemicalStates(n_atoms=2)
states.append_state()
columns = msm.convert(states, to_form='molsysmt.ChemicalStatesDict')
restored = msm.convert(columns, to_form='molsysmt.ChemicalStates')
assert restored.n_chemical_states == 1
```

MolSys can supply its independent collection; pure Topology cannot. Standalone
ChemicalStatesDict preserves typed NumPy columns, null masks, state order and
history. MolSysDict 0.2 adds JSON-safe typed transport; H5MSM 0.5 remains the
numeric storage route. See
{ref}`ChemicalStates <user-foundations-native-world-classes-molsysmt-chemicalstates>`
and {ref}`MolSysDict <user-foundations-native-world-classes-molsysmt-molsysdict>`.

```{toctree}
:maxdepth: 2
:hidden:

get_bondgraph
get_covalent_blocks
get_covalent_paths
get_dihedral_quartets
get_rings
get_rotatable_bonds
get_rigid_fragments
get_substructure_matches
get_atom_correspondences
```
