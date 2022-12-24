from molsysmt._private.digestion import digest

@digest(form='openmm.Simulation')
def to_openmm_Topology(item, atom_indices='all', digest=True):

    from molsysmt.form.openmm_Topology import extract_openmm_Topology

    tmp_item = item.topology
    tmp_item = extract_openmm_Topology(tmp_item, atom_indices=atom_indices, digest=False)

    return tmp_item

