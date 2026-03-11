from molsysmt._private.arg_digestion import arg_digest


@arg_digest(form='molsysmt.TopologyDict')
def to_molsysmt_TopologyDict(item, skip_digestion=False):
    """Copying TopologyDict."""
    return item.copy()
