from molsysmt._private.smonitor import NotImplementedMethodError
from smonitor import signal
from molsysmt._private.arg_digestion import arg_digest
from molsysmt import lib as msmlib
from molsysmt._private.variables import is_all, is_iterable_of_iterables
from molsysmt import pyunitwizard as puw
import numpy as np
import gc

@signal(tags=['api', 'structure'])
@arg_digest()
def get_principal_axes(molecular_system, selection='all', structure_indices='all',
        weights=None, principal_axes_type='inertia', syntax='MolSysMT', engine='MolSysMT'):
    """
    Computing principal axes for a selection of atoms.

    Parameters
    ----------
    molecular_system : molecular system
        Input system.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Atoms used for axis computation.
    structure_indices : 'all' or array-like, default 'all'
        Structures/frames to evaluate.
    weights : array-like, optional
        Weights per atom.
    principal_axes_type : {'inertia', 'geometric'}, default 'inertia'
        Kind of principal axes to compute.
    syntax : str, default 'MolSysMT'
        Selection syntax when using strings.
    engine : {'MolSysMT'}, default 'MolSysMT'
        Backend.

    Returns
    -------
    tuple
        `(axes, moments)` where `axes` has shape `(n_structures, 3, 3)` and `moments` are variances or inertia moments.

    Raises
    ------
    NotImplementedMethodError
        If the engine is unsupported.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import select, get

    if engine=='MolSysMT':

        atom_indices = select(molecular_system, selection=selection, syntax=syntax)

        coordinates = get(molecular_system, element='atom', selection=atom_indices,
                structure_indices=structure_indices, coordinates=True)
        coordinates, length_unit = puw.get_value_and_unit(coordinates)

        if weights is None:
            weights = np.ones((coordinates.shape[1]), dtype=np.float64)

        if principal_axes_type=='geometric':

            variances, axes = msmlib.structure.get_principal_geometric_axes(coordinates, weights)
            moments=variances

        elif principal_axes_type=='inertia':

            moments, axes = msmlib.structure.get_principal_inertia_axes(coordinates, weights)

        del(coordinates, atom_indices, weights)

        gc.collect()

        return axes, moments

    else:

        raise NotImplementedMethodError()
