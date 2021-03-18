def from_openexplorer_OpenExplorerReporter (item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.io.topology.classes import from_openexplorer_OpenExplorerReporter as openexplorer_OpenExplorerReporter_to_molsysmt_Topology
    from molsysmt.native.io.trajectory.classes import from_openexplorer_OpenExplorerReporter as openexplorer_OpenExplorerReporter_to_molsysmt_Trajectory

    tmp_item = MolSys()
    tmp_item.topology = openexplorer_OpenExplorerReporter_to_molsysmt_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory = openexplorer_OpenExplorerReporter_to_molsysmt_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item


