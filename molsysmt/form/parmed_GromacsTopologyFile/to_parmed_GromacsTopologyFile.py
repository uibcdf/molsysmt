from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='parmed.GromacsTopologyFile')
@dep_digest('parmed')
def to_parmed_GromacsTopologyFile(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    from .extract import extract

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
                   copy_if_all=copy_if_all, skip_digestion=True)
