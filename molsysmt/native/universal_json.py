
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional, TextIO, Union
import json
import gzip
from copy import deepcopy


CompressionKind = Literal["none", "gzip"]


def _empty_universal_dict() -> Dict[str, Any]:
    """Minimal universal_json schema (more general than viewer_json)."""
    return {
        "version": "0.1",  # universal_json schema version

        # Global metadata about the system
        "metadata": {
            # Examples (to be defined by the standard):
            # "title": "",
            # "source": "",
            # "authors": [],
            # "references": [],
            # "simulation": {"temperature": ..., "pressure": ..., ...},
        },

        # Description of entities/chains/residues/atoms
        "topology": {
            # Alignable with MolSysMT semantics:
            # "entities": [...],
            # "chains": [...],
            # "residues": [...],
            # "atoms": {...}  # similar to viewer_json, potentially with more fields.
        },

        # Coordinates and trajectories (one or more collections)
        "coordinates": {
            # Example:
            # "collections": [
            #   {
            #     "label": "default",
            #     "n_atoms": ...,
            #     "estructures": [...],   # to be aligned with topology
            #   },
            # ]
        },

        # Bond information (could be in "topology" or here)
        "bonds": {
            # "sets": [
            #   {
            #     "label": "default",
            #     "indexA": [],
            #     "indexB": [],
            #     "order": [],
            #   },
            # ]
        },

        # Annotations and derived data (optional)
        "annotations": {
            # "selection_labels": {...},
            # "regions_of_interest": [...],
            # "analysis_results": {...},
        },
    }


@dataclass
class UniversalJSON:
    """General JSON-serializable container (`molsysmt.UniversalJSON`).

    - `data` is a JSON-compatible dict that may include:
        * `metadata`: unitless descriptive fields (titles, authors, etc.).
        * `topology`: per-atom fields; quantities are unitless except `formal_charge`
          (elementary charge units).
        * `bonds`: `atom_pairs` (0-based indices) and `order` (unitless).
        * `coordinates`: collections with `estructures` where `coordinates` are in nanometers,
          `time` in picoseconds, and `box` (if present) with `length_v*` in nanometers and
          `angle_v*_v*` in radians.
        * `annotations`: unitless by default (context-dependent).
    - `compressed` / `compression` control optional gzip serialization.
    - Utilities: `dumps`/`dump` to serialize, `to_dict(copy=True)` to retrieve the dict
      (deepcopy by default), and `copy()` to deep-copy the instance.
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
                    "Para escritura gzip, pase una ruta (str) o un archivo gzip.bin abierto."
                )
            json.dump(self.data, fp, indent=indent)
