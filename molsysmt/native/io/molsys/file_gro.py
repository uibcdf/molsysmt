def from_file_gro(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native import MolSys
    from molsysmt.native.io.topology import from_file_gro as file_gro_to_molsysmt_Topology
    from molsysmt.basic import convert

    tmp_item = MolSys()
    tmp_item.topology, _ = file_gro_to_molsysmt_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory = convert(molecular_system, to_form='molsysmt.Trajectory', selection=atom_indices, frame_indices=frame_indices)
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

