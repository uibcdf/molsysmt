from molsysmt._private.arg_digestion import arg_digest


_ATOM_STATE_COLUMNS = {
    'formal_charge': 'formal_charge',
    'atom_is_aromatic': 'is_aromatic',
    'n_unpaired_electrons': 'n_unpaired_electrons',
    'n_implicit_hydrogens': 'n_implicit_hydrogens',
    'allows_implicit_hydrogens': 'allows_implicit_hydrogens',
    'atom_stereochemistry': 'stereochemistry',
}

_BOND_COLUMNS = {
    'bond_id': ('bond_id',),
    'bond_type': ('bond_type',),
    'bond_order': ('bond_order',),
    'fractional_bond_order': ('fractional_bond_order',),
    'bond_is_aromatic': ('is_aromatic',),
    'bond_is_conjugated': ('is_conjugated',),
    'bond_stereochemistry': ('stereochemistry',),
    'bond_stereo_atom_indices': ('stereo_atom1_index', 'stereo_atom2_index'),
    'bond_donor_atom_index': ('donor_atom_index',),
    'bond_acceptor_atom_index': ('acceptor_atom_index',),
    'bond_joins_components': ('joins_components',),
    'bond_evidence': ('evidence',),
}

_COUNT_ATTRIBUTES = {
    'n_atoms',
    'n_groups',
    'n_components',
    'n_molecules',
    'n_chains',
    'n_entities',
    'n_bonds',
    'n_inner_bonds',
    'n_amino_acids',
    'n_nucleotides',
    'n_ions',
    'n_waters',
    'n_small_molecules',
    'n_peptides',
    'n_proteins',
    'n_dnas',
    'n_rnas',
    'n_lipids',
    'n_polysaccharides',
    'n_saccharides',
    'n_chemical_states',
}


@arg_digest(form='molsysmt.Topology')
def has_attribute(
    molecular_system,
    attribute,
    include_none=False,
    skip_digestion=False,
):
    """Checking instance-aware attribute availability for native topology."""

    from . import attributes

    if not attributes[attribute]:
        return False
    if include_none:
        return True
    if attribute in _COUNT_ATTRIBUTES:
        return True

    if attribute in _ATOM_STATE_COLUMNS:
        return molecular_system._has_chemical_state_atom_attribute(
            _ATOM_STATE_COLUMNS[attribute]
        )

    if attribute == 'atom_index':
        return molecular_system.n_atoms > 0
    if attribute in {'atom_id', 'atom_name', 'atom_type'}:
        return molecular_system.n_atoms > 0
    if attribute == 'isotope':
        return molecular_system.atoms['isotope'].notna().any()

    hierarchy = {
        'group_index': molecular_system.atoms['group_index'].notna().any(),
        'group_id': molecular_system.n_groups > 0,
        'group_name': molecular_system.n_groups > 0,
        'group_type': molecular_system.n_groups > 0,
        'chain_index': molecular_system.atoms['chain_index'].notna().any(),
        'chain_id': molecular_system.n_chains > 0,
        'chain_name': molecular_system.n_chains > 0,
        'chain_type': molecular_system.n_chains > 0,
        'molecule_index': molecular_system.groups['molecule_index'].notna().any(),
        'molecule_id': molecular_system.n_molecules > 0,
        'molecule_name': molecular_system.n_molecules > 0,
        'molecule_type': molecular_system.n_molecules > 0,
        'entity_index': molecular_system.molecules['entity_index'].notna().any(),
        'entity_id': molecular_system.n_entities > 0,
        'entity_name': molecular_system.n_entities > 0,
        'entity_type': molecular_system.n_entities > 0,
    }
    if attribute in hierarchy:
        return bool(hierarchy[attribute])

    if attribute == 'chemical_state_index':
        return len(molecular_system._chemical_states) > 0
    if attribute == 'chemical_state_id':
        return any(
            chemical_state.state_id is not None
            for chemical_state in molecular_system._chemical_states
        )
    if attribute == 'reference_chemical_state_index':
        return (
            len(molecular_system._chemical_states) == 1
            or molecular_system._reference_chemical_state_index is not None
        )
    if attribute in {
        'connectivity_completeness',
        'component_completeness',
        'component_evidence',
    }:
        return len(molecular_system._chemical_states) > 0

    state = molecular_system._resolve_chemical_state()
    state._ensure_compatibility(molecular_system.n_atoms)
    if attribute == 'component_index':
        return state.component_indices.notna().any()
    if attribute in {'component_id', 'component_name', 'component_type'}:
        return state.components.shape[0] > 0

    bonds = state.bonds
    if attribute in {
        'bond_index',
        'bonded_atoms',
        'bonded_atom_pairs',
        'inner_bond_index',
        'inner_bonded_atoms',
        'inner_bonded_atom_pairs',
    }:
        return bonds.shape[0] > 0
    if attribute in _BOND_COLUMNS:
        return any(
            column in bonds and bonds[column].notna().any()
            for column in _BOND_COLUMNS[attribute]
        )

    return False
