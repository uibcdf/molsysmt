from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all, is_iterable_of_iterables
from molsysmt import lib as msmlib
from molsysmt import pyunitwizard as puw
import numpy as np
import gc


@digest()
def get_distances(molecular_system, selection="all", structure_indices="all", center_of_atoms=False, weights=None,
        molecular_system_2=None, selection_2=None, structure_indices_2=None, center_of_atoms_2=False, weights_2=None,
        pairs=False, pbc=True, engine='MolSysMT', syntax='MolSysMT'):
    """
    To be written soon...

    This is a sentence

    This is a paragraph

    Parameters
    ----------

    Returns
    -------

    Examples
    --------

    See Also
    --------

    Notes
    -----

    """

    # atoms_center in
    # ['center_of_mass','geometric_center','minimum_distance','maximum_distance']
    # output in ['numpy.ndarray','dictionary']

    from molsysmt.basic import select
    from molsysmt.pbc import has_pbc

    if pbc:
        pbc=has_pbc(molecular_system)

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)

    if molecular_system_2 is not None:
        if selection_2 is None:
            selection_2 = selection
        if structure_indices_2 is None:
            structure_indices_2 = structure_indices
        atom_indices_2 = select(molecular_system_2, selection=selection_2)
    else:
        if selection_2 is not None:
            atom_indices_2 = select(molecular_system, selection=selection_2)
        else:
            atom_indices_2 = None

    if is_iterable_of_iterables(atom_indices):
        center_of_atoms = True

    if is_iterable_of_iterables(atom_indices_2):
        center_of_atoms_2 = True

    if engine=='MolSysMT':

        from molsysmt.basic import get
        from molsysmt.file import is_file

        in_memory = True
        if is_file(molecular_system):
            in_memory = False

        if in_memory:
            if molecular_system_2 is not None:
                if is_file(molecular_system_2):
                    in_memory = False

        if in_memory:

            output = _get_distances_in_memory(molecular_system, selection=atom_indices,
                    structure_indices=structure_indices, center_of_atoms=center_of_atoms, weights=weights,
                    molecular_system_2=molecular_system_2, selection_2=atom_indices_2,
                    structure_indices_2=structure_indices_2, center_of_atoms_2=center_of_atoms_2, weights_2=weights_2,
                    pairs=pairs, pbc=pbc, syntax=syntax)

        else:

            raise NotImplementedMethodError

    else:

        raise NotImplementedMethodError

    return output


def _get_distances_in_memory(molecular_system, selection="all", structure_indices="all",
        center_of_atoms=False, weights=None,
        molecular_system_2=None, selection_2=None, structure_indices_2=None,
        center_of_atoms_2=False, weights_2=None,
        pairs=False, pbc=True, aux_dict=False, syntax='MolSysMT'):

    from molsysmt.basic import get
    from .get_center import get_center

    if center_of_atoms:

        coordinates = get_center(molecular_system, selection=selection,
                structure_indices=structure_indices, weights=weights)

    else:

        coordinates = get(molecular_system, element='atom', selection=selection,
                          structure_indices=structure_indices, syntax=syntax,
                          coordinates=True)

    if center_of_atoms_2:

        if molecular_system_2 is None:

            molecular_system_2 = molecular_system

        if structure_indices_2 is None:

            structure_indices_2 = structure_indices

        coordinates_2 = get_center(molecular_system_2, selection=selection_2,
            structure_indices=structure_indices_2, weights=weights_2)

    else:

        if (selection_2 is None) and (structure_indices_2 is None):

            if molecular_system_2 is None:

                coordinates_2 = None

            else:

                structure_indices_2 = structure_indices
                selection_2 = selection

                coordinates_2 = get(molecular_system_2, element='atom', selection=selection_2,
                                    structure_indices=structure_indices_2, syntax=syntax,
                                    coordinates=True)

        else:

            if structure_indices_2 is None:

                structure_indices_2 = structure_indices

            if selection_2 is None:

                selection_2 = selection

            if molecular_system_2 is None:

                molecular_system_2 = molecular_system

            coordinates_2 = get(molecular_system_2, element='atom', selection=selection_2,
                                structure_indices=structure_indices_2, syntax=syntax,
                                coordinates=True)
    if not pairs:

        if coordinates_2 is None:

            coordinates, length_unit = puw.get_value_and_unit(coordinates)

            if pbc:
                box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)
                if box is not None:
                    if box[0] is not None:
                        box = puw.get_value(box, to_unit=length_unit)
                        distances = msmlib.structure.get_mic_distances_single_system(coordinates,
                                    box)
                        del(coordinates, box)
                    else:
                        pbc = False
                else:
                    pbc = False

            if not pbc:
                distances = msmlib.structure.get_distances_single_system(coordinates)
                del(coordinates)

            distances = puw.quantity(distances, length_unit)

        else:

            coordinates, length_unit = puw.get_value_and_unit(coordinates)
            coordinates_2 = puw.get_value(coordinates_2, to_unit=length_unit)

            if pbc:
                box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)
                if box is not None:
                    if box[0] is not None:
                        box = puw.get_value(box, to_unit=length_unit)
                        distances = msmlib.structure.get_mic_distances(coordinates,
                                    coordinates_2, box)
                        del(coordinates, coordinates_2, box)
                    else:
                        pbc = False
                else:
                    pbc = False

            if not pbc:
                distances = msmlib.structure.get_distances(coordinates, coordinates_2)
                del(coordinates, coordinates_2)

            distances = puw.quantity(distances, length_unit)

    else:

        if coordinates_2 is None:

            coordinates, length_unit = puw.get_value_and_unit(coordinates)

            if pbc:
                box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)
                if box is not None:
                    if box[0] is not None:
                        box = puw.get_value(box, to_unit=length_unit)
                        distances = msmlib.structure.get_mic_distances_pairs_single_system(coordinates,
                                    box)
                        del(coordinates, box)
                    else:
                        pbc = False
                else:
                    pbc = False

            if not pbc:
                distances = msmlib.structure.get_distances_pairs_single_system(coordinates)
                del(coordinates)

            distances = puw.quantity(distances, length_unit)

        else:

            coordinates, length_unit = puw.get_value_and_unit(coordinates)
            coordinates_2 = puw.get_value(coordinates_2, to_unit=length_unit)

            if pbc:
                box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)
                if box is not None:
                    if box[0] is not None:
                        box = puw.get_value(box, to_unit=length_unit)
                        distances = msmlib.structure.get_mic_distances_pairs(coordinates,
                                    coordinates_2, box)
                        del(coordinates, coordinates_2, box)
                    else:
                        pbc = False
                else:
                    pbc = False

            if not pbc:
                distances = msmlib.structure.get_distances_pairs(coordinates, coordinates_2)
                del(coordinates, coordinates_2)

            distances = puw.quantity(distances, length_unit)

    distances = puw.standardize(distances)

    gc.collect()

    return distances


