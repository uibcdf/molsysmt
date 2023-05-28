from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import lib as msmlib
from molsysmt import pyunitwizard as puw
import numpy as np
import gc

@digest()
def get_distances(molecular_system, selection="all", groups_of_atoms=None, group_behavior=None, structure_indices="all",
             molecular_system_2=None, selection_2=None, groups_of_atoms_2=None, group_behavior_2=None, structure_indices_2=None,
             pairs=False, pbc=True, engine='MolSysMT', syntax='MolSysMT'):
    """get_distances(item, to_form='molsysmt.MolSys', selection='all', structure_indices='all', syntax='MolSysMT', **kwargs)

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

    # group_behavior in
    # ['center_of_mass','geometric_center','minimum_distance','maximum_distance']
    # output in ['numpy.ndarray','dictionary']

    if engine=='MolSysMT':

        from molsysmt.basic import get
        from molsysmt.file import is_file

        in_memory = True
        if is_file(molecular_system):
            in_memory = False

        if in_memory:
            if is_file(molecular_system_2):
                in_memory = False

        if in_memory:

            output = _get_distances_in_memory(molecular_system,
                    selection=selection, groups_of_atoms=groups_of_atoms,
                    group_behavior=group_behavior, structure_indices=structure_indices,
                    molecular_system_2=molecular_selection_2, selection_2=selection_2,
                    groups_of_atoms_2=groups_of_atoms_2, group_behavior_2=group_behavior_2,
                    structure_indices_2=structure_indices_2,
                    pairs=pairs, pbc=pbc, syntax=syntax)

        else:

            raise NotImplementedMethodError

    else:

        raise NotImplementedMethodError

    return output

def _get_distances_in_memory(molecular_system, selection="all", groups_of_atoms=None, group_behavior=None, structure_indices="all",
        molecular_system_2=None, selection_2=None, groups_of_atoms_2=None, group_behavior_2=None, structure_indices_2=None,
        pairs=False, pbc=True, aux_dict=False, syntax='MolSysMT'):


    from molsysmt.basic import select, get

    if molecular_system_2 is None:
        molecular_system_2 = molecular_system

    if structure_indices_2 is None:
        structure_indices_2 = structure_indices_1

    if group_behavior is None:
        coordinates = get(molecular_system, element='atom', selection=selection,
                          structure_indices=structure_indices, syntax=syntax,
                          coordinates=True)
    else:

        if group_behavior == 'center_of_mass':
            coordinates = get_center_of_mass(molecular_system, selection=selection,
                    groups_of_atoms=groups_of_atoms, structure_indices=structure_indices)

        elif group_behavior == 'geometric_center':
            coordinates= get_geometric_center(molecular_system, selection=selection,
                    groups_of_atoms=groups_of_atoms, structure_indices=structure_indices)

        elif group_behavior == 'closest':
            raise NotImplementedError

        elif group_behavior == 'farthest':
            raise NotImplementedError

        else:
            raise NotImplementedError

    if group_behavior_2 is None:

        if selection_2 is None:
            coordinates_2 = None

        else:
            coordinates_2 = get(molecular_system_2, element='atom', selection=selection_2,
                            structure_indices=structure_indices_2, syntax=syntax,
                            coordinates=True)
    else:

        if group_behavior_2 == 'center_of_mass':
            coordinates_2 = get_center_of_mass(molecular_system_2, selection=selection_2,
                    groups_of_atoms=groups_of_atoms_2, structure_indices=structure_indices_2)

        elif group_behavior == 'geometric_center':
            coordinates_2= get_geometric_center(molecular_system_2, selection=selection_2,
                    groups_of_atoms=groups_of_atoms_2, structure_indices=structure_indices_2)

        elif group_behavior == 'closest':
            raise NotImplementedError

        elif group_behavior == 'farthest':
            raise NotImplementedError

        else:
            raise NotImplementedError


    if not pairs:

        if coordinates_2 is None:

            length_unit, coordinates = puw.get_unit_and_value(coordinates)

            if pbc:
                box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)
                if box is not None:
                    if box[0] is not None:
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

            length_unit, coordinates = puw.get_unit_and_value(coordinates)
            coordinates_2 = puw.get_unit_and_value(coordinates, to_unit=length_unit)

            if pbc:
                box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)
                if box is not None:
                    if box[0] is not None:
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

        length_unit, coordinates = puw.get_unit_and_value(coordinates)
        coordinates_2 = puw.get_unit_and_value(coordinates, to_unit=length_unit)

        if pbc:
            box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)
            if box is not None:
                if box[0] is not None:
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


