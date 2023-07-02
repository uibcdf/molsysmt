from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt import lib as msmlib
import gc

@digest()
def set_dihedral_angles(molecular_system, quartets=None, angles=None, blocks=None,
        structure_indices='all', pbc=True, in_place=False, engine='MolSysMT'):
    """
    To be written soon...
    """

    if engine=='MolSysMT':

        from molsysmt.basic import get, convert, set, copy
        from molsysmt.topology.get_covalent_blocks import get_covalent_blocks

        coordinates = get(molecular_system, element='system', structure_indices=structure_indices,
                coordinates=True)
        coordinates, length_unit = puw.get_value_and_unit(coordinates)

        angles = puw.get_value(angles, to_unit='radians')

        n_quartets = quartets.shape[0]
        on_in_blocks = np.zeros((n_quartets, coordinates.shape[1]), dtype=np.bool_)

        if blocks is None:
            for ii in range(n_quartets):
                blocks = get_covalent_blocks(molecular_system, remove_bonds=[quartets[ii,1],quartets[ii,2]])
                for block in blocks:
                    if quartets[ii,3] in block:
                        on_in_blocks[ii,list(block)] = True
        else:
            for ii in range(n_quartets):
                for block in blocks:
                    if quartets[ii,3] in block:
                        on_in_blocks[ii,list(block)] = True

        if pbc:

            box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)

            if box is not None:
                if box[0] is not None:
                    box = puw.get_value(box, to_unit=length_unit)
                    msmlib.structure.set_mic_dihedral_angles(coordinates, box, angles, quartets,
                            on_in_blocks)
                    del(box, quartets, angles, blocks, on_in_blocks)
                else:
                    pbc = False
            else:
                pbc = False

        if not pbc:

            msmlib.structure.set_dihedral_angles(coordinates, angles, quartets, on_in_blocks)

            del(quartets, angles, blocks, on_in_blocks)

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

