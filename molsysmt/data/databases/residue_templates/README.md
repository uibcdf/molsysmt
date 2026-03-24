# residue_templates

3D coordinate templates for standard and common non-standard residues.
Used by `build/add_missing_heavy_atoms` with `engine='MolSysMT'` to place
new atoms geometrically without requiring an external force-field backend.

## Intended structure

Each file `{RESNAME}.json` contains:

```json
{
  "name": "ALA",
  "atoms": ["N", "CA", "C", "O", "CB"],
  "coords_nm": [[x, y, z], ...],
  "bonds": [["N", "CA"], ["CA", "C"], ...]
}
```

Coordinates are in **nanometres**, taken from the PDB Chemical Component
Dictionary (CCD) or from PDBFixer's `templates/*.pdb` files.

## Sources

- PDBFixer templates: `pdbfixer/templates/*.pdb` (ACE, ALA, ARG, ASN, ASP,
  CYS, GLN, GLU, GLY, HIS, ILE, LEU, LYS, MET, NME, PHE, PRO, SER, THR,
  TRP, TYR, VAL, A, C, G, U, DA, DC, DG, DT).
- PDB CCD: downloadable from https://files.wwpdb.org/pub/pdb/data/monomers/components.cif

## Status

**Not yet populated.**  The directory is reserved for a future
`make_residue_templates_db.py` script that will parse PDBFixer templates and
CCD definitions into the JSON format described above.
