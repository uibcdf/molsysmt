from copy import deepcopy

def _raise_not_implemented_error(item, indices=None, frame_indices=None):
    raise NotImplementedError

_common_fields = {

        'name' : _raise_not_implemented_error,
        'index' : _raise_not_implemented_error,
        'id' : _raise_not_implemented_error,
        'type' : _raise_not_implemented_error,
        'element' : _raise_not_implemented_error,

        'n_atoms' : _raise_not_implemented_error,
        'atom_name' : _raise_not_implemented_error,
        'atom_index' : _raise_not_implemented_error,
        'atom_id' : _raise_not_implemented_error,
        'atom_type' : _raise_not_implemented_error,

        'n_groups' : _raise_not_implemented_error,
        'group_name' : _raise_not_implemented_error,
        'group_index' : _raise_not_implemented_error,
        'group_id' : _raise_not_implemented_error,
        'group_type' : _raise_not_implemented_error,

        'n_components' : _raise_not_implemented_error,
        'component_name' : _raise_not_implemented_error,
        'component_index' : _raise_not_implemented_error,
        'component_id' : _raise_not_implemented_error,
        'component_type' : _raise_not_implemented_error,

        'n_chains' : _raise_not_implemented_error,
        'chain_index' : _raise_not_implemented_error,
        'chain_id' : _raise_not_implemented_error,
        'chain_name' : _raise_not_implemented_error,

        'n_molecules' : _raise_not_implemented_error,
        'molecule_name' : _raise_not_implemend_error,
        'molecule_index' : _raise_not_implemented_error,
        'molecule_id' : _raise_not_implemented_error,
        'molecule_type' : _raise_not_implemented_error,

        'n_entities' : _raise_not_implemented_error,
        'entity_name' : _raise_not_implemented_error,
        'entity_index' : _raise_not_implemented_error,
        'entity_id' : _raise_not_implemented_error,
        'entity_type' : _raise_not_implemented_error,

        'n_aminoacids' : _raise_not_implemented_error,
        'n_nucleotides' : _raise_not_implemented_error,

        'n_ions' : _raise_not_implemented_error,
        'n_waters' : _raise_not_implemented_error,
        'n_cosolutes' : _raise_not_implemented_error,
        'n_small_molecules' : _raise_not_implemented_error,
        'n_peptides' : _raise_not_implemented_error,
        'n_proteins' : _raise_not_implemented_error,
        'n_dnas' : _raise_not_implemented_error,
        'n_rnas' : _raise_not_implemented_error,

        'n_frames' : _raise_not_implemented_error,
        'coordinates' : _raise_not_implemented_error,
        'frames': _raise_not_implemented_error,

        'n_bonds' : _raise_not_implemented_error,
        'bonded_atoms' : _raise_not_implemented_error,
        'bonds' : _raise_not_implemented_error,
        'graph' : _raise_not_implemented_error,

        'masses' : _raise_not_implemented_error,
        'charge' : _raise_not_implemented_error,
        'net_charge' : _raise_not_implemented_error

        }

_atom_fields = deepcopy(_common_fields)
_atom_fields['element'] = _raise_not_implemented_error

_group_fields = deepcopy(_common_fields)

_component_fields = deepcopy(_common_fields)

_chain_fields = deepcopy(_common_fields)

_molecule_fields = deepcopy(_common_fields)

_entity_fields = deepcopy(_common_fields)

_system_fields = deepcopy(_common_fields)
_system_fields['box'] = _raise_not_implemented_error
_system_fields['box_lengths'] = _raise_not_implemented_error
_system_fields['box_angles'] = _raise_not_implemented_error
_system_fields['box_shape'] = _raise_not_implemented_error
_system_fields['time'] = _raise_not_implemented_error
_system_fields['step'] = _raise_not_implemented_error
_system_fields['length_units'] = _raise_not_implemented_error


target_fields = {

        'atom' : _atom_fields,
        'group' : _group_fields,
        'component' : _component_fields,
        'chain' : _chain_fields,
        'molecule' : _molecule_fields,
        'entity': _entity_fields,
        'system': _system_fields

        }

