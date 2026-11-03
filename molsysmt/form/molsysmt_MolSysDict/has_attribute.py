from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.MolSysDict")
def has_attribute(
    molecular_system, attribute, include_none=False, skip_digestion=False
):
    """
    Checking if form molsysmt.MolSysDict supports a specific attribute.


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

    if molecular_system.data.get("version", "0.1") == "0.2":
        from .attributes import attributes

        if not attributes.get(attribute, False):
            return False
        data = molecular_system.data
        from molsysmt.form import molsysmt_Topology

        if attribute == "n_atoms":
            return any(
                data.get(name) is not None
                for name in ("topology", "chemical_states", "structures")
            ) or bool(data.get("interactions"))
        if molsysmt_Topology.attributes.get(attribute, False):
            topology = data.get("topology")
            if topology is None:
                return False
            if include_none or attribute.startswith("n_"):
                return True
            prefix = attribute.split("_", 1)[0]
            table = {
                "atom": "atoms",
                "group": "groups",
                "chain": "chains",
                "molecule": "molecules",
                "entity": "entities",
            }.get(prefix)
            if table is not None:
                return bool(topology.get(table))
        from molsysmt.form._native_dict import decode_molsys
        from molsysmt.form.molsysmt_MolSys import has_attribute as native_has

        return native_has(
            decode_molsys(data),
            attribute,
            include_none=include_none,
            skip_digestion=True,
        )
    from .attributes import attributes

    output = attributes[attribute]
    if not output:
        return False

    topology = molecular_system.data.get("topology", {}) or {}
    structures = molecular_system.data.get("structures", {}) or {}

    if attribute in ["coordinates", "box", "time", "structure_id"]:
        return include_none or structures.get(attribute, None) is not None

    if attribute == "n_structures":
        return True

    if attribute in [
        "bond_index",
        "bond_type",
        "bond_order",
        "bonded_atoms",
        "bonded_atom_pairs",
        "inner_bond_index",
        "inner_bonded_atoms",
        "inner_bonded_atom_pairs",
        "n_bonds",
        "n_inner_bonds",
    ]:
        return include_none or len(topology.get("bonds", []) or []) > 0

    if attribute.startswith("entity_") or attribute == "n_entities":
        return include_none or len(topology.get("entities", []) or []) > 0

    if attribute.startswith("molecule_") or attribute == "n_molecules":
        return include_none or len(topology.get("molecules", []) or []) > 0

    if attribute.startswith("chain_") or attribute == "n_chains":
        return include_none or len(topology.get("chains", []) or []) > 0

    if attribute.startswith("group_") or attribute == "n_groups":
        return include_none or len(topology.get("groups", []) or []) > 0

    if attribute.startswith("atom_") or attribute == "n_atoms":
        return include_none or len(topology.get("atoms", []) or []) > 0

    if attribute.startswith("component_") or attribute == "n_components":
        return include_none or len(topology.get("groups", []) or []) > 0

    return output
