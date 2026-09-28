"""Generate curated templates from pinned, whitespace-normalized CCD files."""

from __future__ import annotations

import hashlib
import json
import shlex
from pathlib import Path

SOURCE_DIR = Path(__file__).parent / "ccd_components"
OUTPUT_DIR = Path(__file__).parent.parent / "databases" / "residue_templates"
SOURCES = {
    "MSE": "945a8ad89ba50417ca70b30c749470710a5dcc5203295a73b4b9e7e041077470",
    "SEP": "a99dd6ecccf72cd3d04afd6bbfa066375e2e09434ee0b641ce36625de23de296",
}
UPSTREAM_SHA256 = {
    "MSE": "2f8373207105fd6e18aa25ec22cfb229987da61cc79a3980e64d7ee31fb4d31c",
    "SEP": "8a64575a99938ed0960684067183d8b7a85daabb204fda3c13c24fa9353e86a9",
}
ORDERS = {"SING": 1, "DOUB": 2, "TRIP": 3}


def _loop_rows(text: str, category: str) -> list[dict[str, str]]:
    """Read one flat CIF loop whose records occupy one line each."""

    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != "loop_":
            continue
        headers = []
        position = index + 1
        while position < len(lines) and lines[position].startswith("_"):
            headers.append(lines[position].strip())
            position += 1
        if not headers or not headers[0].startswith(category + "."):
            continue

        rows = []
        while position < len(lines):
            row = lines[position].strip()
            if not row or row == "#":
                break
            fields = shlex.split(row)
            if len(fields) != len(headers):
                raise ValueError(f"Malformed {category} row: {row}")
            rows.append(dict(zip(headers, fields)))
            position += 1
        return rows
    raise ValueError(f"Missing {category} loop")


def generate_template(name: str) -> dict:
    """Extract one residue's heavy atoms, ideal geometry, and covalent bonds."""

    source_path = SOURCE_DIR / f"{name}.cif"
    source_bytes = source_path.read_bytes()
    digest = hashlib.sha256(source_bytes).hexdigest()
    if digest != SOURCES[name]:
        raise ValueError(f"The pinned {name} CCD file changed: {digest}")
    source_text = source_bytes.decode("utf-8")

    atoms = []
    elements = []
    coords_nm = []
    for row in _loop_rows(source_text, "_chem_comp_atom"):
        if row["_chem_comp_atom.comp_id"] != name:
            raise ValueError(f"Unexpected component in {name} atom table")
        symbol = row["_chem_comp_atom.type_symbol"].capitalize()
        if symbol == "H":
            continue
        atoms.append(row["_chem_comp_atom.atom_id"])
        elements.append(symbol)
        coords_nm.append(
            [
                round(
                    float(row[f"_chem_comp_atom.pdbx_model_Cartn_{axis}_ideal"]) / 10, 6
                )
                for axis in "xyz"
            ]
        )

    heavy_names = set(atoms)
    bonds = []
    bond_orders = []
    for row in _loop_rows(source_text, "_chem_comp_bond"):
        if row["_chem_comp_bond.comp_id"] != name:
            raise ValueError(f"Unexpected component in {name} bond table")
        pair = [row["_chem_comp_bond.atom_id_1"], row["_chem_comp_bond.atom_id_2"]]
        if not all(atom in heavy_names for atom in pair):
            continue
        bonds.append(pair)
        bond_orders.append(ORDERS[row["_chem_comp_bond.value_order"]])

    return {
        "name": name,
        "atoms": atoms,
        "elements": elements,
        "coords_nm": coords_nm,
        "bonds": bonds,
        "bond_orders": bond_orders,
        "source": {
            "url": f"https://files.rcsb.org/ligands/view/{name}.cif",
            "sha256": digest,
            "upstream_sha256": UPSTREAM_SHA256[name],
        },
    }


def main() -> None:
    for name in SOURCES:
        output = OUTPUT_DIR / f"{name}.json"
        output.write_text(json.dumps(generate_template(name), indent=2) + "\n")
        print(f"Wrote {output}")


if __name__ == "__main__":
    main()
