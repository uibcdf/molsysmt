from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.H5MSMFileHandler')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):

    from . import attributes

    output = attributes[attribute]

    if not include_none:

        if attribute in {
            'velocities',
            'temperature',
            'potential_energy',
            'kinetic_energy',
        }:
            dataset = molecular_system.file['structures'].get(attribute)
            output = dataset is not None and dataset.shape[0] > 0
        elif attribute == 'total_energy':
            structures = molecular_system.file['structures']
            output = all(
                name in structures and structures[name].shape[0] > 0
                for name in ('potential_energy', 'kinetic_energy')
            )
        elif attribute == 'isotope':
            atoms = molecular_system.file['topology']['atoms']
            output = 'isotope' in atoms and bool((atoms['isotope'][:] != 0).any())
        elif attribute == 'b_factor':
            if 'b_factor' not in molecular_system.file['structures']:
                output = False
            elif molecular_system.file['structures']['b_factor'].shape[0] == 0:
                output = False
        elif attribute == 'structure_chemical_state_index':
            from .get_structural_attributes import (
                get_structure_chemical_state_index_from_system,
            )

            values = get_structure_chemical_state_index_from_system(
                molecular_system, skip_digestion=True
            )
            output = len(values) > 0 and all(value is not None for value in values)
        elif attribute in {
            'formal_charge', 'atom_is_aromatic', 'n_unpaired_electrons',
            'n_implicit_hydrogens', 'allows_implicit_hydrogens',
            'atom_stereochemistry',
            'bond_id', 'bond_type', 'bond_order', 'fractional_bond_order',
            'bond_is_aromatic', 'bond_is_conjugated', 'bond_stereochemistry',
            'bond_stereo_atom_indices', 'bond_donor_atom_index',
            'bond_acceptor_atom_index', 'bond_joins_components', 'bond_evidence',
        }:
            from .to_molsysmt_Topology import to_molsysmt_Topology
            from molsysmt.form.molsysmt_Topology import has_attribute as topology_has

            topology = to_molsysmt_Topology(molecular_system, skip_digestion=True)
            output = topology_has(
                topology, attribute, include_none=False, skip_digestion=True
            )

    return output
