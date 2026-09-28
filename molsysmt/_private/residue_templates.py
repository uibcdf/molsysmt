"""Load exact residue templates shared by assessment and native repair."""

from __future__ import annotations

import json
from functools import lru_cache
from importlib.resources import files

import numpy as np

CURATED_MODIFIED_RESIDUES = frozenset({"MSE", "SEP"})


def _validate_modified_template(name: str, template: dict) -> None:
    """Reject incomplete or inconsistent curated chemical data."""

    atoms = template.get("atoms")
    elements = template.get("elements")
    bonds = template.get("bonds")
    orders = template.get("bond_orders")
    if template.get("name") != name or not isinstance(atoms, list):
        raise ValueError(f"Invalid {name} residue template identity")
    if not atoms or any(not isinstance(atom, str) or not atom for atom in atoms):
        raise ValueError(f"Invalid {name} residue atom names")
    if len(atoms) != len(set(atoms)):
        raise ValueError(f"Duplicate {name} residue atom names")
    if not isinstance(elements, list) or len(elements) != len(atoms):
        raise ValueError(f"Invalid {name} residue elements")
    if any(element not in {"C", "N", "O", "P", "Se"} for element in elements):
        raise ValueError(f"Unsupported {name} residue element")
    coordinates = np.asarray(template.get("coords_nm"), dtype=float)
    if coordinates.shape != (len(atoms), 3) or not np.isfinite(coordinates).all():
        raise ValueError(f"Invalid {name} residue coordinates")
    if not isinstance(bonds, list) or not isinstance(orders, list):
        raise ValueError(f"Invalid {name} residue bonds")
    if len(bonds) != len(orders):
        raise ValueError(f"Mismatched {name} residue bond orders")
    seen_bonds = set()
    for bond, order in zip(bonds, orders):
        if not isinstance(bond, list) or len(bond) != 2:
            raise ValueError(f"Invalid {name} residue bond")
        atom1, atom2 = bond
        if atom1 not in atoms or atom2 not in atoms or atom1 == atom2:
            raise ValueError(f"Invalid {name} residue bond endpoints")
        pair = frozenset(bond)
        if pair in seen_bonds or type(order) is not int or order not in {1, 2, 3}:
            raise ValueError(f"Invalid {name} residue bond order or duplicate")
        seen_bonds.add(pair)
    source = template.get("source")
    if not isinstance(source, dict) or not source.get("sha256"):
        raise ValueError(f"Missing {name} residue template provenance")


@lru_cache(maxsize=None)
def load_residue_template(group_name: str) -> dict | None:
    """Return a residue template by exact name, or None if absent."""

    if not group_name.isalnum():
        return None
    data = files("molsysmt.data.databases.residue_templates").joinpath(
        f"{group_name}.json"
    )
    try:
        template = json.loads(data.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    if group_name in CURATED_MODIFIED_RESIDUES:
        _validate_modified_template(group_name, template)
    return template
