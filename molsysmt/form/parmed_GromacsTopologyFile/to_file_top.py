from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='parmed.GromacsTopologyFile')
@dep_digest('parmed')
def to_file_top(item, atom_indices='all', output_filename=None, skip_digestion=False):

    item.write(output_filename)

    return output_filename
