from molsysmt._private.argdigest import arg_digest


@arg_digest(form='molsysmt.MolSysDict')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):
    """
    Checking if form molsysmt.MolSysDict supports a specific attribute.

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

    from .attributes import attributes

    output = attributes[attribute]
    if not output:
        return False

    topology = molecular_system.data.get('topology', {}) or {}
    structures = molecular_system.data.get('structures', {}) or {}

    if attribute in ['coordinates', 'box', 'time', 'structure_id']:
        return include_none or structures.get(attribute, None) is not None

    if attribute == 'n_structures':
        return True

    if attribute in ['bond_index', 'bond_type', 'bond_order', 'bonded_atoms', 'bonded_atom_pairs', 'inner_bond_index', 'inner_bonded_atoms', 'inner_bonded_atom_pairs', 'n_bonds', 'n_inner_bonds']:
        return include_none or len(topology.get('bonds', []) or []) > 0

    if attribute.startswith('entity_') or attribute == 'n_entities':
        return include_none or len(topology.get('entities', []) or []) > 0

    if attribute.startswith('molecule_') or attribute == 'n_molecules':
        return include_none or len(topology.get('molecules', []) or []) > 0

    if attribute.startswith('chain_') or attribute == 'n_chains':
        return include_none or len(topology.get('chains', []) or []) > 0

    if attribute.startswith('group_') or attribute == 'n_groups':
        return include_none or len(topology.get('groups', []) or []) > 0

    if attribute.startswith('atom_') or attribute == 'n_atoms':
        return include_none or len(topology.get('atoms', []) or []) > 0

    if attribute.startswith('component_') or attribute == 'n_components':
        return include_none or len(topology.get('groups', []) or []) > 0

    return output
