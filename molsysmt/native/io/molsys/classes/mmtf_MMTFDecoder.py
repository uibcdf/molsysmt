
def from_mmtf_MMTFDecoder(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.io.topology.classes import from_mmtf_MMTFDecoder as molsysmt_Topology_from_mmtf_MMTFDecoder
    from molsysmt.native.io.trajectory.classes import from_mmtf_MMTFDecoder as molsysmt_Trajectory_from_mmtf_MMTFDecoder

    tmp_item = MolSys()
    tmp_item.topology, _ = molsysmt_Topology_from_mmtf_MMTFDecoder(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory, _ = molsysmt_Trajectory_from_mmtf_MMTFDecoder(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

