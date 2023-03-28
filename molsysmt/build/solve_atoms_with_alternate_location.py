from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

@digest()
def solve_atoms_with_alternate_location(molecular_system, selection='all',
        structure_indices='all', location_id='occupancy', syntax='MolSysMT'):

    from molsysmt import get, set, select

    alt_loc_dict = get(molecular_system, alternate_location=True)

    if is_all(structure_indices):

        n_structures = get(molecular_system, n_structures=True)
        structure_indices = np.arange(n_structures)

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)
    n_atoms = atom_indices.shape[0]

    if isinstance(location_id, str):
        if len(location_id)==1:
            location_id = [location_id for ii in range(n_atoms)]

    if isinstance(location_id,(list, tuple, np.ndarray)):
        if len(location_id)!=n_atoms:
            raise ValueError()

        aux_atom_indices=[]
        aux_occupancy=[]
        aux_b_factor=[]
        aux_atom_id=[]
        aux_coordinates=[]
        for structure_index in structure_indices:
            aux2_atom_indices=[]
            aux2_occupancy=[]
            aux2_b_factor=[]
            aux2_atom_id=[]
            aux2_coordinates=[]
            for tmp_atom_index, tmp_alt_loc_value in alt_loc_dict[structure_index].items():
                if tmp_atom_index in atom_indices:
                    aux_arg = np.where(atom_indices==tmp_atom_index)[0][0]
                    arg = np.where(tmp_alt_loc_value['location_id']==location_id[aux_arg])[0][0]
                    aux2_atom_indices.append(tmp_atom_index)
                    aux2_occupancy.append(tmp_alt_loc_value['occupancy'][arg])
                    aux2_b_factor.append(tmp_alt_loc_value['b_factor'][arg])
                    aux2_atom_id.append(tmp_alt_loc_value['atom_id'][arg])
                    aux2_coordinates.append(tmp_alt_loc_value['coordinates'][arg])
            aux_atom_indices.append(aux2_atom_indices)
            aux_occupancy.append(aux2_occupancy)
            aux_b_factor.append(aux2_b_factor)
            aux_atom_id.append(aux2_atom_id)
            aux_coordinates.append(aux2_coordinates)

        for ii in range(len(aux_coordinates)):
            aux_coordinates[ii] = puw.concatenate(aux_coordinates[ii])
        aux_coordinates = puw.concatenate(aux_coordinates)

        equal_atom_indices_all_structures=False

        for tmp_atom_indices in aux_atom_indices:
            equal_atom_indices_all_structures = np.all(tmp_atom_indices==aux_atom_indices[0])
            if not equal_atom_indices_all_structures:
                break

        if equal_atom_indices_all_structures:
            set(molecular_system, element='atom', indices=aux_atom_indices[0], structure_indices=structure_indices,
                    atom_id=aux_atom_id, occupancy=aux_occupancy, b_factor=aux_b_factor, coordinates=aux_coordinates) 
        else:
            for ii in structure_indices:
                set(molecular_system, element='atom', indices=aux_atom_indices[ii], structure_indices=structure_indices[ii],
                    atom_id=aux_atom_id[ii], occupancy=aux_occupancy[ii], b_factor=aux_b_factor[ii], coordinates=aux_coordinates[ii]) 

    elif location_id=='occupancy':

        aux_atom_indices=[]
        aux_occupancy=[]
        aux_b_factor=[]
        aux_atom_id=[]
        aux_coordinates=[]
        for structure_index in structure_indices:
            aux2_atom_indices=[]
            aux2_occupancy=[]
            aux2_b_factor=[]
            aux2_atom_id=[]
            aux2_coordinates=[]
            for tmp_atom_index, tmp_alt_loc_value in alt_loc_dict[structure_index].items():
                if tmp_atom_index in atom_indices:
                    arg = np.max_arg(tmp_alt_loc_value['occupancy'])
                    aux2_atom_indices.append(tmp_atom_index)
                    aux2_occupancy.append(tmp_alt_loc_value['occupancy'][arg])
                    aux2_b_factor.append(tmp_alt_loc_value['b_factor'][arg])
                    aux2_atom_id.append(tmp_alt_loc_value['atom_id'][arg])
                    aux2_coordinates.append(tmp_alt_loc_value['coordinates'][arg])
            aux_atom_indices.append(aux2_atom_indices)
            aux_occupancy.append(aux2_occupancy)
            aux_b_factor.append(aux2_b_factor)
            aux_atom_id.append(aux2_atom_id)
            aux_coordinates.append(aux2_coordinates)

        for ii in range(len(aux_coordinates)):
            aux_coordinates = np.concatenate(aux_coordinates[ii])
        aux_coordinates = np.concatenate(aux_coordinates)

        equal_atom_indices_all_structures=False

        for tmp_atom_indices in aux_atom_indices:
            equal_atom_indices_all_structures = np.all(tmp_atom_indices, aux_atom_indices[0])
            if not equal_atom_indices_all_structures:
                break

        if equal_atom_indices_all_structures:
            set(molecular_system, element='atom', indices=aux_atom_indices[0], structure_indices=structure_indices,
                    atom_id=aux_atom_id, occupancy=aux_occupancy, b_factor=aux_b_factor, coordinates=aux_coordinates)
        else:
            for ii in structure_indices:
                set(molecular_system, element='atom', indices=aux_atom_indices[ii], structure_indices=structure_indices[ii],
                    atom_id=aux_atom_id[ii], occupancy=aux_occupancy[ii], b_factor=aux_b_factor[ii], coordinates=aux_coordinates[ii])

    pass

