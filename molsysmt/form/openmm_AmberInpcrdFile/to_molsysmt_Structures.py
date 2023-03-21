from molsysmt._private.digestion import digest

@digest(form='openmm.AmberInpcrdFile')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all'):

    from molsysmt.native import Structures
    from . import get_coordinates_from_atom, get_velocities_from_atom, get_box_from_system

    tmp_item = Structures()

    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices)
    velocities = get_velocities_from_atom(item, indices=atom_indices, structure_indices=structure_indices)
    box = get_box_from_system(item, structure_indices=structure_indices)
    
    tmp_item.append_structures(coordinates=coordinates, velocities=velocities, box=box)

    return tmp_item

