# Build

For explicit topology construction, use `molsysmt.MolSysBuilder`. Declare atoms
and groups first, add bonds with optional metadata such as
`builder.add_bond(atom_0, atom_1, bond_order=2, bond_type="covalent")`, assign
coordinates with `set_coordinates()`, and call `build()` to materialize a native
system. Before materialization, `molsysmt.get(builder, ...)` reads the complete
declared attribute union of the builder's chemical/topological and structural
components. A builder does not store molecular-mechanics attributes or
per-structure chemical-state associations. The four course paths include
complete builder examples.

Conversions among `molsysmt.MolSys`, `molsysmt.MolSysBuilder`, and
`molsysmt.MolSysDict` provide exhaustive fidelity reports. The reduced
dictionary conversion canonicalizes atom selections, preserves the requested
`structure_indices` order, and rejects detected loss when `strict=True`.

`bond_order` is the formal numeric order; `bond_type` describes the chemical
relationship and accepts `covalent`, `dative`, or explicitly `unknown`.
Aromaticity, fractional order, and force-field parameter classes are distinct
concepts and are not encoded as arbitrary `bond_type` labels.


|      |      |
| :--- | :--- |
| [Add bonds](add_bonds.ipynb) | Adding new covalent bonds between atoms in a molecular system |
| [Add missing bonds](add_missing_bonds.ipynb) | Adding the missing bonds in a molecular system |
| [Add missing heavy atoms](add_missing_heavy_atoms.ipynb) | Adding the missing heavy atoms in a molecular system |
| [Add missing hydrogens](add_missing_hydrogens.ipynb) | Adding the missing hydrogen atoms in a molecular system |
| [Add missing terminal_cappings](add_missing_terminal_cappings.ipynb) | Adding the missing terminal cappings in a molecular system |
| [Build peptide](build_peptide.ipynb) | Building a peptide |
| [Define new chain](define_new_chain.ipynb) | Define a new chain with new id and name attributes|
| [Get disulfide bonds](get_disulfide_bonds.ipynb) | Getting the disulfide bonds of a molecular system |
| [Get missing bonds](get_missing_bonds.ipynb) | Getting the missing bonds of a molecular system |
| [Get missing heavy_atoms](get_missing_heavy_atoms.ipynb) | Getting the missing heavy atoms of a molecular system |
| [Get missing residues](get_missing_residues.ipynb) | Getting the missing residues of a molecular system |
| [Get missing terminal_cappings](get_missing_terminal_cappings.ipynb) | Getting the missing terminal cappings of a molecular system |
| [Get non standard residues](get_non_standard_residues.ipynb) | Getting the non standard residues of a molecular system |
| [Has hydrogens](has_hydrogens.ipynb) | Checking if a molecular system has hydrogen atoms |
| [Is solvated](is_solvated.ipynb) | Checking if a molecular system is solvated |
| [Make bioassembly](make_bioassembly.ipynb) | Making a bioassembly of a molecular system |
| [Make water box](make_water_box.ipynb) | Making a water box system |
| [Mutate](mutate.ipynb) | Mutating residues in a molecular system |
| [Remove overlapping molecules](remove_overlapping_molecules.ipynb) | Removing overlapping molecules in a molecular system |
| [Solvate](solvate.ipynb) | Solvating of a molecular system |
| [Solve atoms with alternate location](solve_atoms_with_alternate_locations.ipynb) | Solving the coordinates of atoms with alternate locations in a molecular system |


```{eval-rst}
.. toctree::
   :maxdepth: 2
   :hidden:

   add_bonds.ipynb
   add_missing_bonds.ipynb
   add_missing_heavy_atoms.ipynb
   add_missing_hydrogens.ipynb
   add_missing_terminal_cappings.ipynb
   build_peptide.ipynb
   define_new_chain.ipynb
   get_disulfide_bonds.ipynb
   get_missing_bonds.ipynb
   get_missing_heavy_atoms.ipynb
   get_missing_residues.ipynb
   get_missing_terminal_cappings.ipynb
   get_non_standard_residues.ipynb
   has_hydrogens.ipynb
   is_solvated.ipynb
   make_bioassembly.ipynb
   make_water_box.ipynb
   mutate.ipynb
   remove_overlapping_molecules.ipynb
   solvate.ipynb
   solve_atoms_with_alternate_locations.ipynb
```
