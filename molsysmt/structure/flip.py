from molsysmt._private.arg_digestion import arg_digest
from smonitor import signal
import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt import lib as msmlib
import gc

@signal(tags=['api', 'structure'])
@arg_digest()
def flip(molecular_system, vector=None, point='[0,0,0] nm', selection='all', structure_indices='all',
        syntax='MolSysMT', in_place=False):
    """
    Reflect (flip) atomic coordinates of a selection through a plane defined by a vector and a point.

    Each selected atom's position is reflected across the plane that passes through ``point``
    and is perpendicular to ``vector``.  The Numba JIT kernel
    ``msmlib.structure.flip`` performs the reflection in-place on the coordinate array.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any form supported by MolSysMT.
    vector : array-like of float, default [0, 0, 1]
        Normal vector of the reflection plane (need not be unit length).
        The reflection plane is perpendicular to this vector.
    point : str or quantity, default '[0,0,0] nm'
        A point lying on the reflection plane, given as a PyUnitWizard length
        quantity or a parseable string (e.g. ``'[0,0,0] nm'``).
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Atoms whose coordinates are reflected.
    structure_indices : 'all' or array-like, default 'all'
        Frame indices over which the reflection is applied.
    syntax : str, default 'MolSysMT'
        Selection syntax used when ``selection`` is a string.
    in_place : bool, default False
        If ``True`` the molecular system is modified in-place and ``None`` is returned.
        If ``False`` a new copy is returned with the reflected coordinates.

    Returns
    -------
    molecular system or None
        A new molecular system with the reflected coordinates when ``in_place=False``;
        ``None`` when ``in_place=True``.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get, set, select, copy
    from molsysmt.structure import translate

    coordinates = get(molecular_system, element='atom', selection=selection, structure_indices=structure_indices,
                      syntax=syntax, coordinates=True)

    coordinates, length_unit =  puw.get_value_and_unit(coordinates)
    point = puw.get_value(point, to_unit=length_unit)

    coordinates = np.asarray(coordinates, dtype=np.float64)
    if vector is None:
        vector = [0.0, 0.0, 1.0]
    vector = np.asarray(vector, dtype=np.float64)
    point = np.asarray(point, dtype=np.float64)

    point = point[0]

    coordinates = msmlib.structure.flip(coordinates, vector, point)

    coordinates = puw.quantity(coordinates, unit=length_unit)


    if in_place:

        set(molecular_system, selection=selection, structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates)
        del(coordinates)
        gc.collect()

    else:

        tmp_molecular_system = copy(molecular_system)
        set(tmp_molecular_system, selection=selection, structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates)
        del(coordinates)
        gc.collect()

        return tmp_molecular_system

