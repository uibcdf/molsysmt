
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional, TextIO, Union
import json
import gzip
from copy import deepcopy


CompressionKind = Literal["none", "gzip"]


def _empty_atoms_dict() -> Dict[str, Any]:
    """Default atom-level fields."""
    return {
        "atom_id": [],
        "atom_name": [],
        "group_id": [],
        "group_name": [],
        "chain_id": [],
        "entity_id": [],
        "element_symbol": [],
        "formal_charge": [],
    }


def _empty_bonds_dict() -> Dict[str, Any]:
    """Default bonds block."""
    return {
        "atom_pairs": [],
        "order": [],
    }


def _empty_structure_dict() -> Dict[str, Any]:
    """Default structure entry aligned with topology."""
    return {
        "coordinates": [],
        "time": None,
        "box": {
            "length_v0": None,
            "length_v1": None,
            "length_v2": None,
            "angle_v1_v2": None,
            "angle_v0_v2": None,
            "angle_v0_v1": None,
        },
    }


def _empty_coordinates_collection(label: str = "default") -> Dict[str, Any]:
    """Default coordinates collection with structures aligned to topology."""
    return {
        "label": label,
        "structures": [],
    }


def _empty_universal_dict() -> Dict[str, Any]:
    """Minimal universal_json schema (more general than viewer_json)."""
    return {
        "version": "0.1",  # universal_json schema version
        "metadata": {},
        "topology": {
            "atoms": _empty_atoms_dict(),
        },
        "coordinates": {
            "collections": [_empty_coordinates_collection()],
        },
        "bonds": _empty_bonds_dict(),
        "annotations": {},
    }


@dataclass
class UniversalJSON:
    """Storing a general JSON representation of a molecular system (`molsysmt.UniversalJSON`).

    The `data` dict follows a broad schema:
    - `metadata`: unitless descriptive fields.
    - `topology`: per-atom columns (ids, names, group/chain/entity ids, element symbols, charges).
    - `bonds`: `atom_pairs` (0-based) plus optional `order`.
    - `coordinates`: collections with `structures`, each holding `coordinates` (nm), optional `time`
      (ps), and optional `box` (lengths in nm, angles in radians).
    - `annotations`: optional derived data.

    `compression`/`compressed` control optional gzip serialization. Use `to_dict(copy=True)` for a
    JSON-compatible dict and `copy()` for deep copies.
    """

    data: Dict[str, Any] = field(default_factory=_empty_universal_dict)

    # Compression info
    compressed: bool = False
    compression: CompressionKind = "none"

    # Field descriptions (for documentation / introspection)
    schema: Dict[str, str] = field(default_factory=lambda: {
        "version": "Universal_json schema version.",
        "metadata": "Global system metadata (sources, references, simulation data, etc.).",
        "topology": "Structural description (entities, chains, residues, atoms).",
        "coordinates": "Coordinate collections and trajectories aligned with topology.",
        "bonds": "Chemical bond information, potentially multiple sets.",
        "annotations": "Annotations and derived data (selections, analysis, regions of interest).",
    })

    def to_dict(self, copy: bool = True) -> Dict[str, Any]:
        """Return the underlying JSON-compatible dict."""
        return deepcopy(self.data) if copy else self.data

    def copy(self) -> "UniversalJSON":
        """Return a deep copy of the instance."""
        return deepcopy(self)

    # --- Serialización JSON ---

    def dumps(self, indent: Optional[int] = None) -> str:
        """Return a JSON text representation."""
        return json.dumps(self.data, indent=indent)

    def dump(
        self,
        fp: Union[str, TextIO],
        *,
        indent: Optional[int] = None,
        compression: Optional[CompressionKind] = None,
    ) -> None:
        """Write content to a file path or file-like as JSON (optionally gzipped)."""
        compression = compression or self.compression

        if isinstance(fp, str):
            if compression == "gzip":
                with gzip.open(fp, "wt", encoding="utf-8") as f:
                    json.dump(self.data, f, indent=indent)
            else:
                with open(fp, "w", encoding="utf-8") as f:
                    json.dump(self.data, f, indent=indent)
        else:
            if compression == "gzip":
                raise ValueError(
                    "For gzip output, pass a file path (str) or an open gzip binary file."
                )
            json.dump(self.data, fp, indent=indent)
