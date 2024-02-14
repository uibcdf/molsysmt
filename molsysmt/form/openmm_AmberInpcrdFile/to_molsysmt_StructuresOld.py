from molsysmt._private.digestion import digest

@digest(form='openmm.AmberInpcrdFile')
def to_molsysmt_StructuresOld(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import StructuresOld
    from . import get_coordinates_from_atom, get_velocities_from_atom, get_box_from_system

    tmp_item = StructuresOld()

    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices,
                                            skip_digestion=True)
    velocities = get_velocities_from_atom(item, indices=atom_indices, structure_indices=structure_indices,
                                          skip_digestion=True)
    box = get_box_from_system(item, structure_indices=structure_indices, skip_digestion=True)
    
    tmp_item.append_structures(coordinates=coordinates, velocities=velocities, box=box, skip_digestion=True)

    return tmp_item

