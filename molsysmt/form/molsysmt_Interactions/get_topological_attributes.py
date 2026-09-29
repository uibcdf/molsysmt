from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.Interactions")
def get_n_atoms_from_system(item, skip_digestion=False):
    """Getting the source atom-domain size from interactions."""

    return item.n_atoms
