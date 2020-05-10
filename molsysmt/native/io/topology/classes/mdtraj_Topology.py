def from_mdtraj_Topology(item, atom_indices='all', frame_indices='all'):

    from .openmm_Topology import from_openmm_Topology

    tmp_item = item.to_openmm()
    tmp_item = from_openmm_Topology(tmp_item)

    return tmp_item

