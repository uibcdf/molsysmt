import numpy as np

from molsysmt import pyunitwizard as _puw
from molsysmt._private.variables import is_all as _is_all


def set_coordinates_to_atom(item, indices="all", structure_indices="all", value=None):
    """
    Setting a structure-first coordinate population in a StructuresDict.


    Parameters
    ----------
    item : dict
        Structural dictionary with a unit-bearing coordinates array shaped
        (n_structures, n_atoms, 3). Mutation is performed in place.
    indices : int, list, tuple, numpy.ndarray or str, default='all'
        Atom indices selecting the second coordinate axis. Explicit list
        order and repetitions define the incoming atom population.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices selecting the first coordinate axis, in supplied
        order. Both explicit selections form a Cartesian product.
    value : quantity or None, default=None
        Coordinate block with shape (n_selected_structures, n_selected_atoms, 3).
        Its length units are converted to the dictionary's stored units.

    Returns
    -------
    None
        Coordinates are updated on the requested population. Boxes and
        coordinates outside that population remain unchanged.

    Notes
    -----
    This adapter delivery function receives index/value validation from the
    public basic.set boundary; it does not reinterpret or transpose square
    selections.

    Examples
    --------
    >>> import molsysmt as msm
    >>> import numpy as np
    >>> molsys = {'coordinates': msm.pyunitwizard.quantity(np.zeros((3, 4, 3)), 'nm')}
    >>> msm.set(molsys, selection=[3, 1], structure_indices=[2, 0],
    ...     coordinates=msm.pyunitwizard.quantity(np.ones((2, 2, 3)), 'angstrom'))
    >>> xyz = msm.pyunitwizard.get_value(molsys['coordinates'], to_unit='nm')
    >>> np.allclose(xyz[2, [3, 1]], 0.1) and np.allclose(xyz[1], 0)
    True

    .. versionadded:: 1.0.0
    """
    length_unit = _puw.get_unit(item["coordinates"])
    value = _puw.convert(value, to_unit=length_unit)

    if _is_all(indices):
        if _is_all(structure_indices):
            item["coordinates"] = value
        else:
            item["coordinates"][structure_indices, :, :] = value
    else:
        if _is_all(structure_indices):
            item["coordinates"][:, indices, :] = value
        else:
            item["coordinates"][np.ix_(structure_indices, indices)] = value

    pass
