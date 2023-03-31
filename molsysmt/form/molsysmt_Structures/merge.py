from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='molsysmt.Structures')
def merge(items, atom_indices='all', atom_indices='all', structure_indices='all'):

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

    list_n_atoms = []
    list_n_structures = []
    list_structure_id = []
    list_time = []
    list_coordinates = []
    list_velocities = []
    list_box = []
    list_b_factor = []
    list_alternate_location = []
    list_bioassembly = []

    n_structures_0 = items[0].n_structures

    count_n_atoms=0

    for aux_item, aux_atom_indices, aux_structure_indices in zip(items, atom_indices, structure_indices):

        if is_all(aux_structure_indices):
            if is_all(aux_atom_indices):

                if n_structures_0!=aux_item.n_structures:
                    raise ValueError()

                list_n_atoms.append(aux_item.n_atoms)
                list_coordinates.append(aux_item.coordinates)
                list_velocities.append(aux_item.velocities)
                list_b_factor.append(aux_item.b_factor)
                list_occupancy.append(aux_item.occupancy)

                if aux_item.alternate_location is not None:
                    tmp_alternate_location = []
                    for alt_loc_dict in aux_item.alternate_location:
                        for key, value in alt_loc_dict.items():
                            tmp_alt_loc_dict = {}
                            tmp_alt_loc_dict[key+count_n_atoms]=value
                        tmp_alternate_location.append(tmp_alt_loc_dict)
                else:
                    tmp_alternate_location = None
                list_alternate_location.append(tmp_alternate_location)


    pass

