from molsysmt._private.argdigest import arg_digest


@arg_digest(form='file:topology_yaml')
def to_molsysmt_Topology(item, skip_digestion=False):
    """Converting a YAML topology file to Topology."""

    from .to_molsysmt_TopologyDict import to_molsysmt_TopologyDict
    from molsysmt.form.molsysmt_TopologyDict.to_molsysmt_Topology import to_molsysmt_Topology as dict_to_topology

    tmp_item = to_molsysmt_TopologyDict(item, skip_digestion=True)
    return dict_to_topology(tmp_item, skip_digestion=True)
