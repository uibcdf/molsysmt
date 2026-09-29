from molsysmt._private.argdigest import arg_digest
from molsysmt.form._domain_conversion import require_full_domain


@arg_digest(form="molsysmt.ChemicalStatesDict")
def to_molsysmt_ChemicalStates(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """Reconstructing chemical states from typed columnar tables."""

    require_full_domain(atom_indices, structure_indices)

    from molsysmt.native.chemical_states_dict import _decode_chemical_states

    return _decode_chemical_states(item)
