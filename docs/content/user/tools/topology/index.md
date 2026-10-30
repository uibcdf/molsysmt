# Topology

`molsysmt.topology` provides sequence comparison over stable represented groups.
Native `Topology` owns atoms, groups, molecules, entities and chains. It has no
bonds, components or chemical-state facade, even while attached to MolSys.

For selected-state graphs, covalent components, rings, torsion definitions and
chemical correspondence, use the [Chemical States tools](../chemical_states/index.md).
See {ref}`Topology <user-foundations-native-world-classes-molsysmt-topology>` for
stable membership and {ref}`ChemicalStates <user-foundations-native-world-classes-molsysmt-chemicalstates>`
for independent chemical storage.

| Tool | Purpose |
| :--- | :--- |
| [Get sequence alignment](get_sequence_alignment.ipynb) | Aligning represented amino-acid sequences while retaining source group indices. |
| [Get sequence identity](get_sequence_identity.ipynb) | Computing identity between aligned sequences. |

```{toctree}
:maxdepth: 2
:hidden:

get_sequence_alignment
get_sequence_identity
```
