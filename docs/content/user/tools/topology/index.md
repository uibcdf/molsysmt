# Topology

Native `molsysmt.Topology` stores the stable atom inventory and hierarchy.
Covalent bonds belong to `molsysmt.ChemicalStates`; `molsys.topology.bonds`
accesses the selected reference state's bond table for existing workflows.
For a `molsysmt.MolSys`, `molsys.chemical_states` exposes that same collection.
`Topology` has no public `chemical_states` property; use the system's
`chemical_states` domain or convert a standalone topology to
`molsysmt.ChemicalStates` when the collection is needed.
`ChemicalStates.get_bonds(chemical_state=...)` selects a state by its positional
index. A collection with no states reports unavailable chemistry; it does not
claim that an evaluated state has zero bonds.

A partial `MolSys` without topology can still report its atom count and
chemical-state inventory through {func}`molsysmt.get`. Inspect its covalent records
directly through `molsys.chemical_states.get_bonds(chemical_state=...)`.
Topology attributes such as atom names are unavailable, and converting that
object to `molsysmt.Topology` raises an error until a topology is supplied.
Conversely, a partial `MolSys` with topology but no chemical states has
stable atom identities and hierarchy, but no covalent-bond claim. Query
`n_chemical_states` to distinguish an absent collection from a present
collection containing zero states.

For typed in-memory interchange, convert the entire collection to
`molsysmt.ChemicalStatesDict` and back:

```python
import molsysmt as msm

states = msm.ChemicalStates(n_atoms=2)
states.append_state()
columns = msm.convert(states, to_form="molsysmt.ChemicalStatesDict")
restored = msm.convert(columns, to_form="molsysmt.ChemicalStates")
assert restored.n_chemical_states == 1
```

The same conversion accepts a complete `molsysmt.Topology` or
`molsysmt.MolSys` as its source and returns an independent copy of its
chemical states. Select or extract a smaller atom domain before converting.

The dictionary preserves state order, the reference index, bond and atom
attribute dtypes, and explicit null masks. Its tables contain NumPy arrays;
they are not JSON data. An empty collection remains different from a state
whose bond table is empty.

|      |      |
| :--- | :--- |
| [Get substructure matches](get_substructure_matches.ipynb) | Matching complete chemical SMARTS with {func}`molsysmt.topology.get_substructure_matches` |
| [Get rings](get_rings.ipynb) | Perceiving a sparse covalent cycle basis |
| [Get bondgraph](get_bondgraph.ipynb) | Getting the bondgraph of a molecular system |
| [Get rigid fragments](get_rigid_fragments.md) | Partitioning complete connectivity at explicit active bonds |
| [Get rotatable bonds](get_rotatable_bonds.md) | Classifying torsion candidates with source indices and exclusion reasons |
| [Get covalent blocks](get_covalent_blocks.ipynb) | Getting the covalent blocks of a molecular system |
| [Get covalent paths](get_covalent_paths.ipynb) | Getting covalent paths between atoms in a molecular system |
| [Get dihedral quartets](get_dihedral_quartets.ipynb) | Getting the quartets of atoms defining specific dihedral angles |
| [Get sequence alignment](get_sequence_alignment.ipynb) | Aligning sequences of molecular systems |
| [Get sequence identity](get_sequence_identity.ipynb) | Computing sequence identity between aligned sequences |


```{eval-rst}
.. toctree::
   :maxdepth: 2
   :hidden:

   get_rigid_fragments.md
   get_rotatable_bonds.md
   get_rings.ipynb
   get_substructure_matches.ipynb
   get_bondgraph.ipynb
   get_covalent_blocks.ipynb
   get_covalent_paths.ipynb
   get_dihedral_quartets.ipynb
   get_sequence_alignment.ipynb
   get_sequence_identity.ipynb
```
