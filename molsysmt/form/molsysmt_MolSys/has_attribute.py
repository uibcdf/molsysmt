from molsysmt._private.argdigest import arg_digest


@arg_digest(form='molsysmt.MolSys')
def has_attribute(
    molecular_system,
    attribute,
    include_none=False,
    skip_digestion=False,
):
    """
    Checking if form molsysmt.MolSys supports a specific attribute.

    Parameters
    ----------
    molecular_system : object
        Argument molecular_system.
    attribute : str
        Attribute name to query.
    include_none : object
        Argument include_none.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.

    .. versionadded:: 1.0.0
    """

    from molsysmt.form import (
        molsysmt_MolecularMechanics,
        molsysmt_Structures,
        molsysmt_Topology,
    )
    from . import attributes

    if not attributes[attribute]:
        return False
    if attribute == 'structure_chemical_state_index':
        if include_none:
            return True
        values = molecular_system._get_structure_chemical_state_indices(
            resolved=True
        )
        return len(values) > 0 and not values.isna().any()
    if molsysmt_Topology.attributes[attribute]:
        return molsysmt_Topology.has_attribute(
            molecular_system.topology,
            attribute,
            include_none=include_none,
            skip_digestion=True,
        )
    if molsysmt_Structures.attributes[attribute]:
        return molsysmt_Structures.has_attribute(
            molecular_system.structures,
            attribute,
            include_none=include_none,
            skip_digestion=True,
        )
    if molsysmt_MolecularMechanics.attributes[attribute]:
        return molsysmt_MolecularMechanics.has_attribute(
            molecular_system.molecular_mechanics,
            attribute,
            include_none=include_none,
            skip_digestion=True,
        )
    return False
