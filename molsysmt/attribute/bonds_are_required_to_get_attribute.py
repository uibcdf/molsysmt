from molsysmt._private.digestion import digest

bond_dependent_attributes = [
    'component_index', 
    'component_id', 
    'component_type', 
    'component_name', 
    'n_components', 
    'molecule_index', 
    'molecule_id', 
    'molecule_type', 
    'molecule_name', 
    'n_molecules', 
    'entity_index', 
    'entity_id', 
    'entity_type', 
    'entity_name', 
    'n_entities', 
    'bond_index', 
    'bond_type', 
    'bond_order', 
    'bonded_atoms', 
    'bonded_atom_pairs', 
    'inner_bond_index', 
    'inner_bonded_atoms', 
    'n_bonds', 
    'n_inner_bonds', 
    'n_peptides', 
    'n_proteins', 
    'n_adns', 
    'n_arns' 
]

bond_dependent_elements=[
    'component', 
    'molecule', 
    'entity',
    'bond'
]

@digest()
def bonds_are_required_to_get_attribute(attribute, from_element=None, skip_digestion=False):

    output = (attribute in bond_dependent_attributes)

    if from_element is not None:

        output = output | (from_element in bond_dependent_elements)

    return output

