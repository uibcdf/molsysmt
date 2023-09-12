from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt import lib as msmlib
from molsysmt._private.variables import is_all, is_iterable_of_iterables
from molsysmt import pyunitwizard as puw
import numpy as np
import gc

@digest()
def get_principal_axes(molecular_system, selection='all', structure_indices='all',
        weights=None, principal_axes_type='inertia', syntax='MolSysMT', engine='MolSysMT'):

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

