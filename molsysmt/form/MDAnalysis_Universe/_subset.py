"""Building faithful in-memory subsets of MDAnalysis universes."""

from copy import deepcopy

import numpy as np
from depdigest import dep_digest

from molsysmt._private.variables import is_all


def _indices(values, size):
    """Normalizing an all-or-explicit index request."""

    if is_all(values):
        return np.arange(size, dtype=np.int64)
    return np.atleast_1d(np.asarray(values, dtype=np.int64))


@dep_digest("MDAnalysis")
def copy_universe(universe):
    """Copy a provider topology and its reader without Python's pickle fallback."""
    if hasattr(universe, "trajectory") and universe.trajectory is not None:
        return universe.copy()

    import MDAnalysis as mda

    return mda.Universe(universe._topology.copy(), to_guess=())


def _copy_connectivity(universe, output, atom_indices):
    """Restrict stored connectivity fields without interpreting their values."""
    index_map = {int(old): new for new, old in enumerate(atom_indices)}
    for name in ("bonds", "angles", "dihedrals", "impropers"):
        source = getattr(universe._topology, name, None)
        if source is None:
            continue
        retained = [
            index
            for index, entry in enumerate(source.values)
            if all(int(atom) in index_map for atom in entry)
        ]
        entries = [
            tuple(index_map[int(atom)] for atom in source.values[index])
            for index in retained
        ]
        replacement = type(source)(
            entries,
            types=deepcopy([source.types[index] for index in retained]),
            guessed=deepcopy([source._guessed[index] for index in retained]),
            order=deepcopy([source.order[index] for index in retained]),
        )
        if hasattr(output._topology, name):
            output.del_TopologyAttr(name)
        output.add_TopologyAttr(replacement)


@dep_digest("MDAnalysis")
def subset_universe(universe, atom_indices="all", structure_indices="all"):
    """Materialize selected atoms and a representable in-memory structure axis."""
    import MDAnalysis as mda

    all_atoms = is_all(atom_indices)
    if all_atoms and is_all(structure_indices):
        return copy_universe(universe)

    atom_indices = _indices(atom_indices, universe.atoms.n_atoms)
    has_trajectory = hasattr(universe, "trajectory") and universe.trajectory is not None
    if has_trajectory:
        structure_indices = _indices(structure_indices, len(universe.trajectory))
    elif not is_all(structure_indices):
        from molsysmt._private.smonitor import NotCompatibleConversionError

        raise NotCompatibleConversionError(
            "MDAnalysis.Universe",
            "MDAnalysis.Universe",
            {"structure_indices"},
            caller="molsysmt.form.MDAnalysis_Universe.extract",
            message="A Universe without a trajectory cannot apply structure indices.",
        )

    if all_atoms:
        output = mda.Universe(universe._topology.copy(), to_guess=())
    else:
        output = mda.Merge(universe.atoms[atom_indices])
        _copy_connectivity(universe, output, atom_indices)
    if not has_trajectory:
        return output

    source_frame = universe.trajectory.frame
    coordinates = []
    velocities = []
    forces = []
    dimensions = []
    times = []
    velocities_are_available = True
    forces_are_available = True
    dimensions_are_available = True
    time_is_available = True
    from .get_structural_attributes import _timestep_has_time

    try:
        for frame_index in structure_indices:
            timestep = universe.trajectory[int(frame_index)]
            coordinates.append(
                np.asarray(universe.atoms.positions[atom_indices], dtype=np.float32)
            )
            if _timestep_has_time(timestep):
                times.append(float(timestep.time))
            else:
                time_is_available = False
            if getattr(timestep, "has_velocities", False):
                velocities.append(
                    np.asarray(
                        universe.atoms.velocities[atom_indices], dtype=np.float32
                    )
                )
            else:
                velocities_are_available = False
            if getattr(timestep, "has_forces", False):
                forces.append(
                    np.asarray(universe.atoms.forces[atom_indices], dtype=np.float32)
                )
            else:
                forces_are_available = False
            frame_dimensions = getattr(timestep, "dimensions", None)
            if frame_dimensions is None:
                dimensions_are_available = False
            else:
                dimensions.append(
                    np.array(frame_dimensions, dtype=np.float32, copy=True)
                )
    finally:
        universe.trajectory[source_frame]

    times = np.asarray(times, dtype=np.float64)
    if time_is_available and len(times) > 1:
        time_steps = np.diff(times)
        if not np.allclose(time_steps, time_steps[0], rtol=1.0e-10, atol=1.0e-12):
            from molsysmt._private.smonitor import NotCompatibleConversionError

            raise NotCompatibleConversionError(
                "MDAnalysis.Universe",
                "MDAnalysis.Universe",
                {"irregular_time"},
                caller="molsysmt.form.MDAnalysis_Universe.extract",
                message=(
                    "MDAnalysis MemoryReader cannot preserve a non-uniform selected "
                    "time axis. Convert to molsysmt.MolSys to retain irregular time."
                ),
            )
        time_step = float(time_steps[0])
        time_offset = float(times[0])
    elif time_is_available:
        timestep_data = getattr(universe.trajectory.ts, "data", {})
        time_step = float(timestep_data.get("dt", 1.0))
        time_offset = float(times[0])
    else:
        time_step = 1.0
        time_offset = 0.0

    output.load_new(
        np.asarray(coordinates, dtype=np.float32),
        format=mda.coordinates.memory.MemoryReader,
        order="fac",
        velocities=(
            np.asarray(velocities, dtype=np.float32)
            if velocities_are_available
            else None
        ),
        forces=np.asarray(forces, dtype=np.float32) if forces_are_available else None,
        dimensions=(
            np.asarray(dimensions, dtype=np.float32)
            if dimensions_are_available
            else None
        ),
        dt=time_step,
        time_offset=time_offset,
    )
    return output
