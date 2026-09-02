from molsysmt._private.argdigest import arg_digest
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
    Shift (increment/decrement) dihedral angles by specified amounts.

    Reads the current dihedral angles with ``get_dihedral_angles``, adds the
    requested shifts, and writes the result back with ``set_dihedral_angles``.
    All covalent-block detection and PBC handling are delegated to
    ``set_dihedral_angles``.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    dihedral_quartets : list, tuple, numpy.ndarray, or None, default=None
        Zero-based atom-index quartets defining the dihedral angles.
    shifts : PyUnitWizard quantity or None, default=None
        Angular increments applied to the current dihedral angles.
    blocks : list, tuple, numpy.ndarray, or None, default=None
        Atom-index blocks that move together when changing each dihedral.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    pbc : bool, default=True
        Whether to take periodic boundary conditions into account.
    in_place : bool, default=False
        Whether to modify the input molecular system in place.
    engine : str, default='MolSysMT'
        Backend used to perform the calculation.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molecular system or None
        A new molecular system with the shifted dihedral angles when
        ``in_place=False``; ``None`` when ``in_place=True``.


    Raises
    ------
    ArgumentError
        If ``dihedral_quartets`` is not an array-like object, does not have 4
        elements in a 1-D case, or does not have shape ``(n, 4)`` in the 2-D
        case.
    ArgumentLengthError
        If a scalar ``shifts`` value is provided but there is more than one
        frame or quartet.


    .. versionadded:: 1.0.0
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
            dihedral_quartets=dihedral_quartets.reshape([1,4])
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
