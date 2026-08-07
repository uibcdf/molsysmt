from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Simulation')
def to_openmm_Context(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    tmp_item = item.context

    return tmp_item

