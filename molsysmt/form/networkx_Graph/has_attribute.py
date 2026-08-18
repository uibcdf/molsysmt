from molsysmt._private.argdigest import arg_digest

@arg_digest(form='networkx.Graph')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):
    """
    Checking if form networkx.Graph supports a specific attribute.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    attribute : object
        Argument attribute.
    include_none : object, default=False
        Argument include_none.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.


    .. versionadded:: 1.0.0
    """

    from . import attributes

    output = attributes[attribute]

    if not output or include_none:
        return output

    if attribute in {
        'atom_index', 'bond_index', 'bonded_atoms', 'n_atoms', 'n_bonds',
    }:
        return True
    if attribute in {
        'connectivity_completeness', 'component_completeness', 'component_evidence',
    }:
        return molecular_system.graph.get(attribute) is not None
    if attribute.startswith('bond_') or attribute == 'fractional_bond_order':
        return any(
            data.get(attribute) is not None
            for _, _, data in molecular_system.edges(data=True)
        )
    return any(
        data.get(attribute) is not None
        for _, data in molecular_system.nodes(data=True)
    )
