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
            "atom_id": [],          # List[str]
            "atom_name": [],        # List[str]
            "group_id": [],         # List[str]
            "group_name": [],       # List[str]
            "chain_id": [],         # List[str]
            "entity_id": [],        # List[str]
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
        "structures": [
            # Each structure is a dict with:
            # {
            #     "coordinates": [[x, y, z], ...],        # List[List[float]], len = n_atoms
            #     "time": 0.0,                           # float or int (optional)
            #     "box": {                               # optional
            #         "v0": [float, float, float],       # box vector 0 (nm)
            #         "v1": [float, float, float],       # box vector 1 (nm)
            #         "v2": [float, float, float],       # box vector 2 (nm)
            #     },
            # }
        ],
    }

def _empty_structure_viewer_dict() -> Dict[str, Any]:
    """Minimal structure_viewer_json schema.

    All values must be JSON-compatible: dict, list, str, int, float, bool, None.
    """
    return {

        "time": 0.0,    # float or int (optional)
        "coordinates": [], # List[List[float]], len = n_atoms
        "box": {                               # optional
                "v0": [0.0, 0.0, 0.0],         # box vector 0 (nm)
                "v1": [0.0, 0.0, 0.0],         # box vector 1 (nm)
                "v2": [0.0, 0.0, 0.0],         # box vector 2 (nm)
               },
    }



@dataclass
class ViewerJSON:
    """Storing a minimal viewer-friendly JSON payload (`molsysmt.ViewerJSON`).

    The underlying `data` dict follows the viewer schema:

    - `atoms`: per-atom columns (ids/names/group/chain/entity ids, element symbol, optional charges).
      All ids/names are strings; charges are unitless integers.
    - `bonds`: `atom_pairs` (0-based index pairs) and optional `order`.
    - `structures`: list of structures with `coordinates` (nm), optional `time` (ps), and optional
      `box` with box vectors (`v0`, `v1`, `v2` in nm).

    `compression`/`compressed` control optional gzip serialization. Use `to_dict(copy=True)` to get a
    JSON-compatible dict and `copy()` for deep copies.
    """

    data: Dict[str, Any] = field(default_factory=_empty_viewer_dict)

    # Compression metadata
    compressed: bool = False
    compression: CompressionKind = "none"

    # Field descriptions (for documentation/introspection)
    schema: Dict[str, str] = field(default_factory=lambda: {
        "version": "Schema version for viewer_json.",
        "atoms": "Dict with per-atom columns: ids, names, residue, chain, entity, element, charge.",
        "bonds": "Dict with bonded atom indices and bond order.",
        "structures": "List of structures with coordinates (nm), time (ps) and optional box.",
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
