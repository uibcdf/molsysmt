from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.TopologyDict")
def has_attribute(
    molecular_system, attribute, include_none=False, skip_digestion=False
):
    """
    Checking if form molsysmt.TopologyDict supports a specific attribute.


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

    from molsysmt.form import molsysmt_MolSys, molsysmt_Topology

    from .attributes import attributes

    if not attributes.get(attribute, False):
        return False
    # Availability for bounded stored-atom reads must not decode unrelated
    # hierarchy/chemistry, including legacy dictionaries with sparse records.
    from molsysmt.form._dict_atom_queries import supports

    records = molecular_system.data.get("atoms")
    if isinstance(records, list) and supports(attribute, "atom"):
        if attribute == "n_atoms":
            return True
        if attribute == "atom_index":
            return include_none or bool(records)
        return include_none or any(
            isinstance(row, dict) and row.get(attribute) is not None for row in records
        )
    if molecular_system.data.get("version", "0.1") == "0.2":
        if not molsysmt_Topology.attributes.get(attribute, False):
            return False
        from .to_molsysmt_Topology import to_molsysmt_Topology

        return molsysmt_Topology.has_attribute(
            to_molsysmt_Topology(molecular_system, skip_digestion=True),
            attribute,
            include_none=include_none,
            skip_digestion=True,
        )
    from .to_molsysmt_MolSys import to_molsysmt_MolSys

    return molsysmt_MolSys.has_attribute(
        to_molsysmt_MolSys(molecular_system, skip_digestion=True),
        attribute,
        include_none=include_none,
        skip_digestion=True,
    )
