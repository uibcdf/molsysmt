from molsysmt._private.argdigest import arg_digest

bond_dependent_attributes = [
    "component_index",
    "component_id",
    "component_type",
    "component_name",
    "n_components",
    "bond_index",
    "bond_id",
    "bond_type",
    "bond_order",
    "fractional_bond_order",
    "bond_is_aromatic",
    "bond_is_conjugated",
    "bond_stereochemistry",
    "bond_stereo_atom_indices",
    "bond_donor_atom_index",
    "bond_acceptor_atom_index",
    "bond_joins_components",
    "bond_evidence",
    "bonded_atoms",
    "bonded_atom_pairs",
    "inner_bond_index",
    "inner_bonded_atoms",
    "inner_bonded_atom_pairs",
    "n_bonds",
    "n_inner_bonds",
]

bond_dependent_elements = ["component", "bond"]


@arg_digest()
def bonds_are_required_to_get_attribute(
    attribute, from_element=None, skip_digestion=False
):
    """Checking whether an attribute query requires state-local connectivity.

    Parameters
    ----------
    attribute : str
        Canonical attribute name to query.
    from_element : str or None, default=None
        Source element of the query. A bond or component source requires its
        chemical graph even when the requested attribute is stable inventory.
        None checks only the requested attribute.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    bool
        True for graph attributes or a bond/component source axis. Stored atom,
        group, chain, molecule and entity inventory does not require bonds.

    Notes
    -----
    This describes reading declared attributes. It does not prescribe how a
    foreign-form converter may reconstruct inventory missing from its source.
    Stable molecule membership is independent of chemical components; reading
    it must not trigger graph inference solely because it names molecules.

    Examples
    --------
    >>> from molsysmt.attribute import bonds_are_required_to_get_attribute
    >>> bonds_are_required_to_get_attribute('molecule_index', 'atom')
    False
    >>> bonds_are_required_to_get_attribute('atom_index', 'component')
    True

    .. versionchanged:: 1.0.0
       Stable molecule, entity and chain inventory is independent of bonds.
    """

    output = attribute in bond_dependent_attributes

    if from_element is not None:
        output = output | (from_element in bond_dependent_elements)

    return output
