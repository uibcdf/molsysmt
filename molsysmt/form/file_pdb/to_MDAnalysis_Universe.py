from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='file:pdb')
@dep_digest('MDAnalysis')
def to_MDAnalysis_Universe(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from MDAnalysis import Universe

    from ..MDAnalysis_Universe.extract import extract

    tmp_item = Universe(item)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False, skip_digestion=True)

    return tmp_item

