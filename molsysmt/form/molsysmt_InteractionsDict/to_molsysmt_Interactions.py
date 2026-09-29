from molsysmt._private.argdigest import arg_digest
from molsysmt.form._domain_conversion import require_full_domain


@arg_digest(form="molsysmt.InteractionsDict")
def to_molsysmt_Interactions(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """Reconstructing a sparse interaction result from typed columns."""

    require_full_domain(atom_indices, structure_indices)

    from molsysmt.native.interactions_dict import _decode_interactions

    return _decode_interactions(item)
