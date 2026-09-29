from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.InteractionsDict")
def get_n_atoms_from_system(item, skip_digestion=False):
    """Getting the source atom-domain size from typed columns."""

    return item.data["n_atoms"]
