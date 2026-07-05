"""Selection adapters for MolSysMT queries applied to MolSysViewer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..access import has_system


@dataclass(frozen=True)
class SelectionResult:
    selection: Any
    element: str
    indices: list[int]
    atom_indices: list[int]

    @property
    def n_selected(self) -> int:
        return len(self.indices)


def select_indices(view: Any, selection: Any = "all", *, element: str = "atom") -> SelectionResult:
    """Run ``msm.select`` on the active view and resolve atoms for the viewer."""
    if not has_system(view):
        raise ValueError("No molecular system attached.")

    import numpy as np
    import molsysmt as msm

    indices = [int(item) for item in np.asarray(
        msm.select(view, selection=selection, element=element)
    ).reshape(-1)]

    if element == "atom":
        atom_indices = list(indices)
    else:
        atom_indices = _atom_indices_for_element_indices(view, element, indices)

    return SelectionResult(
        selection=selection,
        element=element,
        indices=indices,
        atom_indices=atom_indices,
    )


def _atom_indices_for_element_indices(view: Any, element: str, indices: list[int]) -> list[int]:
    import molsysmt as msm

    element_to_atom_attribute = {
        "group": "group_index",
        "component": "component_index",
        "chain": "chain_index",
        "molecule": "molecule_index",
        "entity": "entity_index",
    }
    if element not in element_to_atom_attribute:
        raise ValueError(f"Unsupported selection element: {element!r}")

    selected = set(indices)
    values = msm.get(
        view,
        element="atom",
        output_type="values",
        **{element_to_atom_attribute[element]: True},
    )
    if values is None:
        values = []
    return [
        atom_index
        for atom_index, value in enumerate(values)
        if value is not None and int(value) in selected
    ]
