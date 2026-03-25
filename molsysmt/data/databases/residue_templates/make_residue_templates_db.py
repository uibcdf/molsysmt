"""
make_residue_templates_db.py
============================
Parse PDBFixer template PDB files and generate per-residue JSON coordinate
templates for ``data/databases/residue_templates/``.

Only heavy atoms are written; hydrogen names are identified by PDB convention
(starts with 'H', or digit followed by 'H').

Coordinates are converted from Angstroms (PDBFixer) to nanometres (MolSysMT
convention): coords_nm = coords_angstrom / 10.0

Bond connectivity is sourced from:
  - Standard amino acids (ALA–VAL): molsysmt.data.databases.amino_acids
  - ACE: data/databases/terminal_cappings/c_terminal.json
  - NME: data/databases/terminal_cappings/n_terminal.json
  - RNA/DNA nucleotides (A, C, G, U, DA, DC, DG, DT): bonds left empty (no
    MolSysMT database for these yet; they can be added later from CCD data).

Usage
-----
Run from the repository root::

    python molsysmt/data/databases/residue_templates/make_residue_templates_db.py

Output: one JSON file per residue in the same directory.

JSON format
-----------
{
  "name": "ALA",
  "atoms": ["N", "CA", "C", "O", "CB"],
  "coords_nm": [[-0.1444, -0.0596, 0.0968], ...],
  "bonds": [["N", "CA"], ["CA", "C"], ...]
}
"""

from __future__ import annotations

import json
import os
import pickle
import gzip
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

TEMPLATES_DIR = Path("/home/diego/repos@others/pdbfixer/pdbfixer/templates")
OUTPUT_DIR = Path(__file__).parent
REPO_ROOT = Path(__file__).parents[4]  # molsysmt/

sys.path.insert(0, str(REPO_ROOT))

AA_DB_DIR = REPO_ROOT / "molsysmt" / "data" / "databases" / "amino_acids"
TERMINAL_DB_DIR = REPO_ROOT / "molsysmt" / "data" / "databases" / "terminal_cappings"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_hydrogen(name: str) -> bool:
    if not name:
        return False
    if name[0] == "H":
        return True
    if len(name) >= 2 and name[0].isdigit() and name[1] == "H":
        return True
    return False


def parse_pdb_template(pdb_path: Path) -> tuple[list[str], list[list[float]]]:
    """Return (atom_names, coords_nm) for heavy atoms only."""
    atoms: list[str] = []
    coords: list[list[float]] = []
    with open(pdb_path) as fh:
        for line in fh:
            if not line.startswith("ATOM"):
                continue
            atom_name = line[12:16].strip()
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            if _is_hydrogen(atom_name):
                continue
            atoms.append(atom_name)
            # Angstroms → nm
            coords.append([round(x / 10.0, 6), round(y / 10.0, 6), round(z / 10.0, 6)])
    return atoms, coords


def get_aa_bonds_heavy(resname: str, heavy_atoms: list[str]) -> list[list[str]]:
    """Return bonds between heavy atoms from the amino_acids database."""
    pkl_file = AA_DB_DIR / (resname[0] + ".pkl.gz")
    with gzip.open(pkl_file, "rb") as fh:
        dbs = pickle.load(fh)
    if resname not in dbs:
        return []
    topo = dbs[resname].get("topology", [])
    if not topo:
        return []
    # Use variant 0 (CCD canonical); filter to heavy-atom bonds only.
    heavy_set = set(heavy_atoms)
    bonds = []
    for bond in topo[0].get("bonds", []):
        a, b = bond[0], bond[1]
        if a in heavy_set and b in heavy_set:
            bonds.append([a, b])
    return bonds


def get_terminal_bonds_heavy(resname: str, json_path: Path, heavy_atoms: list[str]) -> list[list[str]]:
    """Return bonds between heavy atoms from a terminal_cappings JSON file."""
    with open(json_path) as fh:
        db = json.load(fh)
    if resname not in db:
        return []
    topo = db[resname].get("topology", [])
    if not topo:
        return []
    heavy_set = set(heavy_atoms)
    bonds = []
    for bond in topo[0].get("bonds", []):
        a, b = bond[0], bond[1]
        if a in heavy_set and b in heavy_set:
            bonds.append([a, b])
    return bonds


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

AMINO_ACIDS_3L = {
    "ALA", "ARG", "ASN", "ASP", "CYS",
    "GLN", "GLU", "GLY", "HIS", "ILE",
    "LEU", "LYS", "MET", "PHE", "PRO",
    "SER", "THR", "TRP", "TYR", "VAL",
}

NUCLEOTIDES = {"A", "C", "G", "U", "DA", "DC", "DG", "DT"}


def main() -> None:
    pdb_files = sorted(TEMPLATES_DIR.glob("*.pdb"))
    if not pdb_files:
        print(f"No PDB files found in {TEMPLATES_DIR}")
        return

    for pdb_file in pdb_files:
        resname = pdb_file.stem
        atoms, coords_nm = parse_pdb_template(pdb_file)

        if not atoms:
            print(f"  {resname}: no heavy atoms found — skipping")
            continue

        # --- bonds ----------------------------------------------------------
        if resname in AMINO_ACIDS_3L:
            bonds = get_aa_bonds_heavy(resname, atoms)
        elif resname == "ACE":
            bonds = get_terminal_bonds_heavy(
                "ACE", TERMINAL_DB_DIR / "c_terminal.json", atoms
            )
        elif resname == "NME":
            # PDBFixer uses 'C' for the methyl carbon; database uses 'CH3'.
            # Fall back to the only meaningful heavy bond: N-C.
            heavy_set = set(atoms)
            if "N" in heavy_set and "C" in heavy_set:
                bonds = [["N", "C"]]
            else:
                bonds = get_terminal_bonds_heavy(
                    "NME", TERMINAL_DB_DIR / "n_terminal.json", atoms
                )
        elif resname in NUCLEOTIDES:
            # No bond source yet; leave empty.
            bonds = []
        else:
            bonds = []

        template = {
            "name": resname,
            "atoms": atoms,
            "coords_nm": coords_nm,
            "bonds": bonds,
        }

        out_path = OUTPUT_DIR / f"{resname}.json"
        with open(out_path, "w") as fh:
            json.dump(template, fh, indent=2)
        print(f"  {resname}: {len(atoms)} heavy atoms, {len(bonds)} bonds → {out_path.name}")

    print(f"\nDone. {len(pdb_files)} templates written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
