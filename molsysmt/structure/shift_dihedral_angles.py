from molsysmt._private.arg_digestion import arg_digest
from smonitor import signal
from molsysmt._private.smonitor import ArgumentError, ArgumentLengthError
import numpy as np
from molsysmt import pyunitwizard as puw

@signal(tags=['api', 'structure'])
@arg_digest()
def shift_dihedral_angles(molecular_system, dihedral_quartets=None, shifts=None, blocks=None,
                          structure_indices='all', pbc=True, in_place=False, engine='MolSysMT',
                          skip_digestion=False):
    """
    To be written soon...
    """

    from . import get_dihedral_angles, set_dihedral_angles
    from molsysmt.basic import get

    if type(dihedral_quartets) in [list,tuple]:
        dihedral_quartets = np.array(dihedral_quartets, dtype=int)
    elif type(dihedral_quartets) is np.ndarray:
        pass
    else:
        raise ArgumentError(
            argument="dihedral_quartets",
            value=dihedral_quartets,
            caller="molsysmt.structure.shift_dihedral_angles",
            message="The argument dihedral_quartets needs to be an array-like object."
        )

    shape = dihedral_quartets.shape

    if len(shape)==1:
        if shape[0]==4:
            dihedral_quartets=dihedra_quartets.reshape([1,4])
        else:
            raise ArgumentError(
                argument="dihedral_quartets",
                value=dihedral_quartets,
                caller="molsysmt.structure.shift_dihedral_angles",
                message="The argument dihedral_quartets needs to have 4 elements if it is a 1D array."
            )
    elif len(shape)==2:
        if shape[1]!=4:
            raise ArgumentError(
                argument="dihedral_quartets",
                value=dihedral_quartets,
                caller="molsysmt.structure.shift_dihedral_angles",
                message="The argument dihedral_quartets needs to have 4 elements in the second dimension."
            )
    else:
        raise ArgumentError(
            argument="dihedral_quartets",
            value=dihedral_quartets,
            caller="molsysmt.structure.shift_dihedral_angles",
            message="The argument dihedral_quartets needs to be a 1D or 2D array."
        )

    n_quartets = dihedral_quartets.shape[0]
    n_structures = get(molecular_system, element='system', structure_indices=structure_indices, n_structures=True)

    shifts_units = puw.get_unit(shifts)
    shifts_value = puw.get_value(shifts)

    if type(shifts_value) in [float]:
        if (n_quartets==1 and n_structures==1):
            shifts_value = np.array([[shifts_value]], dtype=float)
        else:
            raise ArgumentLengthError(
                argument="shifts",
                expected=(n_structures, n_quartets),
                actual=1,
                caller="molsysmt.structure.shift_dihedral_angles",
                message="shifts do not match the number of frames and quartets"
            )
    elif type(shifts_value) in [list,tuple]:
        shifts_value = np.array(shifts_value, dtype=float)
    elif type(shifts_value) is np.ndarray:
        pass
    else:
        raise ArgumentError(
            argument="shifts",
            value=shifts,
            caller="molsysmt.structure.shift_dihedral_angles"
        )

    shape = shifts_value.shape

    if len(shape)==1:
        shifts_value = shifts_value.reshape([n_structures, n_quartets])

    shifts=shifts_value*shifts_units

    angles = get_dihedral_angles(molecular_system, dihedral_quartets=dihedral_quartets,
            structure_indices=structure_indices, pbc=pbc)
    angles = angles + shifts

    return set_dihedral_angles(molecular_system, dihedral_quartets=dihedral_quartets, angles=angles, blocks=None,
                               structure_indices=structure_indices, pbc=pbc, in_place=in_place,
                               engine=engine)

