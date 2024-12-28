from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
from molsysmt import lib as msmlib
import numpy as np
import gc

@digest()
def wrap_to_pbc(molecular_system, selection='all', structure_indices='all',
                box_origin='[0,0,0] nanometers', box_center=None,
                center_of_selection=None, weights=None, center_coordinates='[0,0,0] nanometers',
                keep_covalent_bonds=False, syntax='MolSysMT', engine='MolSysMT', in_place=False,
                skip_digestion=False):
    """
    To be written soon...
    """

    if engine=='MolSysMT':

        from molsysmt.basic import select, get, set, extract, copy
        from molsysmt.structure import center

        atom_indices = select(molecular_system, selection=selection, syntax=syntax)

        if center_of_selection is not None:

            molecular_system = center(molecular_system, selection=atom_indices,
                                      center_of_selection=center_of_selection, weight=weight,
                                      center_coordinates=center_coordinates, syntax=syntax, in_place=False,
                                      skip_digestion=True)

        coordinates= get(molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                         coordinates=True)
        box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)

        original_length_units = puw.get_unit(coordinates)
        coordinates, length_units = puw.get_value_and_unit(coordinates, standardized=True)
        box = puw.get_value(box, standardized=True)

        n_structures = coordinates.shape[0]
        if box.shape[0]==1 and n_structures>1:
            box = np.repeat(box, repeats=n_structures, axis=0)

        if box_center is None:

            box_origin = puw.get_value(box_origin, standardized=True)

            if np.all(np.isclose(box_origin, 0, atol=1e-4)):
                box_origin = np.zeros((3), dtype=np.float64)

            msmlib.pbc.wrap_to_pbc(coordinates, box, box_origin)

        else:

            raise NotImplementedError

        coordinates=puw.quantity(coordinates, length_units)
        coordinates=puw.convert(coordinates, to_unit=original_length_units)

        del(box)

    else:

        raise NotImplementedMethodError()



    if in_place:

        set(molecular_system, selection='atom_index in @atom_indices', structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates)

        del(coordinates, atom_indices, structure_indices)

        gc.collect()

        pass

    else:

        tmp_molecular_system = copy(molecular_system)
        set(tmp_molecular_system, selection='atom_index in @atom_indices', structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates)

        del(coordinates, atom_indices, structure_indices)

        gc.collect()

        return tmp_molecular_system

