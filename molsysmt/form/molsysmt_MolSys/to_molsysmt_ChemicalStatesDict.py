from molsysmt._private.argdigest import arg_digest
from molsysmt.form._domain_conversion import require_full_domain


@arg_digest(form="molsysmt.MolSys")
def to_molsysmt_ChemicalStatesDict(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """Converting a molecular system to typed chemical-state columns.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source molecular system.
    atom_indices : 'all'
        Complete atom domain; selections are not supported by this converter.
    structure_indices : 'all'
        Complete structure domain; selections are not supported by this converter.
    skip_digestion : bool, default=False
        Whether to skip validated argument digestion.

    Returns
    -------
    molsysmt.ChemicalStatesDict
        Independent typed columns for the chemical-state collection.

    Raises
    ------
    ValueError
        If chemical states are absent or atom or structure indices select a subset.

    .. versionadded:: 1.0.0
    """

    from molsysmt.native.chemical_states_dict import _encode_chemical_states

    if item.chemical_states is None:
        raise ValueError("This MolSys has no chemical-states domain to convert.")
    require_full_domain(atom_indices, structure_indices)
    return _encode_chemical_states(item.chemical_states)
