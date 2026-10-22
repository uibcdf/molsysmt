from __future__ import annotations

import gzip
import json
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict, Literal, Optional, TextIO, Union

from molsysmt._private.argdigest import arg_digest

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
            "atom_id": [],  # List[str]
            "atom_name": [],  # List[str]
            "group_id": [],  # List[str]
            "group_name": [],  # List[str]
            "chain_id": [],  # List[str]
            "entity_id": [],  # List[str]
            "element_symbol": [],  # List[str] (e.g. "C", "N", "O")
            "formal_charge": [],  # List[int]
        },
        # Bond information (optional)
        "bonds": {
            # Atom pairs (0-based) participating in each bond
            "atom_pairs": [],  # List[List[int, int]]
            # Optional bond order (1, 2, 3, ...)
            "order": [],  # List[int] (same length as atom_pairs) or []
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
        "time": 0.0,  # float or int (optional)
        "coordinates": [],  # List[List[float]], len = n_atoms
        "box": {  # optional
            "v0": [0.0, 0.0, 0.0],  # box vector 0 (nm)
            "v1": [0.0, 0.0, 0.0],  # box vector 1 (nm)
            "v2": [0.0, 0.0, 0.0],  # box vector 2 (nm)
        },
    }


@dataclass
class ViewerJSON:
    """Storing a minimal viewer-friendly JSON payload (`molsysmt.ViewerJSON`).

    The underlying `data` dict follows the viewer schema:

    - `atoms`: per-atom columns (ids/names/group/chain/entity ids, element symbol, optional charges).
      IDs/names are strings; formal charges are integers and partial charges, when
      present, are numerical values in elementary-charge units.
      Native exports also include optional `group_index`, `chain_index` and
      `entity_index` columns to distinguish repeated labels. The native reader
      compacts represented axes in source index order. Legacy payloads without
      these columns identify groups by label within a chain, and chains/entities
      by label. They cannot distinguish separate identities with the same label.
    - `bonds`: `atom_pairs` (0-based index pairs) and optional `order`.
      Native recovery and bond queries also accept aligned legacy `indexA`/`indexB`
      columns or a wrapper containing one bond definition. Multiple `sets` are
      ambiguous for native chemistry: explicitly assign the desired set to
      `data['bonds']` on a copy before conversion or bond queries. Graphics copying
      and extraction can retain separate sets without mapping them to chemical states.
    - `structures`: list of structures with `coordinates` (nm), optional `time` (ps), and optional
      `box` with box vectors (`v0`, `v1`, `v2` in nm).

    `compression`/`compressed` control optional gzip serialization. Use `to_dict(copy=True)` to get a
    JSON-compatible dict and `copy()` for deep copies.
    """

    def __repr__(self):
        """Summarizing stored metadata without reading or rendering payloads."""
        from ._repr import size, summary

        data = vars(self).get("data") or {}
        atoms = data.get("atoms") or {}
        return summary(
            self,
            n_atoms=size(atoms.get("atom_id")),
            n_structures=size(data.get("structures")),
            compressed=vars(self).get("compressed", False),
        )

    data: Dict[str, Any] = field(default_factory=_empty_viewer_dict)

    # Compression metadata
    compressed: bool = False
    compression: CompressionKind = "none"

    # Field descriptions (for documentation/introspection)
    schema: Dict[str, str] = field(
        default_factory=lambda: {
            "version": "Schema version for viewer_json.",
            "atoms": "Dict with per-atom IDs, names, group/chain/entity indices, element and charge.",
            "bonds": "Dict with bonded atom indices and bond order.",
            "structures": "List of structures with coordinates (nm), time (ps) and optional box.",
        }
    )

    def to_dict(self, copy: bool = True) -> Dict[str, Any]:
        """Return the underlying JSON-compatible dict.

        Notes:
        - All values must be JSON types (dict, list, str, int, float, bool, None).
        """
        return deepcopy(self.data) if copy else self.data

    def __copy__(self):
        """Copying independent mutable state through the native graph protocol."""
        return self.__deepcopy__({})

    def __deepcopy__(self, memo):
        """Copying current state with the containing graph's memo."""
        from ._copy import _clone

        return _clone(self, memo)

    @arg_digest()
    def copy(self, *, skip_digestion=False) -> "ViewerJSON":
        """Copying graphics payload and compression metadata independently.

        Parameters
        ----------
        skip_digestion : bool, default=False
            Skip argument digestion only for inputs already satisfying this contract.

        Returns
        -------
        ViewerJSON
            An independent graphics wrapper retaining compression settings and schema.

        Notes
        -----
        Python copy.copy and copy.deepcopy detach mutable payload data and
        supported extension state. Copying does not render a scene, encode JSON
        or certify that the payload is JSON serializable. Plain Python dict
        values retain their ordinary copying behavior outside this wrapper.

        Examples
        --------
        >>> payload = ViewerJSON()
        >>> duplicate = payload.copy()
        >>> duplicate is payload
        False
        >>> duplicate.compressed
        False

        .. admonition:: User guide

           See :ref:`user-foundations-resident-copying` for native and payload copy contracts.

        .. versionadded:: 1.0.0
        """
        from ._copy import _copy_independently

        return _copy_independently(self, skip_digestion)

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
                from molsysmt._private.smonitor import ArgumentError

                raise ArgumentError(
                    argument="fp",
                    value=type(fp).__name__,
                    message="For gzip output, pass a file path (str) or an open gzip binary file.",
                )
            json.dump(self.data, fp, indent=indent)
