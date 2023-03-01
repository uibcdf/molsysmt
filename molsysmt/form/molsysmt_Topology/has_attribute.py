from molsysmt._private.digestion import digest

@digest(form='molsysmt.Topology')
def has_attribute(molecular_system, **kwargs):

    arguments = []
    for key in kwargs.keys():
        if kwargs[key]:
            arguments.append(key)

    outputs = []

    for argument in arguments:

        output = False

        ###
        ### TOPOLOGICAL
        ###

        if argument in ['atom_index', 'atom_id', 'atom_name', 'atom_type',
                'group_index', 'group_id', 'group_name', 'group_type',
                'component_index', 'component_id', 'component_name', 'component_type',
                'molecule_index', 'molecule_id', 'molecule_name', 'molecule_type',
                'chain_index', 'chain_id', 'chain_name', 'chain_type',
                'entity_index', 'entity_id', 'entity_name', 'entity_type']:
            if molecular_system.topology.atoms_data_frame.shape[0]:
                output = True 

        elif argument in ['bond_index', 'bond_id', 'bond_name', 'bond_type',
                'bond_order', 'bond_atoms']:
            if molecular_system.topology.bonds_data_frame.shape[0]:
                output = True 

        outputs.append(output)

    if len(outputs)==1:
        return outputs[0]
    else:
        return outputs

