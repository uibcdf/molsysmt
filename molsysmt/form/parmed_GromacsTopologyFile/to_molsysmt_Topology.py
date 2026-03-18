from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='parmed.GromacsTopologyFile')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from molsysmt.form.parmed_Structure.to_molsysmt_Topology import to_molsysmt_Topology as parmed_Structure_to_molsysmt_Topology

    return parmed_Structure_to_molsysmt_Topology(item, atom_indices=atom_indices, skip_digestion=True)
