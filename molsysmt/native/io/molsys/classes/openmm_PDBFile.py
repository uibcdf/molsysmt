def from_openmm_PDBFile (item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.io.topology.classes import from_openmm_PDBFile as molsysmt_topology_from_openmm_PDBFile
    from molsysmt.native.io.trajectory.classes import from_openmm_PDBFile as molsysmt_trajectory_from_openmm_PDBFile

    tmp_item = MolSys()
    tmp_item.topology = molsysmt_topology_from_openmm_PDBFile(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory = molsysmt_trajectory_from_openmm_PDBFile(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.card = None
    tmp_item.topography = None

    return tmp_item

