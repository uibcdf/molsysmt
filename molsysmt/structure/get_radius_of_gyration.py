from molsysmt._private._digestion import digest
from molsysmt._private.exceptions.not_implemented import NotImplementedError
from molsysmt.lib import geometry as libgeometry
from molsysmt import puw
import numpy as np

@digest
def get_radius_of_gyration(molecular_system, selection='all', structure_indices='all',
                           weights=None, pbc=False, engine='MolSysMT', syntax='MolSysMT'):

    if engine=='MolSysMT':

        from molsysmt.basic import select, get

        coordinates == msm.get(molecular_system, element='atom', selection=selection,
                               structure_indices=structure_indices, syntax=syntax, coordinates=True)

        length_units = puw.get_unit(coordinates_1)
        coordinates = np.asfortranarray(puw.get_value(coordinates), dtype='float64')

        n_structures = coordinates.shape[0]
        n_atoms = coordinates.shape[1]

        if pbc:

            box, box_shape = get(molecular_system, element='system', structure_indices=structure_indices, box=True,
                                 box_shape=True)

            orthogonal = 0
            if box_shape is None:
                raise ValueError("The system has no PBC box. The input argument 'pbc' can not be True.")
            elif box_shape == 'cubic':
                orthogonal =1

        else:

            box= np.zeros([n_structures, 3, 3])*length_units
            orthogonal = 1

        box = np.asfortranarray(puw.get_value(box, to_unit=length_units), dtype='float64')

        if weights is None:
            weights = np.ones(n_atoms)
            weights_units = 1
        elif weights is 'masses':
            from molsysmt.chemphys import get_masses
            masses = get_masses(molecular_systems, selection=selection, syntax=syntax)
            weights_units = puw.get_unit(masses)
            weights = puw.get_value(masses)

        output = libgeometry.radius_of_gyration(coordinates, weights, box, orthogonal, int(pbc), n_structures, n_atoms)
        output = output*weights_units*length_units*length_units

        del(weights, coordinates, box, orthogonal)

    elif engine=='mdtraj':

        raise NotImplementedError()

    else:

        raise NotImplementedError()

    return output

