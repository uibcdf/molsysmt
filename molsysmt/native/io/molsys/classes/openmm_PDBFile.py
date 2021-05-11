def from_openmm_PDBFile (item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.io.topology.classes import from_openmm_PDBFile as molsysmt_topology_from_openmm_PDBFile
    from molsysmt.native.io.trajectory.classes import from_openmm_PDBFile as molsysmt_trajectory_from_openmm_PDBFile

    tmp_item = MolSys()
    tmp_item.topology, _ = molsysmt_topology_from_openmm_PDBFile(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory, _ = molsysmt_trajectory_from_openmm_PDBFile(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

