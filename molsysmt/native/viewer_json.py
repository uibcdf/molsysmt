from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional, TextIO, Union
import json
import gzip
from copy import deepcopy

CompressionKind = Literal["none", "gzip"]

def _empty_viewer_dict() -> Dict[str, Any]:
    """Minimal viewer_json schema.

    All values must be JSON-compatible: dict, list, str, int, float, bool, None.
    """
    return {
        "version": "0.1",  # viewer_json schema version

        # Per-atom information (columnar, length = n_atoms)
        "atoms": {
            # Internal or external atom identifiers
            "atom_id": [],          # List[int] | List[str]
            "atom_name": [],        # List[str]
            "group_ig": [],         # List[int] | List[str]
            "group_name": [],       # List[str]
            "chain_id": [],         # List[str]
            "entity_id": [],        # List[int] | List[str]
            "element_symbol": [],   # List[str] (e.g. "C", "N", "O")
            "formal_charge": [],    # List[int]
        },

        # Bond information (optional)
        "bonds": {
            # Atom pairs (0-based) participating in each bond
            "atom_pairs": [],       # List[List[int, int]]
            # Optional bond order (1, 2, 3, ...)
            "order": [],            # List[int] (same length as atom_pairs) or []
        },

        # List of coordinate structures
        "estructures": [
            # Each structure is a dict with:
            # {
            #     "coordinates": [[x, y, z], ...],        # List[List[float]], len = n_atoms
            #     "time": 0.0,                           # float or int (optional)
            #     "box": {                               # optional
            #         "length_v0": float,                # |v0| (nm)
            #         "length_v1": float,                # |v1| (nm)
            #         "length_v2": float,                # |v2| (nm)
            #         "angle_v1_v2": float,              # radians
            #         "angle_v0_v2": float,              # radians
            #         "angle_v0_v1": float,              # radians
            #     },
            # }
        ],
    }


@dataclass
class ViewerJSON:
    """Minimal JSON-serializable container for visualization (`molsysmt.ViewerJSON`).

    - `data` is a JSON-compatible dict with:
        * `atoms`: columnar per-atom fields. Units: coordinates in nanometers, `formal_charge` in
          elementary charge units; IDs/names are unitless.
        * `bonds`: `atom_pairs` (0-based index pairs) and `order` (unitless).
        * `estructures`: list of structures with `coordinates` (nanometers), `time` (picoseconds),
          and optional `box` with `length_v*` (nanometers) and `angle_v*_v*` (radians).
    - `compressed` / `compression` control optional gzip serialization.
    - Utilities: `dumps`/`dump` to serialize, `to_dict(copy=True)` to retrieve the dict (deepcopy by
      default), and `copy()` to deep-copy the instance.
    """

    data: Dict[str, Any] = field(default_factory=_empty_viewer_dict)

    # Información de compresión
    compressed: bool = False
    compression: CompressionKind = "none"

    # Descripción esquemática de los campos (para documentación / introspección)
    schema: Dict[str, str] = field(default_factory=lambda: {
        "version": "Versión del esquema viewer_json.",
        "atoms": "Dict con campos columnar (por átomo): id, nombre, residuo, cadena, entidad, elemento, carga.",
        "bonds": "Dict with bonded atom indices and bond order.",
        "estructures": "List of structures with coordinates (nm), time (ps) and optional box.",
    })

    def to_dict(self, copy: bool = True) -> Dict[str, Any]:
        """Return the underlying JSON-compatible dict.

        Notes:
        - All values must be JSON types (dict, list, str, int, float, bool, None).
        """
        return deepcopy(self.data) if copy else self.data

    def copy(self) -> "ViewerJSON":
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
