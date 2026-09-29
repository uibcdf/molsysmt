from molsysmt._private.argdigest import arg_digest
from molsysmt.form._domain_conversion import require_full_domain


@arg_digest(form="molsysmt.Interactions")
def to_molsysmt_InteractionsDict(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """Converting a full interaction result to typed sparse columns."""

    require_full_domain(atom_indices, structure_indices)

    from molsysmt.native.interactions_dict import _encode_interactions

    return _encode_interactions(item)
