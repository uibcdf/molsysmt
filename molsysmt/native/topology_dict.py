from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict


def _empty_topology_dict() -> Dict[str, Any]:
    return {
        "format": "molsysmt",
        "kind": "topology",
        "version": "0.1",
        "metadata": {},
        "atoms": [],
        "groups": [],
        "bonds": [],
        "chains": [],
        "molecules": [],
        "entities": [],
    }


@dataclass
class TopologyDict:
    """Storing a declared, serializable topology representation (`molsysmt.TopologyDict`)."""

    data: Dict[str, Any] = field(default_factory=_empty_topology_dict)

    def to_dict(self, copy: bool = True) -> Dict[str, Any]:
        """Returning the underlying serializable dictionary."""
        return deepcopy(self.data) if copy else self.data

    def copy(self) -> "TopologyDict":
        """Copying the dictionary representation deeply."""
        return deepcopy(self)
