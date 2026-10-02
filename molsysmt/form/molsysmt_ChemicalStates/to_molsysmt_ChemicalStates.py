from molsysmt._private.argdigest import arg_digest
from molsysmt.form._domain_conversion import require_full_domain


@arg_digest(form="molsysmt.ChemicalStates")
def to_molsysmt_ChemicalStates(
    item,
    atom_indices="all",
    structure_indices="all",
    copy_if_all=True,
    skip_digestion=False,
):
    """Converting chemical states to an independent native collection."""

    require_full_domain(atom_indices, structure_indices)

    return item.copy() if copy_if_all else item
