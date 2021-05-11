def to_XYZ (item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt import get

    tmp_item = get(item, target='atom', selection=atom_indices, frame_indices=frame_indices,
                coordinates=True)

    tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

