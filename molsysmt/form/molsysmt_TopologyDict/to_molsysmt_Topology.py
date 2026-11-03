from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.TopologyDict")
def to_molsysmt_Topology(item, skip_digestion=False):
    """
    Converting from molsysmt.TopologyDict to molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Topology
        Resulting object in molsysmt.Topology form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.form._native_dict import decode_topology

    return decode_topology(item.data)
