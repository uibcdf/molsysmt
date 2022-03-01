def from_file_gro(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.native import Trajectory
    tmp_item = Trajectory(filepath=item, atom_indices=atom_indices, structure_indices=structure_indices)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

