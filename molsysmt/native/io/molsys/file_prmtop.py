def from_file_prmtop(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt import convert
    from molsysmt.native import MolSys
    from molsysmt.native.io.topology import from_file_prmtop as file_prmtop_to_molsysmt_Topology

    tmp_item = MolSys()
    tmp_item.topology, _ = file_prmtop_to_molsysmt_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory = convert(molecular_system, to_form='molsysmt.Trajectory', selection=atom_indices, frame_indices=frame_indices)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

