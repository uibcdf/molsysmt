import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private.digestion import digest
from molsysmt.basic import get
from molsysmt.lib import geometry as libgeometry

@digest()
def get_dihedral_angles(molecular_system, dihedral_angle=None, selection='all', quartets=None,
                        structure_indices='all', syntax='MolSysMT', pbc=False):

    from molsysmt.topology import get_dihedral_quartets

    if quartets is None:

        quartets = get_dihedral_quartets(molecular_system, dihedral_angle=dihedral_angle,
                                                  selection=selection, syntax=syntax)

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
