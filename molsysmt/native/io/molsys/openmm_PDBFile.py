def from_openmm_PDBFile (item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.io.topology import from_openmm_PDBFile as molsysmt_topology_from_openmm_PDBFile
    from molsysmt.native.io.trajectory import from_openmm_PDBFile as molsysmt_trajectory_from_openmm_PDBFile

    tmp_item = MolSys()
    tmp_item.topology, _ = molsysmt_topology_from_openmm_PDBFile(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory, _ = molsysmt_trajectory_from_openmm_PDBFile(item, atom_indices=atom_indices, frame_indices=frame_indices)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

