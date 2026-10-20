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

    def __repr__(self):
        """Summarizing stored metadata without reading or rendering payloads."""
        from ._repr import size, summary

        data = vars(self).get("data") or {}
        return summary(
            self,
            n_atoms=size(data.get("atoms")),
            n_groups=size(data.get("groups")),
            n_bonds=size(data.get("bonds")),
        )

    data: Dict[str, Any] = field(default_factory=_empty_topology_dict)

    def to_dict(self, copy: bool = True) -> Dict[str, Any]:
        """Returning the underlying serializable dictionary."""
        return deepcopy(self.data) if copy else self.data

    def copy(self) -> "TopologyDict":
        """Copying the dictionary representation deeply."""
        return deepcopy(self)
