
def from_mdtraj_Trajectory(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.molsys import MolSys
    #from molsysmt.native.io.card import from_mmtf_mdtraj_Trajectory as to_card
    from molsysmt.native.io.topology import from_mdtraj_Topology as to_topology
    from molsysmt.native.io.trajectory import from_mdtraj_Trajectory as to_trajectory

    tmp_item = MolSys()
    tmp_item.topology = to_topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory = to_trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.card = None
    tmp_item.topography = None
    return tmp_item




