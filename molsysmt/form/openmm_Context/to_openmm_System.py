from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Context')
def to_openmm_System(item, atom_indices='all', skip_digestion=False):

    tmp_item = item.getSystem()

    return tmp_item

