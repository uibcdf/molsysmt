"""Pure MolSysMT topology adapters for the MolSysViewer addon."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..access import has_system, system_for_verbs


@dataclass(frozen=True)
class BondGraphLinks:
    """Bond graph plus viewer-ready atom-pair links."""

    graph: Any
    atom_pairs: list[list[int]]

    @property
    def n_bonds(self) -> int:
        return len(self.atom_pairs)


@dataclass(frozen=True)
class DihedralQuartets:
    """Standard dihedral quartets returned as plain atom-index lists."""

    quartets: list[list[int]]
    dihedral_types: tuple[str, ...]

    @property
    def n_dihedrals(self) -> int:
        return len(self.quartets)


def bond_graph_links(
    view: Any,
    *,
    selection: Any = "all",
    syntax: str = "MolSysMT",
) -> BondGraphLinks:
    """Compute a MolSysMT bond graph and expose edges as viewer links."""
    if not has_system(view):
        raise ValueError("No molecular system attached.")

    import molsysmt as msm

    graph = msm.topology.get_bondgraph(
        system_for_verbs(view),
        selection=selection,
        syntax=syntax,
    )
    atom_pairs = [[int(u), int(v)] for u, v in graph.edges()]
    return BondGraphLinks(graph=graph, atom_pairs=atom_pairs)


def dihedral_quartets(
    view: Any,
    *,
    dihedral_types: tuple[str, ...] = ("phi", "psi", "omega"),
    selection: Any = "all",
    syntax: str = "MolSysMT",
) -> DihedralQuartets:
    """Compute standard MolSysMT dihedral quartets for explicit types."""
    if not has_system(view):
        raise ValueError("No molecular system attached.")

    import molsysmt as msm

    flags = {name: True for name in dihedral_types}
    raw = msm.topology.get_dihedral_quartets(
        system_for_verbs(view),
        selection=selection,
        syntax=syntax,
        **flags,
    )
    if raw is None:
        quartets: list[list[int]] = []
    elif raw and isinstance(raw[0], list) and raw[0] and isinstance(raw[0][0], list):
        quartets = [
            [int(atom_index) for atom_index in quartet]
            for grouped_quartets in raw
            for quartet in grouped_quartets
        ]
    else:
        quartets = [[int(atom_index) for atom_index in quartet] for quartet in raw]
    return DihedralQuartets(quartets=quartets, dihedral_types=tuple(dihedral_types))
