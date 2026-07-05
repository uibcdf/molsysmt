"""Pure MolSysMT molecular-mechanics adapters for the MolSysViewer addon."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..access import has_system, materialize_system, system_for_verbs


@dataclass(frozen=True)
class ForcesResult:
    """Forces prepared for vector rendering."""

    forces: Any
    vectors: Any
    atom_indices: list[int]

    @property
    def n_vectors(self) -> int:
        return len(self.atom_indices)


@dataclass(frozen=True)
class PotentialEnergyResult:
    """Scalar potential-energy result."""

    energy: Any
    value: float


@dataclass(frozen=True)
class MinimizedSystem:
    """Minimized molecular system ready to load into the viewer.

    Minimization moves atoms but does not add/remove them, so the viewer can
    reconcile it with ``view.set_coordinates`` (preserving regions, selections,
    colors and shapes) instead of a destructive reload.
    """

    molecular_system: Any
    coordinates: Any = None


def _first_structure_forces(forces: Any) -> Any:
    import numpy as np

    forces_arr = np.asarray(forces)
    if forces_arr.ndim == 3:
        return forces_arr[0]
    return forces_arr


def compute_forces(
    view: Any,
    *,
    selection: Any = "all",
    engine: str = "OpenMM",
    syntax: str = "MolSysMT",
) -> ForcesResult:
    """Compute forces from the active viewer system."""
    if not has_system(view):
        raise ValueError("No molecular system attached.")

    import molsysmt as msm

    forces = msm.molecular_mechanics.get_forces(
        system_for_verbs(view),
        selection=selection,
        engine=engine,
        syntax=syntax,
    )
    vectors = _first_structure_forces(forces)
    atom_indices = list(range(len(vectors)))
    return ForcesResult(forces=forces, vectors=vectors, atom_indices=atom_indices)


def potential_energy(
    view: Any,
    *,
    selection: Any = "all",
    platform: str = "CPU",
    engine: str = "OpenMM",
    syntax: str = "MolSysMT",
) -> PotentialEnergyResult:
    """Compute potential energy from the active viewer system."""
    if not has_system(view):
        raise ValueError("No molecular system attached.")

    import molsysmt as msm
    import numpy as np

    energy = msm.molecular_mechanics.get_potential_energy(
        system_for_verbs(view),
        selection=selection,
        platform=platform,
        engine=engine,
        syntax=syntax,
    )
    value = float(np.asarray(energy).flatten()[0])
    return PotentialEnergyResult(energy=energy, value=value)


def minimize_energy(
    view: Any,
    *,
    platform: str = "CPU",
    engine: str = "OpenMM",
) -> MinimizedSystem:
    """Minimize a materialized copy of the active viewer system."""
    if not has_system(view):
        raise ValueError("No molecular system attached.")

    import molsysmt as msm

    new_ms = msm.molecular_mechanics.potential_energy_minimization(
        materialize_system(view),
        platform=platform,
        engine=engine,
    )
    coordinates = msm.get(new_ms, coordinates=True)
    return MinimizedSystem(molecular_system=new_ms, coordinates=coordinates)
