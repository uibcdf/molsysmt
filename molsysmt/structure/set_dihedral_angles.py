from molsysmt._private.smonitor import NotImplementedMethodError
from smonitor import signal
from molsysmt._private.arg_digestion import arg_digest
import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private import rust_backend as _kernels
from molsysmt.lib.structure._kernel_inputs import extract_coordinates_value_and_unit
import gc

@signal(tags=['api', 'structure'])
@arg_digest()
def set_dihedral_angles(molecular_system, dihedral_quartets=None, angles=None, blocks=None,
        structure_indices='all', pbc=True, in_place=False, engine='MolSysMT'):
    """
    Set dihedral angles to specified target values by rotating covalent blocks.

    For each dihedral quartet ``(i, j, k, l)``, the function determines which
    atoms form a covalently connected block on the side of atom ``l`` after the
    bond ``j-k`` is removed.  That block is then rotated about the ``j-k`` axis
    so that the dihedral angle reaches the target value.

    When ``pbc=True`` and the system has a periodic box the minimum-image
    dihedral kernel is used; otherwise the standard (non-periodic) kernel is
    applied.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any form supported by MolSysMT.
    dihedral_quartets : numpy.ndarray of shape (n_quartets, 4)
        Global atom indices defining each dihedral angle to be set.  Each row
        contains four atom indices ``[i, j, k, l]``.
    angles : quantity
        Target dihedral angle values as a PyUnitWizard angle quantity.  The array
        must be compatible with shape ``(n_structures, n_quartets)``.  Values are
        internally converted to radians.
    blocks : list of sets or None, default None
        Pre-computed covalent blocks (one per quartet) used to determine which
        atoms move.  When ``None``, the blocks are computed on-the-fly for every
        quartet by calling ``molsysmt.topology.get_covalent_blocks`` with the
        relevant bond removed.  Providing pre-computed blocks avoids redundant
        topology traversals when calling this function in a loop.
    structure_indices : 'all' or array-like, default 'all'
        Frame indices over which the operation is performed.
    pbc : bool, default True
        Use the minimum-image dihedral kernel when the system has a periodic box.
    in_place : bool, default False
        If ``True`` the molecular system is modified in-place and ``None`` is
        returned.  If ``False`` a new copy is returned with the updated
        coordinates.
    engine : {'MolSysMT'}, default 'MolSysMT'
        Backend used for the dihedral rotation kernels.

    Returns
    -------
    molecular system or None
        A new molecular system with the updated dihedral angles when
        ``in_place=False``; ``None`` when ``in_place=True``.

    Raises
    ------
    NotImplementedMethodError
        If an unsupported engine is requested.

    .. versionadded:: 1.0.0
    """

    if engine=='MolSysMT':

        from molsysmt.basic import get, convert, set, copy
        from molsysmt.topology.get_covalent_blocks import get_covalent_blocks

        coordinates = get(molecular_system, element='system', structure_indices=structure_indices,
                coordinates=True)
        coordinates, length_unit = extract_coordinates_value_and_unit(coordinates)

        angles = np.asarray(puw.get_value(angles, to_unit='radians'), dtype=np.float64)

        n_quartets = dihedral_quartets.shape[0]
        on_in_blocks = np.zeros((n_quartets, coordinates.shape[1]), dtype=np.bool_)

        if blocks is None:
            for ii in range(n_quartets):
                blocks = get_covalent_blocks(molecular_system, remove_bonds=[dihedral_quartets[ii,1],dihedral_quartets[ii,2]])
                for block in blocks:
                    if dihedral_quartets[ii,3] in block:
                        on_in_blocks[ii,list(block)] = True
        else:
            for ii in range(n_quartets):
                for block in blocks:
                    if dihedral_quartets[ii,3] in block:
                        on_in_blocks[ii,list(block)] = True

        if pbc:

            box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)

            if box is not None:
                if box[0] is not None:
                    box = np.asarray(puw.get_value(box, to_unit=length_unit), dtype=np.float64)
                    _kernels.set_mic_dihedral_angles(coordinates, box, angles, dihedral_quartets,
                            on_in_blocks)
                    del(box, dihedral_quartets, angles, blocks, on_in_blocks)
                else:
                    pbc = False
            else:
                pbc = False

        if not pbc:

            _kernels.set_dihedral_angles(coordinates, angles, dihedral_quartets, on_in_blocks)

            del(dihedral_quartets, angles, blocks, on_in_blocks)

        coordinates = puw.quantity(coordinates, length_unit)

        if in_place:
            set(molecular_system, structure_indices=structure_indices, coordinates=coordinates)
            del(coordinates)
            gc.collect()
        else:
            tmp_molecular_system = copy(molecular_system)
            set(tmp_molecular_system, structure_indices=structure_indices, coordinates=coordinates)
            del(coordinates)
            gc.collect()
            return tmp_molecular_system

    else:

        raise NotImplementedMethodError()
