# Group

The `group` level in MolSysMT encompasses residues, solvent molecules, ions, and functional building blocks. In addition to general query helpers, specialized submodules provide domain-specific operations for amino acids, ions, water, lipids, nucleotides, saccharides, small molecules, and terminal cappings.

## General Group Operations

|      |      |
| :--- | :--- |
| [Get group type](get_group_type.ipynb) | Querying group classifications in molecular systems |
| [Get group type from group name](get_group_type_from_group_name.ipynb) | Inferring group type from residue name strings |
| [Get bonded atom pairs](get_bonded_atom_pairs.ipynb) | Extracting standard covalent bond pairs for residues |
| [Is group type](is_group_type.ipynb) | Validating recognized group classifications |

## Specialized Group Submodules

|      |      |
| :--- | :--- |
| [Amino Acid](amino_acid/index.md) | Dedicated tools for amino acid residues and 1-letter translations |
| [Ion](ion/index.md) | Identification and database queries for ion species |
| [Water](water/index.md) | Validation of standard solvent and water models |
| [Terminal Capping](terminal_capping/index.md) | Operations for N-terminal and C-terminal capping groups |
| [Small Molecule](small_molecule/index.md) | Validation of ligands and small molecule entities |
| [Nucleotide](nucleotide/index.md) | Identification of DNA and RNA nucleotide residues |
| [Lipid](lipid/index.md) | Validation of membrane lipids |
| [Saccharide](saccharide/index.md) | Identification of carbohydrate and saccharide units |

```{eval-rst}
.. toctree::
   :maxdepth: 2
   :hidden:

   get_group_type.ipynb
   get_group_type_from_group_name.ipynb
   get_bonded_atom_pairs.ipynb
   is_group_type.ipynb
   amino_acid/index.md
   ion/index.md
   water/index.md
   terminal_capping/index.md
   small_molecule/index.md
   nucleotide/index.md
   lipid/index.md
   saccharide/index.md
```
