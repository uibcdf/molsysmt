from molsysmt._private.argdigest import arg_digest
from molsysmt.form._domain_conversion import require_full_domain


@arg_digest(form="molsysmt.InteractionsDict")
def to_molsysmt_InteractionsDict(
    item, atom_indices="all", structure_indices="all", copy_if_all=True,
    skip_digestion=False,
):
    """Converting a columnar interaction payload to an independent copy."""

    require_full_domain(atom_indices, structure_indices)

    return item.copy() if copy_if_all else item
