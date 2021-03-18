def from_gro(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native import MolSys
    from molsysmt.native.io.topology.files import from_gro as gro_to_molsysmt_Topology
    from molsysmt.multitool import convert

    tmp_item = MolSys()
    tmp_item.topology = gro_to_molsysmt_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory = convert(molecular_system, to_form='molsysmt.Trajectory', selection=atom_indices, frame_indices=frame_indices)

    return tmp_item

