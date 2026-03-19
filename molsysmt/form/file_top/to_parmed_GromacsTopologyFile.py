from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='file:top')
@dep_digest('parmed')
def to_parmed_GromacsTopologyFile(item, atom_indices='all', skip_digestion=False):

    import parmed

    tmp_item = parmed.load_file(item)

    return tmp_item
