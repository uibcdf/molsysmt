from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import lib as msmlib
from molsysmt import pyunitwizard as puw
import numpy as np

@digest()
def get_rmsd(molecular_system, selection='backbone', structure_indices='all',
          reference_molecular_system=None, reference_selection=None, reference_structure_index=0,
          syntax='MolSysMT', engine='MolSysMT'):

    if reference_molecular_system is None:
        reference_molecular_system = molecular_system

    if reference_selection is None:
        reference_selection = selection

    if engine=='MolSysMT':

        from molsysmt.basic import select, get

        n_atoms = get(molecular_system, element='atom', selection=selection, syntax=syntax, n_atoms=True)
        n_reference_atoms = get(reference_molecular_system, element='atom', selection=reference_selection,
                                syntax=syntax, n_atoms=True)

        if n_atoms!=n_reference_atoms:
            raise ValueError("reference selection and selection needs to have the same number of atoms")

        coordinates = get(molecular_system, selection=selection, structure_indices=structure_indices,
                          syntax=syntax, coordinates=True)

        reference_coordinates = get(reference_molecular_system, selection=reference_selection,
                                    structure_indices=reference_structure_index, syntax=syntax,
                                    coordinates=True)

        coordinates_value, coordinates_unit = puw.get_value_and_unit(coordinates)
        reference_coordinates_value, reference_coordinates_unit = puw.get_value_and_unit(reference_coordinates)

        rmsd_val = msmlib.structure.rmsd(coordinates, reference_coordinates)
        rmsd_val = puw.quantity(rmsd_val, coordinates_unit, standardize=True)

        return rmsd_val

    else:

        raise NotImplementedMethodError()

