from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt import lib as msmlib
from molsysmt._private.variables import is_all, is_iterable_of_iterables
from molsysmt import pyunitwizard as puw
from scipy.spatial.transform import Rotation as R
import numpy as np
import gc

@digest()
def align_principal_axes(molecular_system, selection='all',
        principal_axes_of_selection=None, principal_axes_type='inertia',
        structure_indices='all', weights=None, axes=[[1,0,0],[0,1,0],[0,0,1]], center=False,
        syntax='MolSysMT', engine='MolSysMT', in_place=False):

    from molsysmt.basic import select, get, set, copy
    from . import get_principal_axes, get_center

    if engine=='MolSysMT':

        if principal_axes_of_selection is None:

            principal_axes_of_selection = selection

        aux_axes, _ = get_principal_axes(molecular_system,
                selection=principal_axes_of_selection, structure_indices=structure_indices,
                principal_axes_type=principal_axes_type,
                weights=weights, syntax=syntax)

        aux_center = get_center(molecular_system, selection=principal_axes_of_selection,
                structure_indices=structure_indices, weights=weights, syntax=syntax)

        atom_indices = select(molecular_system, selection=selection, syntax=syntax)

        coordinates = get(molecular_system, element='atom', selection=atom_indices,
                structure_indices=structure_indices, coordinates=True)

        coordinates, length_unit = puw.get_value_and_unit(coordinates)
        aux_center, _ = puw.get_value_and_unit(aux_center)

        n_structures = coordinates.shape[0]

        if np.dot(np.cross(axes[0], axes[1]), axes[2])<0.0:
            axes[2]=-axes[2]

        for ii in range(n_structures):

            if np.dot(np.cross(aux_axes[ii,0], aux_axes[ii,1]), aux_axes[ii,2])<0.0:
                aux_axes[ii,2]=-aux_axes[ii,2]

            rot, val_aux = R.align_vectors(axes, aux_axes[ii])
            coordinates[ii,:,:]=coordinates[ii,:,:]-aux_center[ii,0,:]
            coordinates[ii,:,:]=rot.apply(coordinates[ii,:,:])
            if not center:
                coordinates[ii,:,:]=coordinates[ii,:,:]+aux_center[ii]

        coordinates = puw.quantity(coordinates, unit=length_unit)

        if in_place:

            set(molecular_system, selection=atom_indices, structure_indices=structure_indices,
                syntax=syntax, coordinates=coordinates)
            del(coordinates, aux_center, aux_axes, atom_indices)
            gc.collect()

        else:

            tmp_molecular_system = copy(molecular_system)
            set(tmp_molecular_system, selection=atom_indices, structure_indices=structure_indices,
                syntax=syntax, coordinates=coordinates)
            del(coordinates, aux_center, aux_axes, atom_indices)
            gc.collect()

            return tmp_molecular_system

    else:

        raise NotImplementedMethodError()

