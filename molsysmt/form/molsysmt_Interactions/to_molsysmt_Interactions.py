from molsysmt._private.argdigest import arg_digest
from molsysmt.form._domain_conversion import require_full_domain


@arg_digest(form="molsysmt.Interactions")
def to_molsysmt_Interactions(
    item,
    atom_indices="all",
    structure_indices="all",
    copy_if_all=True,
    skip_digestion=False,
):
    """Converting an interaction result to an independent full result."""

    require_full_domain(atom_indices, structure_indices)

    if not copy_if_all:
        return item
    from molsysmt.native.interactions_dict import (
        _decode_interactions,
        _encode_interactions,
    )

    return _decode_interactions(_encode_interactions(item))
