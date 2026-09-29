from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form="molsysmt.InteractionsDict")
def get_n_structures_from_system(item, structure_indices="all", skip_digestion=False):
    """Getting the source structure-domain size from typed columns."""

    return (
        item.data["n_structures"]
        if is_all(structure_indices)
        else len(structure_indices)
    )
