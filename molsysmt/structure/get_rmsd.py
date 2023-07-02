from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import lib as msmlib
from molsysmt import pyunitwizard as puw
import numpy as np
import gc

@digest()
def get_rmsd(molecular_system, selection='atom_type!="H"', structure_indices='all',
          reference_molecular_system=None, reference_selection=None, reference_structure_indices=0,
          syntax='MolSysMT', engine='MolSysMT'):
    """
    To be written soon...
    """

    if reference_molecular_system is None:
        reference_molecular_system = molecular_system

    if reference_selection is None:
        reference_selection = selection

    if engine=='MolSysMT':

        from molsysmt.basic import select, get

        coordinates = get(molecular_system, element='atom', selection=selection,
                structure_indices=structure_indices, syntax=syntax,
                coordinates=True)

        if reference_molecular_system is None:
            reference_molecular_system = molecular_system

        if reference_selection is None:
            reference_selection = selection

        reference_coordinates = get(reference_molecular_system, element='atom', selection=reference_selection,
                structure_indices=reference_structure_indices, syntax=syntax,
                coordinates=True)

        coordinates, length_unit = puw.get_value_and_unit(coordinates)
        reference_coordinates = puw.get_value(reference_coordinates, to_unit=length_unit)

        if coordinates.shape[1]!=reference_coordinates.shape[1]:
            raise ValueError("reference selection and selection needs to have the same number of atoms")

        if coordinates.shape[0]==1 and reference_coordinates.shape[0]>1:
            rmsd_val = msmlib.structure.get_rmsd_with_single_reference_structure(reference_coordinates, coordinates[0])
        elif coordinates.shape[0]>1 and reference_coordinates.shape[0]==1:
            rmsd_val = msmlib.structure.get_rmsd_with_single_reference_structure(coordinates, reference_coordinates[0])
        else:
            rmsd_val = msmlib.structure.get_rmsd(coordinates, reference_coordinates)

        rmsd_val = puw.quantity(rmsd_val, length_unit, standardized=True)

        del(coordinates, reference_coordinates, length_unit)
        gc.collect()

        return rmsd_val

    else:

        raise NotImplementedMethodError()

