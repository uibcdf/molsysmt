from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='MDAnalysis.AtomGroup')
def to_MDAnalysis_Universe(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt._private.variables import is_all

    indices = item.indices
    if not is_all(atom_indices):
        indices = indices[atom_indices]

    from molsysmt.form.MDAnalysis_Universe._subset import subset_universe

    return subset_universe(
        item.universe,
        atom_indices=indices,
        structure_indices=structure_indices,
    )
