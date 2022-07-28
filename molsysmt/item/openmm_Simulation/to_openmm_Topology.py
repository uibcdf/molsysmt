from molsysmt._private.digestion import digest

@digest(form='openmm.Simulation')
def to_openmm_Topology(item, atom_indices='all'):

    from molsysmt.item.openmm_Topology import extract_openmm_Topology

    tmp_item = item.topology
    tmp_item = extract_openmm_Topology(tmp_item, atom_indices=atom_indices)

    return tmp_item

