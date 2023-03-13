from molsysmt._private.digestion import digest

@digest(form='molsysmt.Topology')
def has_attribute(molecular_system, attribute):

    output = False

    # Check attributes list first

    from . import attributes

    if not attributes[attribute]:
        return output

    ###
    ### TOPOLOGICAL
    ###

    if attribute in ['atom_index', 'atom_id', 'atom_name', 'atom_type',
            'group_index', 'group_id', 'group_name', 'group_type',
            'component_index', 'component_id', 'component_name', 'component_type',
            'molecule_index', 'molecule_id', 'molecule_name', 'molecule_type',
            'chain_index', 'chain_id', 'chain_name', 'chain_type',
            'entity_index', 'entity_id', 'entity_name', 'entity_type']:
        if molecular_system.topology.atoms_data_frame.shape[0]:
            output = True 

    elif attribute in ['n_atoms', 'n_groups', 'n_components', 'n_molecules', 'n_chains', 'n_entities',
        'n_ions', 'n_waters', 'n_small_molecules', 'n_peptides', 'n_proteins', 'n_dnas',
        'n_rnas', 'n_lipids', 'n_oligosaccharides']:
        output = True

    elif attribute in ['bond_index', 'bond_id', 'bond_name', 'bond_type',
            'bond_order', 'bond_atoms']:
        if molecular_system.topology.bonds_data_frame.shape[0]:
            output = True 

    elif attribute=='n_bonds':
        output = True

    return output
