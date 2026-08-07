from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt._private.variables import is_all, is_iterable
from molsysmt import pyunitwizard as puw
import numpy as np
from copy import deepcopy

@arg_digest(form='molsysmt.Structures')
def merge(items, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import Structures

    n_items = len(items)

    if n_items == 0:
        return Structures()

    output = Structures()

    if is_all(atom_indices):
        atom_indices = ['all' for ii in range(n_items)]

    if is_all(structure_indices):
        structure_indices = ['all' for ii in range(n_items)]

    if len(atom_indices)!=n_items:
        raise ArgumentError("atom_indices", value=atom_indices, caller="molsysmt.form.molsysmt_Structures.merge")

    if len(structure_indices)!=n_items:
        raise ArgumentError("structure_indices", value=structure_indices, caller="molsysmt.form.molsysmt_Structures.merge")

    # We need to set n_structures before checking it
    first_structure_indices = structure_indices[0]
    if is_all(first_structure_indices):
        n_structures = items[0].n_structures
        output.box = deepcopy(items[0].box)
        output.structure_id = deepcopy(items[0].structure_id)
        output.time = deepcopy(items[0].time)
    else:
        n_structures = len(first_structure_indices)
        output.box = None if items[0].box is None else items[0].box[first_structure_indices,:,:]
        output.structure_id = None if items[0].structure_id is None else items[0].structure_id[first_structure_indices]
        output.time = None if items[0].time is None else items[0].time[first_structure_indices]

    output.alternate_location = [{} for ii in range(n_structures)]

    with_alternate_location = False

    list_n_atoms = []
    list_coordinates = []
    list_velocities = []
    list_b_factor = []

    count_n_atoms=0

    for aux_item, aux_atom_indices, aux_structure_indices in zip(items, atom_indices, structure_indices):

        if is_all(aux_structure_indices):
            
            aux_n_atoms = aux_item.n_atoms if is_all(aux_atom_indices) else len(aux_atom_indices)

            if aux_n_atoms > 0:

                if n_structures != aux_item.n_structures:
                    raise StructuralInconsistencyError(reason=f"Inconsistent number of structures: {n_structures} vs {aux_item.n_structures}", caller="molsysmt.form.molsysmt_Structures.merge")

                if is_all(aux_atom_indices):
                    list_coordinates.append(aux_item.coordinates)
                    list_velocities.append(aux_item.velocities)
                    list_b_factor.append(aux_item.b_factor)
                else:
                    list_coordinates.append(aux_item.coordinates[:,aux_atom_indices,:] if aux_item.coordinates is not None else None)
                    list_velocities.append(aux_item.velocities[:,aux_atom_indices,:] if aux_item.velocities is not None else None)
                    list_b_factor.append(aux_item.b_factor[:,aux_atom_indices] if aux_item.b_factor is not None else None)

                if aux_item.alternate_location is not None:
                    for ii, alt_loc_dict in enumerate(aux_item.alternate_location):
                        if alt_loc_dict is not None:
                            for key, value in alt_loc_dict.items():
                                output.alternate_location[ii][key+count_n_atoms]=value
        else:

            aux_n_structure_indices = len(aux_structure_indices)

            if aux_n_structure_indices > 0:
                
                if n_structures != aux_n_structure_indices:
                     raise StructuralInconsistencyError(reason=f"Inconsistent number of structures: {n_structures} vs {aux_n_structure_indices}", caller="molsysmt.form.molsysmt_Structures.merge")

                aux_n_atoms = aux_item.n_atoms if is_all(aux_atom_indices) else len(aux_atom_indices)

                if aux_n_atoms > 0:

                    if is_all(aux_atom_indices):
                        list_coordinates.append(aux_item.coordinates[aux_structure_indices,:,:] if aux_item.coordinates is not None else None)
                        list_velocities.append(aux_item.velocities[aux_structure_indices,:,:] if aux_item.velocities is not None else None)
                        list_b_factor.append(aux_item.b_factor[aux_structure_indices,:] if aux_item.b_factor is not None else None)
                    else:
                        tmp = aux_item.coordinates[aux_structure_indices,:,:] if aux_item.coordinates is not None else None
                        list_coordinates.append(tmp[:,aux_atom_indices,:] if tmp is not None else None)
                        tmp = aux_item.velocities[aux_structure_indices,:,:] if aux_item.velocities is not None else None
                        list_velocities.append(tmp[:,aux_atom_indices,:] if tmp is not None else None)
                        tmp = aux_item.b_factor[aux_structure_indices,:] if aux_item.b_factor is not None else None
                        list_b_factor.append(tmp[:,aux_atom_indices] if tmp is not None else None)

                    if aux_item.alternate_location is not None:
                        for ii, alt_loc_idx in enumerate(aux_structure_indices):
                            alt_loc_dict = aux_item.alternate_location[alt_loc_idx]
                            if alt_loc_dict is not None:
                                for key, value in alt_loc_dict.items():
                                    output.alternate_location[ii][key+count_n_atoms]=value

        count_n_atoms += aux_n_atoms

    if any([ii is None for ii in list_coordinates]):
        output.coordinates = None
    else:
        output.coordinates = puw.utils.numpy.hstack(list_coordinates)

    if any([ii is None for ii in list_velocities]):
        output.velocities = None
    else:
        output.velocities = puw.utils.numpy.hstack(list_velocities)

    if any([ii is None for ii in list_b_factor]):
        output.b_factor = None
    else:
        output.b_factor = puw.utils.numpy.hstack(list_b_factor)

    del(list_coordinates, list_velocities, list_b_factor)

    return output
