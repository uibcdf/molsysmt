from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict


def _empty_molsys_dict() -> Dict[str, Any]:
    return {
        "format": "molsysmt",
        "kind": "molsys",
        "version": "0.1",
        "metadata": {},
        "topology": {
            "atoms": [],
            "groups": [],
            "bonds": [],
            "chains": [],
            "molecules": [],
            "entities": [],
        },
        "structures": {
            "structure_id": None,
            "time": None,
            "box": None,
            "coordinates": None,
        },
    }


@dataclass
class MolSysDict:
    """Storing a declared, serializable molecular system representation (`molsysmt.MolSysDict`)."""

    data: Dict[str, Any] = field(default_factory=_empty_molsys_dict)

    def to_dict(self, copy: bool = True) -> Dict[str, Any]:
        """Returning the underlying serializable dictionary."""
        return deepcopy(self.data) if copy else self.data

    def copy(self) -> "MolSysDict":
        """Copying the dictionary representation deeply."""
        return deepcopy(self)
