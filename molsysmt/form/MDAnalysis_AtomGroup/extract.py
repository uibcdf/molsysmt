from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='MDAnalysis.AtomGroup')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    if is_all(atom_indices) and is_all(structure_indices) and not copy_if_all:
        return item

    indices = item.indices
    if not is_all(atom_indices):
        indices = indices[atom_indices]

    from molsysmt.form.MDAnalysis_Universe._subset import subset_universe

    return subset_universe(
        item.universe,
        atom_indices=indices,
        structure_indices=structure_indices,
    ).atoms
