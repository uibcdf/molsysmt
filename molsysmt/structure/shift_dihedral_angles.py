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
    Shift (increment/decrement) dihedral angles by specified amounts.

    Reads the current dihedral angles with ``get_dihedral_angles``, adds the
    requested shifts, and writes the result back with ``set_dihedral_angles``.
    All covalent-block detection and PBC handling are delegated to
    ``set_dihedral_angles``.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any form supported by MolSysMT.
    dihedral_quartets : list, tuple or numpy.ndarray of shape (n_quartets, 4)
        Global atom indices defining each dihedral angle.  Each row contains
        four indices ``[i, j, k, l]``.  A 1-D array of length 4 is accepted
        and automatically reshaped to ``(1, 4)``.
    shifts : quantity or array-like
        Angular increments to apply as a PyUnitWizard angle quantity.  Broadcast
        rules:

        * A scalar float is accepted only when both ``n_quartets`` and
          ``n_structures`` are 1.
        * A 1-D array of length ``n_quartets`` is reshaped to
          ``(n_structures, n_quartets)``.
        * A 2-D array of shape ``(n_structures, n_quartets)`` is used directly.
    blocks : list of sets or None, default None
        Pre-computed covalent blocks passed through to ``set_dihedral_angles``.
        When ``None`` the blocks are computed on-the-fly.
    structure_indices : 'all' or array-like, default 'all'
        Frame indices over which the operation is performed.
    pbc : bool, default True
        Apply minimum-image convention when the system has a periodic box.
    in_place : bool, default False
        If ``True`` the molecular system is modified in-place and ``None`` is
        returned.  If ``False`` a new copy is returned with the updated
        coordinates.
    engine : {'MolSysMT'}, default 'MolSysMT'
        Backend used for the dihedral rotation kernels.
    skip_digestion : bool, default False
        Whether to skip argument digestion (for internal use on trusted hot paths).

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

