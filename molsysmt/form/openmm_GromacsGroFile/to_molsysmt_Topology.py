from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openmm.GromacsGroFile')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from molsysmt.form.openmm_Topology.to_molsysmt_Topology import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology

    tmp_item = item.topology
    tmp_item = openmm_Topology_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item
