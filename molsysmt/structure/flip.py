from molsysmt._private.argdigest import arg_digest
from smonitor import signal
import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private import rust_backend as _kernels


@signal(tags=["api", "structure"])
@arg_digest()
def flip(
    molecular_system,
    vector=None,
    point="[0,0,0] nm",
    selection="all",
    structure_indices="all",
    syntax="MolSysMT",
    in_place=False,
):
    """
    Reflect (flip) atomic coordinates of a selection through a plane defined by a vector and a point.

    Each selected atom's position is reflected across the plane that passes through ``point``
    and is perpendicular to ``vector``. The native kernel
    The reflection is performed in-place on the coordinate array by the compute kernel.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    vector : array-like or None, default=None
        Normal vector of the reflection plane.
    point : PyUnitWizard quantity, default='[0,0,0] nm'
        Point on the reflection plane, in units of length.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    in_place : bool, default=False
        Whether to modify the input molecular system in place.

    Returns
    -------
    molecular system or None
        A new molecular system with the reflected coordinates when ``in_place=False``;
        ``None`` when ``in_place=True``.


    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get, set, select, copy
    from molsysmt.structure import translate

    coordinates = get(
        molecular_system,
        element="atom",
        selection=selection,
        structure_indices=structure_indices,
        syntax=syntax,
        coordinates=True,
    )

    coordinates, length_unit = puw.get_value_and_unit(coordinates)
    point = puw.get_value(point, to_unit=length_unit)

    coordinates = np.asarray(coordinates, dtype=np.float64)
    if vector is None:
        vector = [0.0, 0.0, 1.0]
    vector = np.asarray(vector, dtype=np.float64)
    point = np.asarray(point, dtype=np.float64)

    point = point[0]

    coordinates = _kernels.flip(coordinates, vector, point)

    coordinates = puw.quantity(coordinates, unit=length_unit)

    if in_place:
        set(
            molecular_system,
            selection=selection,
            structure_indices=structure_indices,
            syntax=syntax,
            coordinates=coordinates,
        )
        del coordinates

    else:
        tmp_molecular_system = copy(molecular_system)
        set(
            tmp_molecular_system,
            selection=selection,
            structure_indices=structure_indices,
            syntax=syntax,
            coordinates=coordinates,
        )
        del coordinates

        return tmp_molecular_system
