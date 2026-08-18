from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import types

form = 'MDAnalysis.Universe'


def _source_frame(item):
    """Returning the active frame to restore after random access."""

    return item.trajectory.frame


def _timestep_has_time(timestep):
    """Returning whether MDAnalysis received time metadata from its reader."""

    data = getattr(timestep, 'data', {})
    return any(key in data for key in ('time', 'dt', 'time_offset'))


@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    """
    Getting coordinates from atom in form MDAnalysis.Universe.

    Parameters
    ----------
    item : MDAnalysis.Universe
        Source item in MDAnalysis.Universe form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    frames = _get_frame_indices(item, structure_indices)
    output = []
    source_frame = _source_frame(item)
    try:
        for frame_index in frames:
            item.trajectory[frame_index]
            coords = np.asarray(item.atoms.positions, dtype=np.float64)
            if not is_all(indices):
                coords = coords[indices, :]
            output.append(coords)
    finally:
        item.trajectory[source_frame]
    coordinates = np.asarray(output, dtype=np.float64)
    return puw.quantity(coordinates, 'angstroms', standardized=True)


@arg_digest(form=form)
def get_velocities_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    """
    Getting velocities from atom in form MDAnalysis.Universe.

    Parameters
    ----------
    item : MDAnalysis.Universe
        Source item in MDAnalysis.Universe form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    frames = _get_frame_indices(item, structure_indices)
    output = []
    source_frame = _source_frame(item)
    try:
        for frame_index in frames:
            timestep = item.trajectory[frame_index]
            if not getattr(timestep, 'has_velocities', False):
                return None
            velocities = np.asarray(item.atoms.velocities, dtype=np.float64)
            if not is_all(indices):
                velocities = velocities[indices, :]
            output.append(velocities)
    finally:
        item.trajectory[source_frame]
    return puw.quantity(np.asarray(output), 'angstroms/picosecond', standardized=True)


@arg_digest(form=form)
def get_coordinates_from_system(item, structure_indices='all', skip_digestion=False):
    """
    Getting coordinates from system in form MDAnalysis.Universe.

    Parameters
    ----------
    item : MDAnalysis.Universe
        Source item in MDAnalysis.Universe form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_coordinates_from_atom(item, indices='all', structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):
    """
    Getting n structures from system in form MDAnalysis.Universe.

    Parameters
    ----------
    item : MDAnalysis.Universe
        Source item in MDAnalysis.Universe form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if not hasattr(item, 'trajectory') or item.trajectory is None:
        return 0
    return len(_get_frame_indices(item, structure_indices))


@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):
    """
    Getting box from system in form MDAnalysis.Universe.

    Parameters
    ----------
    item : MDAnalysis.Universe
        Source item in MDAnalysis.Universe form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if not hasattr(item, 'trajectory') or item.trajectory is None:
        return None
    frames = _get_frame_indices(item, structure_indices)
    lengths = []
    angles = []
    source_frame = _source_frame(item)
    try:
        for frame_index in frames:
            ts = item.trajectory[frame_index]
            dimensions = getattr(ts, 'dimensions', None)
            if dimensions is None or np.allclose(dimensions[:3], 0.0):
                return None
            lengths.append(dimensions[:3])
            angles.append(dimensions[3:])
    finally:
        item.trajectory[source_frame]

    from molsysmt.pbc import get_box_from_lengths_and_angles

    return get_box_from_lengths_and_angles(
        puw.quantity(np.asarray(lengths), 'angstroms'),
        puw.quantity(np.asarray(angles), 'degrees'),
        skip_digestion=True,
    )


@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):
    """
    Getting time from system in form MDAnalysis.Universe.

    Parameters
    ----------
    item : MDAnalysis.Universe
        Source item in MDAnalysis.Universe form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if not hasattr(item, 'trajectory') or item.trajectory is None:
        return None
    frames = _get_frame_indices(item, structure_indices)
    times = []
    source_frame = _source_frame(item)
    try:
        for frame_index in frames:
            ts = item.trajectory[frame_index]
            if not _timestep_has_time(ts):
                return None
            time = getattr(ts, 'time', None)
            if time is None:
                return None
            times.append(float(time))
    finally:
        item.trajectory[source_frame]
    return puw.quantity(np.asarray(times, dtype=np.float64), 'picosecond', standardized=True)


@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):
    """
    Getting structure id from system in form MDAnalysis.Universe.

    Parameters
    ----------
    item : MDAnalysis.Universe
        Source item in MDAnalysis.Universe form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    frames = _get_frame_indices(item, structure_indices)
    return np.asarray(frames, dtype=np.int64)


def _get_frame_indices(item, structure_indices):
    if not hasattr(item, 'trajectory') or item.trajectory is None:
        return []
    n_frames = len(item.trajectory)
    if is_all(structure_indices):
        return list(range(n_frames))
    if isinstance(structure_indices, (int, np.integer)):
        return [int(structure_indices)]
    return [int(ii) for ii in structure_indices]


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
