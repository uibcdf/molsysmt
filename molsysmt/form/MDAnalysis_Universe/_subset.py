"""Building faithful in-memory subsets of MDAnalysis universes."""

import numpy as np

from molsysmt._private.variables import is_all


def _indices(values, size):
    """Normalizing an all-or-explicit index request."""

    if is_all(values):
        return np.arange(size, dtype=np.int64)
    return np.atleast_1d(np.asarray(values, dtype=np.int64))


def subset_universe(universe, atom_indices="all", structure_indices="all"):
    """Returning an MDAnalysis Universe subset without changing the source frame."""

    import MDAnalysis as mda

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

    output = mda.Merge(universe.atoms[atom_indices])
    if not has_trajectory:
        return output

    source_frame = universe.trajectory.frame
    coordinates = []
    velocities = []
    dimensions = []
    times = []
    velocities_are_available = True
    dimensions_are_available = True
    time_is_available = True
    from .get_structural_attributes import _timestep_has_time

    try:
        for frame_index in structure_indices:
            timestep = universe.trajectory[int(frame_index)]
            coordinates.append(np.asarray(universe.atoms.positions[atom_indices], dtype=np.float32))
            if _timestep_has_time(timestep):
                times.append(float(timestep.time))
            else:
                time_is_available = False
            if getattr(timestep, "has_velocities", False):
                velocities.append(
                    np.asarray(universe.atoms.velocities[atom_indices], dtype=np.float32)
                )
            else:
                velocities_are_available = False
            frame_dimensions = getattr(timestep, "dimensions", None)
            if frame_dimensions is None:
                dimensions_are_available = False
            else:
                dimensions.append(np.asarray(frame_dimensions, dtype=np.float32))
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
        timestep_data = getattr(universe.trajectory.ts, 'data', {})
        time_step = float(timestep_data.get('dt', 1.0))
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
        dimensions=(
            np.asarray(dimensions, dtype=np.float32)
            if dimensions_are_available
            else None
        ),
        dt=time_step,
        time_offset=time_offset,
    )
    return output
