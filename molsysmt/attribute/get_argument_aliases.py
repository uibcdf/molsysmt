from copy import deepcopy

from .attributes import attribute_synonyms


_ELEMENT_ATTRIBUTE_ALIASES = {
    'atom': {'name': 'atom_name', 'index': 'atom_index', 'id': 'atom_id', 'type': 'atom_type'},
    'group': {'name': 'group_name', 'index': 'group_index', 'id': 'group_id', 'type': 'group_type'},
    'component': {
        'name': 'component_name',
        'index': 'component_index',
        'id': 'component_id',
        'type': 'component_type',
    },
    'molecule': {
        'name': 'molecule_name',
        'index': 'molecule_index',
        'id': 'molecule_id',
        'type': 'molecule_type',
    },
    'chain': {'name': 'chain_name', 'index': 'chain_index', 'id': 'chain_id', 'type': 'chain_type'},
    'entity': {
        'name': 'entity_name',
        'index': 'entity_index',
        'id': 'entity_id',
        'type': 'entity_type',
    },
    'bond': {'index': 'bond_index', 'id': 'bond_id', 'type': 'bond_type', 'order': 'bond_order'},
}


def get_argument_aliases():
    """Returning the public argument-alias contract.

    The returned plain dictionary describes both global attribute synonyms and the
    element-dependent short names accepted by :func:`molsysmt.basic.get`. Consumers
    must scope these semantic mappings to their own callables. Each call returns an
    independent copy, so changing it cannot alter MolSysMT's runtime configuration.

    Returns
    -------
    dict
        Versioned argument-alias contract.

    Notes
    -----
    Canonical names are never included as aliases, and aliases are resolved in one
    pass. The contract deliberately contains no ArgDigest registry objects.

    See Also
    --------
    :func:`molsysmt.basic.get`

    Examples
    --------
    >>> import molsysmt as msm
    >>> aliases = msm.attribute.get_argument_aliases()
    >>> aliases['attribute_synonyms']['atom_names']
    'atom_name'
    >>> aliases['element_attribute_aliases']['group']['name']
    'group_name'

    .. versionadded:: 0.22.0
    """

    contract = {
        'schema_version': 1,
        'attribute_synonyms': dict(attribute_synonyms),
        'element_attribute_aliases': _ELEMENT_ATTRIBUTE_ALIASES,
    }

    return deepcopy(contract)
