
def from_openmm_PDBFile(item, atom_indices='all', frame_indices='all'):

    from .from_openmm_Topology import from_openmm_Topology

    tmp_item = item.getTopology()

    return from_openmm_Topology(item.topology, atom_indices=atom_indices, frame_indices=frame_indices)

