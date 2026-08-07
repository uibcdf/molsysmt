from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.GromacsTopFile')
def to_openmm_Topology(item, atom_indices='all', skip_digestion=False):

    tmp_item = item.topology

    return tmp_item

