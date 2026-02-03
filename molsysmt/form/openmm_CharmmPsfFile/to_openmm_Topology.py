from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openmm.CharmmPsfFile')
def to_openmm_Topology(item, atom_indices='all', skip_digestion=False):

    tmp_item = item.topology

    return tmp_item


