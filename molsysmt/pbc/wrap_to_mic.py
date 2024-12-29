from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
from molsysmt import lib as msmlib
import numpy as np
import gc

@digest()
def wrap_to_mic(molecular_system, selection='all', structure_indices='all',
                mic_origin='[0,0,0] nanometers',
                center_of_selection=None, center_coordinates='[0,0,0] nanometers', weights=None,
                keep_covalent_bonds=False, syntax='MolSysMT', engine='MolSysMT', in_place=False,
                skip_digestion=False):
    """
    To be written soon...
    """

    if engine=='MolSysMT':

        from molsysmt.basic import select, get, set, extract, copy
        from molsysmt.structure import center

        atom_indices = select(molecular_system, selection=selection, syntax=syntax, skip_digestion=True)

        if center_of_selection is not None:

            molecular_system = center(molecular_system, selection=atom_indices,
                                      center_of_selection=center_of_selection, weights=weights,
                                      center_coordinates=center_coordinates, syntax=syntax, in_place=False,
                                      skip_digestion=True)

        coordinates= get(molecular_system, element='atom', selection=atom_indices, coordinates=True, skip_digestion=True)
        box = get(molecular_system, element='system', structure_indices=structure_indices, box=True, skip_digestion=True)

        original_length_units = puw.get_unit(coordinates)
        coordinates, length_units = puw.get_value_and_unit(coordinates, standardized=True)
        box = puw.get_value(box, standardized=True)

        n_structures = coordinates.shape[0]
        if box.shape[0]==1 and n_structures>1:
            box = np.repeat(box, repeats=n_structures, axis=0)

        mic_origin = puw.get_value(mic_origin, standardized=True)

        if np.all(np.isclose(mic_origin, 0, atol=1e-4)):
            mic_origin = np.zeros((3), dtype=np.float64)

        msmlib.pbc.wrap_to_mic(coordinates, box, mic_origin)

        coordinates=puw.quantity(coordinates, length_units)
        coordinates=puw.convert(coordinates, to_unit=original_length_units)

        del(box)

    else:

        raise NotImplementedMethodError()

    if in_place:

        set(molecular_system, selection='atom_index in @atom_indices', structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates, skip_digestion=True)

        del(coordinates, atom_indices, structure_indices)

        gc.collect()

        pass

    else:

        tmp_molecular_system = copy(molecular_system, skip_digestion=True)
        set(tmp_molecular_system, selection='atom_index in @atom_indices', structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates, skip_digestion=True)

        del(coordinates, atom_indices, structure_indices)

        gc.collect()

        return tmp_molecular_system

