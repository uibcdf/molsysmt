import numpy as np
from molsysmt import puw
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from molsysmt.basic import get
from molsysmt.lib import geometry as libgeometry

def get_dihedral_angles(molecular_system, dihedral_angle=None, selection='all', quartets=None,
                        structure_indices='all', syntaxis='MolSysMT', pbc=False, check=True):

    if check:

        digest_single_molecular_system(molecular_system)
        syntaxis = digest_syntaxis(syntaxis)
        selection = digest_selection(selection, syntaxis)
        structure_indices = digest_structure_indices(structure_indices)

    from molsysmt.topology import get_covalent_dihedral_quartets

    if quartets is None:

        quartets = get_covalent_dihedral_quartets(molecular_system, dihedral_angle=dihedral_angle,
                                                  selection=selection, syntaxis=syntaxis, check=False)

    elif type(quartets) in [list,tuple]:
        quartets = np.array(quartets, dtype=int)
    elif type(quartets) is np.ndarray:
        pass
    else:
        raise ValueError

    shape = quartets.shape

    if len(shape)==1:
        if shape[0]==4:
            quartets=quartets.reshape([1,4])
        else:
            raise ValueError
    elif len(shape)==2:
        if shape[1]!=4:
            raise ValueError
    else:
        raise ValueError

    coordinates = get(molecular_system, element='system', structure_indices=structure_indices, coordinates=True)

    n_angles = quartets.shape[0]
    n_structures = coordinates.shape[0]
    n_atoms = coordinates.shape[1]

    if pbc:

        box, box_shape = get(molecular_system, element='system', structure_indices=structure_indices, box=True,
                             box_shape=True)
        if box_shape is None:
            raise ValueError("The system has no PBC box. The input argument 'pbc' can not be True.")
        orthogonal = 0

        if box_shape is None:
            orthogonal =1
        elif box_shape == 'cubic':
            orthogonal =1

    else:

        orthogonal = 1
        box = np.zeros([n_structures,3,3])*puw.unit('nm')

    box = np.asfortranarray(puw.get_value(box, to_unit='nm'), dtype='float64')
    coordinates = np.asfortranarray(puw.get_value(coordinates, to_unit='nm'), dtype='float64')

    angles = libgeometry.dihedral_angles(coordinates, box, orthogonal, int(pbc), quartets, n_angles, n_atoms, n_structures)
    angles = np.ascontiguousarray(angles)*puw.unit('degrees')

    return angles
