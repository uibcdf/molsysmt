from molsysmt._private.argdigest import arg_digest


@arg_digest(form='file:topology_yaml')
def to_molsysmt_Topology(item, skip_digestion=False):
    """
    Converting from file:topology_yaml to molsysmt.Topology.

    Parameters
    ----------
    item : file:topology_yaml
        Source item in file:topology_yaml form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Topology
        Resulting object in molsysmt.Topology form.

    .. versionadded:: 1.0.0
    """

    from .to_molsysmt_TopologyDict import to_molsysmt_TopologyDict
    from molsysmt.form.molsysmt_TopologyDict.to_molsysmt_Topology import to_molsysmt_Topology as dict_to_topology

    tmp_item = to_molsysmt_TopologyDict(item, skip_digestion=True)
    return dict_to_topology(tmp_item, skip_digestion=True)
