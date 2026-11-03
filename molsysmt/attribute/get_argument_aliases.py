from molsysmt._private.attribute_aliases import (
    get_alias_contract as _get_alias_contract,
)


def get_argument_aliases():
    """
    Returning the public argument-alias contract.

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

    return _get_alias_contract()
