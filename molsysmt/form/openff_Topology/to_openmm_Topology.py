from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openff.Topology')
def to_openmm_Topology(item, skip_digestion=False):
    """
    Converting from openff.Topology to openmm.Topology.

    Parameters
    ----------
    item : openff.Topology
        Source item in openff.Topology form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Topology
        Resulting object in openmm.Topology form.

    .. versionadded:: 1.0.0
    """

    return item.to_openmm()
