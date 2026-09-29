from molsysmt._private.argdigest import arg_digest
from molsysmt.form._domain_conversion import require_full_domain


@arg_digest(form="molsysmt.ChemicalStates")
def to_molsysmt_ChemicalStatesDict(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """Converting chemical states to typed columnar tables."""

    require_full_domain(atom_indices, structure_indices)

    from molsysmt.native.chemical_states_dict import _encode_chemical_states

    return _encode_chemical_states(item)
