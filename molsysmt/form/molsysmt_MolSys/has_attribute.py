from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='molsysmt.MolSys')
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
            output = molecular_system.topology._has_chemical_state_atom_attribute(
                atom_state_attributes[attribute]
            )

        ###
        ### TOPOLOGICAL
        ###

        elif attribute == 'isotope':
            output = molecular_system.topology.atoms['isotope'].notna().any()

        elif attribute in ['atom_index', 'atom_id', 'atom_name', 'atom_type',
                'group_index', 'group_id', 'group_name', 'group_type',
                'component_index', 'component_id', 'component_name', 'component_type',
                'molecule_index', 'molecule_id', 'molecule_name', 'molecule_type',
                'chain_index', 'chain_id', 'chain_name', 'chain_type',
                'entity_index', 'entity_id', 'entity_name', 'entity_type']:
            if molecular_system.topology.atoms.shape[0]:
                output = True 

        elif attribute in ['bond_index', 'bonded_atoms', 'bonded_atom_pairs',
                'inner_bond_index', 'inner_bonded_atoms',
                'inner_bonded_atom_pairs', 'n_bonds', 'n_inner_bonds']:
            if molecular_system.topology._get_chemical_state_bonds().shape[0]:
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
            bonds = molecular_system.topology._get_chemical_state_bonds()
            output = column in bonds and bonds[column].notna().any()

        ###
        ### STRUCTURAL ATTRIBUTES
        ###

        elif attribute == 'structure_chemical_state_index':
            values = molecular_system._get_structure_chemical_state_indices(
                resolved=True
            )
            output = len(values) > 0 and not values.isna().any()

        elif attribute=='structure_index':
            if molecular_system.structures.structure_id is None:
                output = False

        elif attribute=='structure_id':
            if molecular_system.structures.structure_id is None:
                output = False

        elif attribute=='coordinates':
            if molecular_system.structures.coordinates is None:
                output = False

        elif attribute=='velocities':
            if molecular_system.structures.velocities is None:
                output = False

        elif attribute=='time':
            if molecular_system.structures.time is None:
                output = False

        elif attribute in ['box', 'box_shape', 'box_angles', 'box_lengths', 'box_volume']:
            if molecular_system.structures.box is None:
                output = False

        elif attribute=='alternate_location':
            if molecular_system.structures.alternate_location is None:
                output = False

        elif attribute=='b_factor':
            if molecular_system.structures.b_factor is None:
                output = False


        ###
        ### MECHANICAL ATTRIBUTES
        ###

        elif attribute=='partial_charge':
            if molecular_system.molecular_mechanics.partial_charge is None:
                output = False

        elif attribute=='atom_ff_type':
            if molecular_system.molecular_mechanics.atom_ff_type is None:
                output = False

        elif attribute=='forcefield':
            if molecular_system.molecular_mechanics.forcefield is None:
                output = False

        elif attribute=='non_bonded_method':
            if molecular_system.molecular_mechanics.non_bonded_method is None:
                output = False

        elif attribute=='cutoff_distance':
            if molecular_system.molecular_mechanics.cutoff_distance is None:
                output = False

        elif attribute=='switch_distance':
            if molecular_system.molecular_mechanics.switch_distance is None:
                output = False

        elif attribute=='dispersion_correction':
            if molecular_system.molecular_mechanics.dispersion_correction is None:
                output = False

        elif attribute=='ewald_error_tolerance':
            if molecular_system.molecular_mechanics.ewald_error_tolerance is None:
                output = False

        elif attribute=='hydrogen_mass':
            if molecular_system.molecular_mechanics.hydrogen_mass is None:
                output = False

        elif attribute=='constraints':
            if molecular_system.molecular_mechanics.constraints is None:
                output = False

        elif attribute=='flexible_constraints':
            if molecular_system.molecular_mechanics.flexible_constraints is None:
                output = False

        elif attribute=='water_model':
            if molecular_system.molecular_mechanics.water_model is None:
                output = False

        elif attribute=='rigid_water':
            if molecular_system.molecular_mechanics.rigid_water is None:
                output = False

        elif attribute=='implicit_solvent':
            if molecular_system.molecular_mechanics.implicit_solvent is None:
                output = False

        elif attribute=='solute_dielectric':
            if molecular_system.molecular_mechanics.solute_dielectric is None:
                output = False

        elif attribute=='solvent_dielectric':
            if molecular_system.molecular_mechanics.solvent_dielectric is None:
                output = False

        elif attribute=='salt_concentration':
            if molecular_system.molecular_mechanics.salt_concentration is None:
                output = False

        elif attribute=='kappa':
            if molecular_system.molecular_mechanics.kappa is None:
                output = False

    return output
