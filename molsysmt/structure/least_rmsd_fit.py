from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np
from molsysmt import lib as msmlib
from molsysmt import pyunitwizard as puw
import gc

@digest()
def least_rmsd_fit(molecular_system=None, selection='all', selection_fit='atom_type!="H"', structure_indices='all',
        reference_molecular_system=None, reference_selection_fit=None, reference_structure_index=0,
        to_form=None, in_place=False, syntax='MolSysMT', engine='MolSysMT'):
    """
    To be written soon...
    """

    if engine=='MolSysMT':

        from molsysmt.basic import select, get, copy, convert
        from . import rotate, translate

        coordinates = get(molecular_system, element='atom', selection=selection_fit,
                structure_indices=structure_indices, syntax=syntax, coordinates=True)

        if reference_molecular_system is None:
            reference_molecular_system = molecular_system

        if reference_selection_fit is None:
            reference_selection_fit = selection_fit

        reference_coordinates = get(reference_molecular_system, element='atom',
                selection=reference_selection_fit, structure_indices=reference_structure_index,
                syntax=syntax, coordinates=True)

        coordinates, length_unit = puw.get_value_and_unit(coordinates)
        reference_coordinates = puw.get_value(reference_coordinates, to_unit=length_unit)

        if coordinates.shape[1]!=reference_coordinates.shape[1]:
            raise ValueError("reference selection and selection needs to have the same number of atoms")

        if coordinates.shape[0]==1 and reference_coordinates.shape[0]>1:
            rotation_center, rotation, translation = \
                    msmlib.structure.get_least_rmsd_rotation_and_translation_with_single_reference_structure(
                        reference_coordinates, coordinates[0])
        elif coordinates.shape[0]>1 and reference_coordinates.shape[0]==1:
            rotation_center, rotation, translation = \
                    msmlib.structure.get_least_rmsd_rotation_and_translation_with_single_reference_structure(
                        coordinates, reference_coordinates[0])
        else:
            rotation_center, rotation, translation = msmlib.structure.get_least_rmsd_rotation_and_translation(
                coordinates, reference_coordinates)

        rotation_center = puw.quantity(rotation_center, length_unit, standardized=True)
        translation = puw.quantity(translation, length_unit, standardized=True)

        del(coordinates, reference_coordinates)

        if in_place:

            rotate(molecular_system, rotation=rotation, rotation_center=rotation_center,
                   selection=selection, structure_indices=structure_indices,
                   syntax=syntax, in_place=True)

            translate(molecular_system, translation=translation,
                   selection=selection, structure_indices=structure_indices,
                   syntax=syntax, in_place=True)

            del(rotation, rotation_center, translation)
            gc.collect()

        else:

            tmp_molecular_system = copy(molecular_system)

            rotate(tmp_molecular_system, rotation=rotation, rotation_center=rotation_center,
                   selection=selection, structure_indices=structure_indices,
                   syntax=syntax, in_place=True)

            translate(tmp_molecular_system, translation=translation,
                   selection=selection, structure_indices=structure_indices,
                   syntax=syntax, in_place=True)

            del(rotation, rotation_center, translation)
            gc.collect()

            if to_form is None:
                return tmp_molecular_system
            else:
                tmp_molecular_system = convert(tmp_molecular_system, to_form=to_form)
                return tmp_molecular_system

    else:

        raise NotImplementedMethodError()

