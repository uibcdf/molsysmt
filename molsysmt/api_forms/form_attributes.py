def form_attributes():
    """ Returns a dictionary with the attributes of each form.
        This is a template dictionary in which each attribute
        is set to false by default.

        For each form the attributes that are present must be
        set to true.
    """
    return {
        'atom_index': False,
        'atom_id': False,
        'atom_name': False,
        'atom_type': False,

        'bond_index': False,
        'bond_id': False,
        'bond_name': False,
        'bond_type': False,
        'bond_order': False,

        'group_index': False,
        'group_id': False,
        'group_name': False,
        'group_type': False,

        'component_index': False,
        'component_id': False,
        'component_name': False,
        'component_type': False,

        'molecule_index': False,
        'molecule_id': False,
        'molecule_name': False,
        'molecule_type': False,

        'chain_index': False,
        'chain_id': False,
        'chain_name': False,
        'chain_type': False,

        'entity_index': False,
        'entity_id': False,
        'entity_name': False,
        'entity_type': False,

        'coordinates': False,
        'velocities': False,
        'box': False,
        'time': False,
        'step': False,

        'forcefield': False,
        'temperature': False,
        'pressure': False,
        'integrator': False,
        'damping': False,

    }
