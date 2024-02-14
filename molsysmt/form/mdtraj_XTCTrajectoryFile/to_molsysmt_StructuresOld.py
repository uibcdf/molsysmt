from molsysmt._private.digestion import digest

@digest(form='mdtraj.XTCTrajectoryFile')
def to_molsysmt_StructuresOld(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native.structures_old import StructuresOld
    from . import get_coordinates_from_atom, get_structure_id_from_system, get_time_from_system, get_box_from_system

    tmp_item = StructuresOld()

    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices,
                                            skip_digestion=False)
    structure_id = get_structure_id_from_system(item, structure_indices=structure_indices, skip_digestion=False)
    time = get_time_from_system(item, structure_indices=structure_indices, skip_digestion=False)
    box = get_box_from_system(item, structure_indices=structure_indices, skip_digestion=False)

    tmp_item.append_structures(structure_id=structure_id, time=time, box=box, coordinates=coordinates)

    return tmp_item

