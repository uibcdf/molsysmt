# residue_templates

3D coordinate templates for standard residues and capping groups.
Used by `build/add_missing_heavy_atoms` with `engine='MolSysMT'` to place
new atoms geometrically without requiring an external force-field backend.

## Contents

One JSON file per residue:

| Set | Residues |
|-----|----------|
| Standard amino acids | ALA, ARG, ASN, ASP, CYS, GLN, GLU, GLY, HIS, ILE, LEU, LYS, MET, PHE, PRO, SER, THR, TRP, TYR, VAL |
| Capping groups | ACE, NME |
| RNA nucleotides | A, C, G, U |
| DNA nucleotides | DA, DC, DG, DT |

## JSON format

```json
{
  "name": "ALA",
  "atoms": ["N", "CA", "C", "O", "CB"],
  "coords_nm": [[-0.1444, -0.0596, 0.0968], ...],
  "bonds": [["N", "CA"], ["CA", "C"], ...]
}
```

- **atoms**: heavy (non-hydrogen) atoms only, in PDBFixer template order.
- **coords_nm**: Cartesian coordinates in **nanometres**.
  Converted from PDBFixer templates (Angstroms) by dividing by 10.
- **bonds**: bonds between heavy atoms only.  Sourced from
  `data/databases/amino_acids/*.pkl.gz` (amino acids),
  `data/databases/terminal_cappings/c_terminal.json` (ACE),
  `data/databases/terminal_cappings/n_terminal.json` (NME).
  RNA/DNA nucleotides have empty bond lists (no MolSysMT database yet).

## Sources

- 3D coordinates: PDBFixer templates at `pdbfixer/pdbfixer/templates/*.pdb`
  (Angstroms, heavy atoms only; no explicit bonds in source files).
- Bond connectivity: MolSysMT amino-acid topology database
  (`data/databases/amino_acids/`) and terminal-capping database
  (`data/databases/terminal_cappings/`).

## Generation

Run from the repository root to regenerate all JSON files:

```bash
python molsysmt/data/databases/residue_templates/make_residue_templates_db.py
```

Requires PDBFixer source available at `~/repos@others/pdbfixer`.
