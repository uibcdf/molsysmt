from molsysmt._private_tools._digestion import *
from molsysmt._private_tools.exceptions import *
from molsysmt.basic import select, get
from molsysmt.lib import geometry as libgeometry
from molsysmt import puw
import numpy as np

def get_radius_of_gyration(molecular_system, selection='all', structure_indices='all',
                           weights=None, pbc=False, engine='MolSysMT', syntaxis='MolSysMT'):

    molecular_system = digest_molecular_system(molecular_system)

    engine = digest_engine(engine)
    structure_indices = digest_structure_indices(structure_indices)

    if engine=='MolSysMT':

        coordinates == msm.get(molecular_system, target='atom', selection=selection,
                               structure_indices=structure_indices, syntaxis=syntaxis, coordinates=True)

        length_units = puw.get_unit(coordinates_1)
        coordinates = np.asfortranarray(puw.get_value(coordinates), dtype='float64')

        n_frames = coordinates.shape[0]
        n_atoms = coordinates.shape[1]

        if pbc:

            box, box_shape = get(molecular_system, target='system', box=True, box_shape=True, structure_indices=structure_indices)

            orthogonal = 0
            if box_shape is None:
                raise ValueError("The system has no PBC box. The input argument 'pbc' can not be True.")
            elif box_shape == 'cubic':
                orthogonal =1

        else:

            box= np.zeros([nframes, 3, 3])*length_units
            orthogonal = 1

        box = np.asfortranarray(puw.get_value(box, to_unit=length_units), dtype='float64')

        if weights is None:
            weights = np.ones(n_atoms)
            weights_units = 1
        elif weights is 'masses':
            masses = msm.chemphys.get_masses(molecular_systems, selection=selection, syntaxis=syntaxis)
            weights_units = msm.puw.get_unit(masses)
            weights = msm.puw.get_value(masses)

        output = libgeometry.radius_of_gyration(coordinates, weights, box, orthogonal, int(pbc), n_frames, n_atoms)
        output = output*weights_units*length_units*length_units

        del(weights, coordinates, box, orthogonal)

    elif engine=='mdtraj':

        raise NotImplementedError()

    else:

        raise NotImplementedError()

    return output

