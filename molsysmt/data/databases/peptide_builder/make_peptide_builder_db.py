"""Build peptide-builder templates from AmberClassic LEaP library files."""

from __future__ import annotations

import argparse
import gzip
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple


ENTRY_RE = re.compile(r"!entry\.([A-Za-z0-9_]+)\.unit\.")


def _collect_entry_names(text: str) -> List[str]:
    names = set()
    for match in ENTRY_RE.finditer(text):
        names.add(match.group(1))
    return sorted(names)


def _extract_block(text: str, marker: str) -> List[str]:
    index = text.find(marker)
    if index < 0:
        return []
    lines = text[index:].splitlines()[1:]
    output = []
    for line in lines:
        if line.startswith("!entry."):
            break
        stripped = line.strip()
        if stripped:
            output.append(stripped)
    return output


def _parse_atoms(lines: List[str]) -> Tuple[List[str], List[str], List[int], List[float]]:
    atom_names = []
    atom_types = []
    atom_elements = []
    atom_charges = []
    for line in lines:
        tokens = line.split()
        atom_names.append(tokens[0].strip('"'))
        atom_types.append(tokens[1].strip('"'))
        atom_elements.append(int(tokens[6]))
        atom_charges.append(float(tokens[7]))
    return atom_names, atom_types, atom_elements, atom_charges


def _parse_positions(lines: List[str]) -> List[List[float]]:
    coordinates = []
    for line in lines:
        x_str, y_str, z_str = line.split()[:3]
        # LEaP libraries store coordinates in angstrom.
        coordinates.append([float(x_str) / 10.0, float(y_str) / 10.0, float(z_str) / 10.0])
    return coordinates


def _parse_connect(lines: List[str]) -> List[int | None]:
    if len(lines) < 2:
        return [None, None]
    first = int(lines[0])
    second = int(lines[1])
    return [first - 1 if first > 0 else None, second - 1 if second > 0 else None]


def _parse_connectivity(lines: List[str]) -> List[List[int]]:
    bonds = []
    for line in lines:
        atom1_str, atom2_str = line.split()[:2]
        atom1 = int(atom1_str) - 1
        atom2 = int(atom2_str) - 1
        if atom1 < atom2:
            bonds.append([atom1, atom2])
        else:
            bonds.append([atom2, atom1])
    bonds.sort()
    return bonds


def _parse_library(path: Path) -> Dict[str, dict]:
    text = path.read_text(errors="ignore")
    output: Dict[str, dict] = {}
    for name in _collect_entry_names(text):
        atoms_lines = _extract_block(text, f"!entry.{name}.unit.atoms table")
        positions_lines = _extract_block(text, f"!entry.{name}.unit.positions table")
        connect_lines = _extract_block(text, f"!entry.{name}.unit.connect array")
        connectivity_lines = _extract_block(text, f"!entry.{name}.unit.connectivity table")
        residueconnect_lines = _extract_block(text, f"!entry.{name}.unit.residueconnect table")

        if not atoms_lines or not positions_lines or not connectivity_lines:
            continue

        atom_names, atom_types, atom_elements, atom_charges = _parse_atoms(atoms_lines)
        coordinates_nm = _parse_positions(positions_lines)
        connect = _parse_connect(connect_lines)
        residueconnect = _parse_connect(residueconnect_lines)
        bonds = _parse_connectivity(connectivity_lines)

        if len(atom_names) != len(coordinates_nm):
            continue

        output[name] = {
            "atom_names": atom_names,
            "atom_types": atom_types,
            "atom_elements": atom_elements,
            "atom_charges": atom_charges,
            "coordinates_nm": coordinates_nm,
            "bonds": bonds,
            "connect": connect,
            "residueconnect": residueconnect,
        }

    return output


def build_database(amberclassic_root: Path) -> dict:
    library_paths = [
        amberclassic_root / "dat" / "leap" / "lib" / "amino12.lib",
        amberclassic_root / "dat" / "leap" / "lib" / "aminont12.lib",
        amberclassic_root / "dat" / "leap" / "lib" / "aminoct12.lib",
    ]

    templates: Dict[str, dict] = {}
    for path in library_paths:
        if not path.exists():
            raise FileNotFoundError(f"Required LEaP library not found: {path}")
        templates.update(_parse_library(path))

    return {
        "database_name": "peptide_builder",
        "forcefield": "amber14sb",
        "source": "AmberClassic LEaP libraries (amino12, aminont12, aminoct12)",
        "templates": templates,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate peptide_builder template database.")
    parser.add_argument(
        "--amberclassic-root",
        default="../AmberClassic",
        help="Path to local AmberClassic repository root.",
    )
    parser.add_argument(
        "--output",
        default="amber14sb.json.gz",
        help="Output filename inside peptide_builder directory.",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    amberclassic_root = (script_dir / args.amberclassic_root).resolve()
    output_path = script_dir / args.output

    database = build_database(amberclassic_root)
    with gzip.open(output_path, "wt", encoding="utf-8") as file_handle:
        json.dump(database, file_handle, indent=2, sort_keys=True)

    print(f"Wrote {output_path} with {len(database['templates'])} templates.")


if __name__ == "__main__":
    main()
