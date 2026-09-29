from molsysmt._private.argdigest import arg_digest
from molsysmt.form._domain_conversion import require_full_domain


@arg_digest(form="molsysmt.Topology")
def to_molsysmt_ChemicalStates(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """Converting topology chemistry to an independent state collection.

    Parameters
    ----------
    item : molsysmt.Topology
        Source topology.
    atom_indices : 'all'
        Complete atom domain; selections are not supported by this converter.
    structure_indices : 'all'
        Complete structure domain; selections are not supported by this converter.
    skip_digestion : bool, default=False
        Whether to skip validated argument digestion.

    Returns
    -------
    molsysmt.ChemicalStates
        Independent copy of the chemical-state collection.

    Raises
    ------
    ValueError
        If atom or structure indices select a subset.

    .. versionadded:: 1.0.0
    """

    require_full_domain(atom_indices, structure_indices)
    return item._chemical_states_domain.copy()
