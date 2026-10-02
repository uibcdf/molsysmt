from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.MolSys")
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

    from molsysmt.attribute.attributes import attributes as catalogue
    from molsysmt.form import (
        molsysmt_MolecularMechanics,
        molsysmt_Structures,
        molsysmt_Topology,
    )

    from . import attributes

    if not attributes[attribute]:
        return False
    if attribute == "n_atoms":
        return molecular_system._get_n_atoms() is not None
    if attribute == "n_structures":
        return molecular_system._get_n_structures() is not None
    if attribute == "n_chemical_states":
        return molecular_system.chemical_states is not None
    if attribute == "chemical_state_index":
        if molecular_system.chemical_states is None:
            return False
        return include_none or molecular_system.chemical_states.n_chemical_states > 0
    if attribute == "chemical_state_id":
        if molecular_system.chemical_states is None:
            return False
        return include_none or any(
            state.state_id is not None
            for state in molecular_system.chemical_states._states
        )
    if attribute == "reference_chemical_state_index":
        if molecular_system.chemical_states is None:
            return False
        return include_none or (
            molecular_system.chemical_states.reference_chemical_state_index is not None
        )
    if attribute == "structure_chemical_state_index":
        if (
            molecular_system.structures is None
            or molecular_system.chemical_states is None
        ):
            return False
        if include_none:
            return True
        values = molecular_system._get_structure_chemical_state_indices(resolved=True)
        return len(values) > 0 and not values.isna().any()
    if molecular_system.chemical_states is None and (
        catalogue[attribute]["chemical_state"]
        or attribute in {"n_components", "n_bonds", "n_inner_bonds"}
    ):
        return False
    if molsysmt_Topology.attributes[attribute]:
        if molecular_system.topology is None:
            return False
        return molsysmt_Topology.has_attribute(
            molecular_system.topology,
            attribute,
            include_none=include_none,
            skip_digestion=True,
        )
    if molsysmt_Structures.attributes[attribute]:
        if molecular_system.structures is None:
            return False
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
