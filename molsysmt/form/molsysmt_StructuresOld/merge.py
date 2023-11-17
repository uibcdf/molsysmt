from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
from copy import deepcopy

@digest(form='molsysmt.Structures')
def merge(items, atom_indices='all', structure_indices='all'):

    from molsysmt.native import Structures

    n_items = len(items)

    output = Structures()


    if is_all(atom_indices):
        atom_indices = ['all' for ii in range(n_items)]

    if is_all(structure_indices):
        structure_indices = ['all' for ii in range(n_items)]

    if len(atom_indices)!=n_items:
        raise ValueError(atom_indices)

    if len(structure_indices)!=n_items:
        raise ValueError(structure_indices)

    if is_all(structure_indices[0]):
        output.n_structures = items[0].n_structures
        output.box = deepcopy(items[0].box)
        output.structure_id = deepcopy(items[0].structure_id)
        output.time = deepcopy(items[0].time)
    else:
        output.n_structures = len(structure_indices)
        output.box = items[0].box[structure_indices,:,:]
        output.structure_id = items[0].structure_id[structure_indices]
        output.time = items[0].time[structure_indices]


    output.alternate_location = [{} for ii in range(output.n_structures)]

    with_alternate_location = False

    list_n_atoms = []
    list_coordinates = []
    list_velocities = []
    list_b_factor = []
    list_occupancy = []

    count_n_atoms=0

    for aux_item, aux_atom_indices, aux_structure_indices in zip(items, atom_indices, structure_indices):

        if is_all(aux_structure_indices):
            if is_all(aux_atom_indices):

                aux_n_atoms = aux_item.n_atoms

                if aux_n_atoms > 0:

                    if output.n_structures!=aux_item.n_structures:
                        raise ValueError()

                    list_coordinates.append(aux_item.coordinates)
                    list_velocities.append(aux_item.velocities)
                    list_b_factor.append(aux_item.b_factor)
                    list_occupancy.append(aux_item.occupancy)

                    if aux_item.alternate_location is not None:
                        for ii, alt_loc_dict in enumerate(aux_item.alternate_location):
                            if alt_loc_dict is not None:
                                for key, value in alt_loc_dict.items():
                                    output.alternate_location[ii][key+count_n_atoms]=value
            else:

                aux_n_atoms = len(aux_atom_indices)

                if aux_n_atoms > 0:

                    if output.n_structures!=aux_item.n_structures:
                        raise ValueError()

                    if aux_item.coordinates is not None:
                        list_coordinates.append(aux_item.coordinates[:,aux_atom_indices,:])
                    else:
                        list_coordinates.append(None)

                    if aux_item.velocities is not None:
                        list_velocities.append(aux_item.velocities[:,aux_atom_indices,:])
                    else:
                        list_velocities.append(None)

                    if aux_item.b_factor is not None:
                        list_b_factor.append(aux_item.b_factor[:,aux_atom_indices])
                    else:
                        list_b_factor.append(None)

                    if aux_item.occupancy is not None:
                        list_occupancy.append(aux_item.occupancy[:,aux_atom_indices])
                    else:
                        list_occupancy.append(None)

                    if aux_item.alternate_location is not None:
                        for ii, alt_loc_dict in enumerate(aux_item.alternate_location):
                            if alt_loc_dict is not None:
                                for key, value in alt_loc_dict.items():
                                    output.alternate_location[ii][key+count_n_atoms]=value

        else:

            aux_n_structure_indices = len(aux_structure_indices)

            if aux_n_structure_indices > 0:

                if is_all(aux_atom_indices):

                    aux_n_atoms = aux_item.n_atoms

                    if aux_n_atoms > 0:

                        if output.n_structures!=aux_item.n_structures:
                            raise ValueError()

                        if aux_item.coordinates is not None:
                            list_coordinates.append(aux_item.coordinates[aux_structure_indices,:,:])
                        else:
                            list_coordinates.append(None)

                        if aux_item.velocities is not None:
                            list_velocities.append(aux_item.velocities[aux_structure_indices,:,:])
                        else:
                            list_velocities.append(None)

                        if aux_item.b_factor is not None:
                            list_b_factor.append(aux_item.b_factor[aux_structure_indices,:])
                        else:
                            list_b_factor.append(None)

                        if aux_item.occupancy is not None:
                            list_occupancy.append(aux_item.occupancy[aux_structure_indices,:])
                        else:
                            list_occupancy.append(None)

                        if aux_item.alternate_location is not None:
                            for ii, alt_loc_dict in enumerate(aux_item.alternate_location):
                                if alt_loc_dict is not None:
                                    for key, value in alt_loc_dict.items():
                                        output.alternate_location[ii][key+count_n_atoms]=value

                else:

                    aux_n_atoms = len(aux_atom_indices)

                    if aux_n_atoms > 0:

                        if output.n_structures!=aux_item.n_structures:
                            raise ValueError()

                        if aux_item.coordinates is not None:
                            tmp = aux_item.coordinates[aux_structure_indices,:,:]
                            list_coordinates.append(tmp[:,aux_atom_indices,:])
                            del(tmp)
                        else:
                            list_coordinates.append(None)

                        if aux_item.velocities is not None:
                            tmp = aux_item.velocities[aux_structure_indices,:,:]
                            list_velocities.append(tmp[:,aux_atom_indices,:])
                        else:
                            list_velocities.append(None)

                        if aux_item.b_factor is not None:
                            tmp = aux_item.b_factor[aux_structure_indices,:]
                            list_b_factor.append(tmp[:,aux_atom_indices])
                        else:
                            list_b_factor.append(None)

                        if aux_item.occupancy is not None:
                            tmp = aux_item.occupancy[aux_structure_indices,:]
                            list_occupancy.append(tmp[:,aux_atom_indices])
                        else:
                            list_occupancy.append(None)

                        if aux_item.alternate_location is not None:
                            for ii, alt_loc_dict in enumerate(aux_item.alternate_location):
                                if ii in aux_structure_indices:
                                    if alt_loc_dict is not None:
                                        for key, value in alt_loc_dict.items():
                                            output.alternate_location[ii][key+count_n_atoms]=value



        count_n_atoms += aux_n_atoms

    if any([ii is None for ii in list_coordinates]):
        output.coordinates = None
    else:
        output.coordinates = puw.hstack(list_coordinates)

    if any([ii is None for ii in list_velocities]):
        output.velocities = None
    else:
        output.velocities = puw.hstack(list_velocities)

    if any([ii is None for ii in list_b_factor]):
        output.b_factor = None
    else:
        output.b_factor = puw.hstack(list_b_factor)

    if any([ii is None for ii in list_occupancy]):
        output.occupancy = None
    else:
        output.occupancy = np.hstack(list_occupancy)

    del(list_coordinates, list_velocities, list_b_factor, list_occupancy)

    output.n_atoms = count_n_atoms

    return output

