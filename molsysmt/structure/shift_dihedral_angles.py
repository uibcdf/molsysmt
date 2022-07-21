from molsysmt._private.digestion import digest
import numpy as np
from molsysmt import puw
from molsysmt.lib import geometry as libgeometry

@digest
def shift_dihedral_angles(molecular_system, quartets=None, angles_shifts=None, blocks=None,
                          structure_indices='all', pbc=True, in_place=False, engine='MolSysMT'):

    from . import get_dihedral_angles, set_dihedral_angles
    from molsysmt.basic import get

    if type(quartets) in [list,tuple]:
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

    n_quartets = quartets.shape[0]
    n_structures = get(molecular_system, element='system', structure_indices=structure_indices, n_structures=True)

    angles_shifts_units = puw.get_unit(angles_shifts)
    angles_shifts_value = puw.get_value(angles_shifts)

    if type(angles_shifts_value) in [float]:
        if (n_quartets==1 and n_structures==1):
            angles_shifts_value = np.array([[angles_shifts_value]], dtype=float)
        else:
            raise ValueError("angles_shifts do not match the number of frames and quartets")
    elif type(angles_shifts_value) in [list,tuple]:
        angles_shifts_value = np.array(angles_shifts_value, dtype=float)
    elif type(angles_shifts_value) is np.ndarray:
        pass
    else:
        raise ValueError

    shape = angles_shifts_value.shape

    if len(shape)==1:
        angles_shifts_value = angles_shifts_value.reshape([n_structures, n_quartets])

    angles_shifts=angles_shifts_value*angles_shifts_units

    angles = get_dihedral_angles(molecular_system, quartets=quartets,
            structure_indices=structure_indices, pbc=pbc, check=False)
    angles = angles + angles_shifts

    return set_dihedral_angles(molecular_system, quartets=quartets, angles=angles, blocks=None,
                               structure_indices=structure_indices, pbc=pbc, in_place=in_place,
                               engine=engine, check=False)

