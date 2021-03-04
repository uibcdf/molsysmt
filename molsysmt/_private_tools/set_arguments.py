from molsysmt._private_tools.exceptions import BadCallError

where_set_argument = {

    'atom_name' : ['topology'],
    'atom_id' : ['topology'],
    'atom_type' : ['topology'],
    'group_name' : ['topology'],
    'group_id' : ['topology'],
    'group_type' : ['topology'],
    'component_name' : ['topology'],
    'component_id' : ['topology'],
    'component_type' : ['topology'],
    'chain_name' : ['topology'],
    'chain_id' : ['topology'],
    'chain_type' : ['topology'],
    'molecule_name' : ['topology'],
    'molecule_id' : ['topology'],
    'molecule_type' : ['topology'],
    'entity_name' : ['topology'],
    'entity_id' : ['topology'],
    'entity_type' : ['topology'],

    'bond_name' : ['bonds'],
    'bond_id' : ['bonds'],
    'bond_type' : ['bonds'],
    'bond_order' : ['bonds'],
    'bonded_atoms' : ['bonds'],
    'inner_bonded_atoms' : ['bonds'],
    'inner_bond_index' : ['bonds'],

    'step' : ['coordinates'],
    'time' : ['coordinates'],
    'frame' : ['coordinates'],
    'coordinates' : ['coordinates'],

    'box' : ['box'],

}


set_argument_synonym = {
    'atom_names': 'atom_name',
    'atom_ids': 'atom_id',
    'atom_types': 'atom_type',
    'group_names': 'group_name',
    'group_ids': 'group_id',
    'group_types': 'group_type',
    'component_names': 'component_name',
    'component_ids': 'component_id',
    'component_types': 'component_type',
    'chain_names': 'chain_name',
    'chain_ids': 'chain_id',
    'chain_types': 'chain_type',
    'molecule_names': 'molecule_name',
    'molecule_ids': 'molecule_id',
    'molecule_types': 'molecule_type',
    'entity_names': 'entity_name',
    'entity_ids': 'entity_id',
    'entity_types': 'entity_type',
    'bond_ids': 'bond_id',
    'bond_types': 'bond_type',
    'bonded_atom': 'bonded_atoms',
    'bonds_order': 'bond_order',
    'inner_bonded_atom': 'inner_bonded_atoms',
    'inner_bond_indices': 'inner_bond_index',
    'residue_index': 'group_index',
    'residue_names': 'group_name',
    'residue_name': 'group_name',
    'residue_ids': 'group_id',
    'residue_id': 'group_id',
    'residue_types': 'group_type',
    'residue_type': 'group_type',
    'steps': 'step',
    'times': 'time',
    'frames': 'frame',
}


set_arguments = list(where_set_argument.keys())

def digest_set_argument(set_argument, target):

    tmp_set_argument = set_argument.lower()
    if tmp_set_argument in ['name', 'names', 'id', 'ids', 'type', 'types', 'order']:
        tmp_set_argument = ('_').join([target, set_argument])
    if tmp_set_argument in set_argument_synonym:
        tmp_set_argument = set_argument_synonymn[tmp_set_argument]
    if tmp_set_argument in set_arguments:
        return tmp_set_argument
    else:
        raise BadCallError()

