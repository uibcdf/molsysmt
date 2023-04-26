from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np
from molsysmt.lib import rmsd as librmsd
from molsysmt import pyunitwizard as puw

@digest()
def get_rmsd(molecular_system, selection='backbone', structure_indices='all',
          reference_molecular_system=None, reference_selection=None, reference_structure_index=0,
          syntax='MolSysMT', engine='MolSysMT'):

    if engine=='MolSysMT':

        from molsysmt.basic import select, get

        if reference_molecular_system is None:
            reference_molecular_system = molecular_system

        if reference_selection is None:
            reference_selection = selection

        coordinates = get(molecular_system, selection=selection, structure_indices=structure_indices,
                          syntax=syntax, coordinates=True)

        reference_coordinates = get(reference_molecular_system, selection=reference_selection,
                                    structure_indices=reference_structure_index, syntax=syntax,
                                    coordinates=True)

        coordinates_value, coordinates_unit = puw.get_value_and_unit(coordinates)
        reference_coordinates_value, reference_coordinates_unit = puw.get_value_and_unit(reference_coordinates)

        rmsd_val = librmsd.rmsd(coordinates, atom_indices, reference_coordinates, structure_indices,
                                 n_atoms, n_structures, n_atom_indices, n_structure_indices)

        rmsd_val = puw.quantity(rmsd_val, coordinates_unit, standardize=True)

        return rmsd_val

    else:

        raise NotImplementedMethodError()

