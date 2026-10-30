from molsysmt._private.argdigest import arg_digest

_ATOM_STATE_COLUMNS = {
    "formal_charge": "formal_charge",
    "atom_is_aromatic": "is_aromatic",
    "n_unpaired_electrons": "n_unpaired_electrons",
    "n_implicit_hydrogens": "n_implicit_hydrogens",
    "n_explicit_hydrogens": "n_explicit_hydrogens",
    "allows_implicit_hydrogens": "allows_implicit_hydrogens",
    "atom_stereochemistry": "stereochemistry",
}

_BOND_COLUMNS = {
    "bond_id": ("bond_id",),
    "bond_type": ("bond_type",),
    "bond_order": ("bond_order",),
    "fractional_bond_order": ("fractional_bond_order",),
    "bond_is_aromatic": ("is_aromatic",),
    "bond_is_conjugated": ("is_conjugated",),
    "bond_stereochemistry": ("stereochemistry",),
    "bond_stereo_atom_indices": ("stereo_atom1_index", "stereo_atom2_index"),
    "bond_donor_atom_index": ("donor_atom_index",),
    "bond_acceptor_atom_index": ("acceptor_atom_index",),
    "bond_joins_components": ("joins_components",),
    "bond_evidence": ("evidence",),
}

_COUNT_ATTRIBUTES = {
    "n_atoms",
    "n_groups",
    "n_components",
    "n_molecules",
    "n_chains",
    "n_entities",
    "n_bonds",
    "n_inner_bonds",
    "n_amino_acids",
    "n_nucleotides",
    "n_ions",
    "n_waters",
    "n_small_molecules",
    "n_peptides",
    "n_proteins",
    "n_dnas",
    "n_rnas",
    "n_lipids",
    "n_polysaccharides",
    "n_saccharides",
    "n_chemical_states",
}


@arg_digest(form="molsysmt.Topology")
def has_attribute(
    molecular_system,
    attribute,
    include_none=False,
    skip_digestion=False,
):
    """
    Checking if form molsysmt.Topology supports a specific attribute.


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

    if not attributes[attribute]:
        return False
    if include_none:
        return True
    if attribute in _COUNT_ATTRIBUTES:
        return True

    if attribute == "atom_index":
        return molecular_system.n_atoms > 0
    if attribute in {"atom_id", "atom_name", "atom_type"}:
        return molecular_system.n_atoms > 0
    if attribute == "isotope":
        return molecular_system.atoms["isotope"].notna().any()

    hierarchy = {
        "group_index": molecular_system.n_groups > 0,
        "group_id": molecular_system.n_groups > 0,
        "group_name": molecular_system.n_groups > 0,
        "group_type": molecular_system.n_groups > 0,
        "chain_index": molecular_system.n_chains > 0,
        "chain_id": molecular_system.n_chains > 0,
        "chain_name": molecular_system.n_chains > 0,
        "chain_type": molecular_system.n_chains > 0,
        "molecule_index": molecular_system.n_molecules > 0,
        "molecule_id": molecular_system.n_molecules > 0,
        "molecule_name": molecular_system.n_molecules > 0,
        "molecule_type": molecular_system.n_molecules > 0,
        "entity_index": molecular_system.n_entities > 0,
        "entity_id": molecular_system.n_entities > 0,
        "entity_name": molecular_system.n_entities > 0,
        "entity_type": molecular_system.n_entities > 0,
    }
    if attribute in hierarchy:
        return bool(hierarchy[attribute])

    return False
