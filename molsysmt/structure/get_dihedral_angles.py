import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private.digestion import digest
from molsysmt.basic import get
from molsysmt.lib import geometry as libgeometry

@digest()
def get_dihedral_angles(molecular_system, selection='all', quartets=None,
                        structure_indices='all', syntax='MolSysMT', pbc=False, **kwargs):

    # phi, psi, omega, chi1, chi2, chi3, chi4, chi5

    dihedral_angles = []
    for key in kwargs.keys():
        if kwargs[key]:
            dihedral_angles.append(key)

    from molsysmt.topology import get_dihedral_quartets

    coordinates = get(molecular_system, element='system', structure_indices=structure_indices, coordinates=True)
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

    if quartets is not None:

        n_angles = quartets.shape[0]

        angles = libgeometry.dihedral_angles(coordinates, box, orthogonal, int(pbc), quartets, n_angles, n_atoms, n_structures)
        angles = np.ascontiguousarray(angles)*puw.unit('degrees')

        return angles

    else:

        all_angles = []

        for dihedral_angle in dihedral_angles:

            quartets = get_dihedral_quartets(molecular_system, selection=selection, syntax=syntax, **{dihedral_angle:True})

            n_angles = quartets.shape[0]

            angles = libgeometry.dihedral_angles(coordinates, box, orthogonal, int(pbc), quartets, n_angles, n_atoms, n_structures)
            angles = np.ascontiguousarray(angles)*puw.unit('degrees')

            all_angles.append(angles)

        if len(dihedral_angles)==0:
            all_angles = None
        elif len(dihedral_angles)==1:
            all_angles = all_angles[0]

        return all_angles
