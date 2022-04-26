from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'mdtraj.Trajectory')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from molsysmt.native.structures import Structures
    from . import get_coordinates_from_atom, get_time_from_system, get_step_from_system, get_box_from_system

    tmp_item = Structures()

    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, check=False)
    time = get_time_from_atom(item, structure_indices=structure_indices, check=False)
    step = get_step_from_atom(item, structure_indices=structure_indices, check=False)
    box = get_box_from_atom(item, structure_indices=structure_indices, check=False)

    tmp_item.append_structures(step=step, time=time, box=box, coordinates=coordinates, check=False)

    return tmp_item

