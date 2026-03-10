from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import types

form = 'MDAnalysis.Universe'


@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    frames = _get_frame_indices(item, structure_indices)
    output = []
    for frame_index in frames:
        item.trajectory[frame_index]
        coords = np.asarray(item.atoms.positions, dtype=np.float64)
        if not is_all(indices):
            coords = coords[indices, :]
        output.append(coords)
    coordinates = np.asarray(output, dtype=np.float64)
    return puw.quantity(coordinates, 'angstroms', standardized=True)


@arg_digest(form=form)
def get_coordinates_from_system(item, structure_indices='all', skip_digestion=False):
    return get_coordinates_from_atom(item, indices='all', structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):
    if not hasattr(item, 'trajectory') or item.trajectory is None:
        return 0
    return len(_get_frame_indices(item, structure_indices))


@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):
    if not hasattr(item, 'trajectory') or item.trajectory is None:
        return None
    frames = _get_frame_indices(item, structure_indices)
    boxes = []
    has_box = False
    for frame_index in frames:
        ts = item.trajectory[frame_index]
        dimensions = getattr(ts, 'dimensions', None)
        if dimensions is None or np.allclose(dimensions[:3], 0.0):
            boxes.append(None)
            continue
        has_box = True
        lx, ly, lz, alpha, beta, gamma = [float(ii) for ii in dimensions]
        box = np.array([
            [lx, 0.0, 0.0],
            [0.0, ly, 0.0],
            [0.0, 0.0, lz],
        ], dtype=np.float64)
        boxes.append(box)
    if not has_box:
        return None
    return puw.quantity(np.asarray(boxes, dtype=np.float64), 'angstroms', standardized=True)


@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):
    if not hasattr(item, 'trajectory') or item.trajectory is None:
        return None
    frames = _get_frame_indices(item, structure_indices)
    times = []
    for frame_index in frames:
        ts = item.trajectory[frame_index]
        time = getattr(ts, 'time', None)
        if time is None:
            return None
        times.append(float(time))
    return puw.quantity(np.asarray(times, dtype=np.float64), 'picosecond', standardized=True)


@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):
    frames = _get_frame_indices(item, structure_indices)
    return [str(ii) for ii in frames]


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
