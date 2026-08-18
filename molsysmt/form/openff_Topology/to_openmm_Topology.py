from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openff.Topology')
def to_openmm_Topology(item, skip_digestion=False):
    """
    Converting from openff.Topology to openmm.Topology.

    Parameters
    ----------
    item : openff.Topology
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.Topology
        Converted molecular system representation.
    """

    return item.to_openmm()
