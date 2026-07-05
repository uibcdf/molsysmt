"""Hydrogen-bond adapters for MolSysMT analyses rendered in MolSysViewer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..access import has_system


@dataclass(frozen=True)
class HBondLinks:
    """Hydrogen-bond donor/acceptor pairs ready for viewer link rendering."""

    structures: list[list[list[int]] | None]
    method: str = "buch"

    @property
    def n_hbonds(self) -> int:
        return sum(len(item) for item in self.structures if item is not None)


def buch_hbond_links(view: Any) -> HBondLinks:
    """Return Buch hydrogen bonds as per-structure donor/acceptor atom pairs."""
    if not has_system(view):
        raise ValueError("No molecular system attached.")

    import numpy as np
    import molsysmt as msm

    atoms_per_structure, _distances = msm.hbonds.get_buch_hbonds(view)
    structures: list[list[list[int]] | None] = []
    for frame_atoms in atoms_per_structure:
        if frame_atoms is None or len(frame_atoms) == 0:
            structures.append(None)
            continue
        arr = np.asarray(frame_atoms)
        structures.append([[int(arr[i, 0]), int(arr[i, 2])] for i in range(len(arr))])

    return HBondLinks(structures=structures)
