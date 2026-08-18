from molsysmt._private.smonitor import NotImplementedMethodError
from smonitor import signal
from molsysmt._private.argdigest import arg_digest
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
        Molecular system in any supported MolSysMT format.
    dihedral_quartets : object, default=None
        Argument dihedral_quartets.
    angles : object, default=None
        Argument angles.
    blocks : object, default=None
        Argument blocks.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    pbc : bool, default=True
        Whether to take periodic boundary conditions into account.
    in_place : object, default=False
        Argument in_place.
    engine : object, default='MolSysMT'
        Argument engine.

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
