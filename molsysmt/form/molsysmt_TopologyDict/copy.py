from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.TopologyDict")
def copy(item, skip_digestion=False):
    """Copying a TopologyDict payload independently.

    Parameters
    ----------
    item : TopologyDict
        Native payload wrapper. Mutable data and metadata are detached without
        decoding, remapping or validating the payload schema.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    TopologyDict
        Independent payload preserving the wrapper's concrete supported type.

    See Also
    --------
    molsysmt.basic.copy : Copy a molecular system in its registered form.

    Examples
    --------
    >>> from molsysmt.native import TopologyDict
    >>> payload = TopologyDict(data={})
    >>> copy(payload) is payload
    False

    .. versionadded:: 1.0.0
    """
    return item.copy(skip_digestion=True)
