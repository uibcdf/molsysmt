from molsysmt._private.argdigest import arg_digest


@arg_digest(form='molsysmt.TopologyDict')
def to_molsysmt_TopologyDict(item, skip_digestion=False):
    """
    Converting from molsysmt.TopologyDict to molsysmt.TopologyDict.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.TopologyDict
        Resulting object in molsysmt.TopologyDict form.


    .. versionadded:: 1.0.0
    """
    return item.copy()
