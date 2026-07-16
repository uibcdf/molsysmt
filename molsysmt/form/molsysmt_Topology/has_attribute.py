from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='molsysmt.Topology')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):

    from . import attributes

    output = attributes[attribute]

    if not include_none:

        atom_state_attributes = {
            'formal_charge': 'formal_charge',
            'atom_is_aromatic': 'is_aromatic',
            'n_unpaired_electrons': 'n_unpaired_electrons',
            'n_implicit_hydrogens': 'n_implicit_hydrogens',
            'allows_implicit_hydrogens': 'allows_implicit_hydrogens',
            'atom_stereochemistry': 'stereochemistry',
        }
        if attribute in atom_state_attributes:
            output = molecular_system._has_chemical_state_atom_attribute(
                atom_state_attributes[attribute]
            )

        ###
        ### TOPOLOGICAL
        ###

        elif attribute == 'isotope':
            output = molecular_system.atoms['isotope'].notna().any()

        elif attribute in ['atom_index', 'atom_id', 'atom_name', 'atom_type',
                'group_index', 'group_id', 'group_name', 'group_type',
                'component_index', 'component_id', 'component_name', 'component_type',
                'molecule_index', 'molecule_id', 'molecule_name', 'molecule_type',
                'chain_index', 'chain_id', 'chain_name', 'chain_type',
                'entity_index', 'entity_id', 'entity_name', 'entity_type']:
            if molecular_system.atoms.shape[0]:
                output = True 

        elif attribute in ['bond_index', 'bonded_atoms', 'bonded_atom_pairs',
                'inner_bond_index', 'inner_bonded_atoms',
                'inner_bonded_atom_pairs', 'n_bonds', 'n_inner_bonds']:
            if molecular_system._get_chemical_state_bonds().shape[0]:
                output = True 

        elif attribute in {
            'bond_id': 'bond_id',
            'bond_type': 'bond_type',
            'bond_order': 'bond_order',
            'fractional_bond_order': 'fractional_bond_order',
            'bond_is_aromatic': 'is_aromatic',
            'bond_is_conjugated': 'is_conjugated',
            'bond_stereochemistry': 'stereochemistry',
            'bond_stereo_atom_indices': 'stereo_atom1_index',
            'bond_donor_atom_index': 'donor_atom_index',
            'bond_acceptor_atom_index': 'acceptor_atom_index',
            'bond_joins_components': 'joins_components',
            'bond_evidence': 'evidence',
        }:
            column = {
                'bond_id': 'bond_id',
                'bond_type': 'bond_type',
                'bond_order': 'bond_order',
                'fractional_bond_order': 'fractional_bond_order',
                'bond_is_aromatic': 'is_aromatic',
                'bond_is_conjugated': 'is_conjugated',
                'bond_stereochemistry': 'stereochemistry',
                'bond_stereo_atom_indices': 'stereo_atom1_index',
                'bond_donor_atom_index': 'donor_atom_index',
                'bond_acceptor_atom_index': 'acceptor_atom_index',
                'bond_joins_components': 'joins_components',
                'bond_evidence': 'evidence',
            }[attribute]
            bonds = molecular_system._get_chemical_state_bonds()
            output = column in bonds and bonds[column].notna().any()

    return output
