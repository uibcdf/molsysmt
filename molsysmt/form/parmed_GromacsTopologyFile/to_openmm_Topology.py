from molsysmt._private.argdigest import arg_digest

@arg_digest(form='parmed.GromacsTopologyFile')
def to_openmm_Topology(item, atom_indices='all', skip_digestion=False):

    from molsysmt.form.parmed_Structure.to_openmm_Topology import to_openmm_Topology as parmed_Structure_to_openmm_Topology

    return parmed_Structure_to_openmm_Topology(item, atom_indices=atom_indices, skip_digestion=True)
