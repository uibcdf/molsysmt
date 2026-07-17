from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='MDAnalysis.Universe')
@dep_digest('MDAnalysis')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    if is_all(atom_indices) and is_all(structure_indices) and not copy_if_all:
        return item

    from ._subset import subset_universe

    return subset_universe(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
    )
