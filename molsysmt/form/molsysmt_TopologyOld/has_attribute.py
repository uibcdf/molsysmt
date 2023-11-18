from molsysmt._private.digestion import digest

@digest(form='molsysmt.TopologyOld')
def has_attribute(molecular_system, attribute):

    from . import attributes

    output = attributes[attribute]

    ###
    ### TOPOLOGICAL
    ###

    if attribute in ['atom_index', 'atom_id', 'atom_name', 'atom_type',
            'group_index', 'group_id', 'group_name', 'group_type',
            'component_index', 'component_id', 'component_name', 'component_type',
            'molecule_index', 'molecule_id', 'molecule_name', 'molecule_type',
            'chain_index', 'chain_id', 'chain_name', 'chain_type',
            'entity_index', 'entity_id', 'entity_name', 'entity_type']:
        if molecular_system.atoms_dataframe.shape[0]:
            output = True 

    elif attribute in ['bond_index', 'bond_id', 'bond_type',
            'bond_order', 'bond_atoms']:
        if molecular_system.bonds_dataframe.shape[0]:
            output = True 

    return output
