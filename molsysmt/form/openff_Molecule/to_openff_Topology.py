from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openff.Molecule')
def to_openff_Topology(item, skip_digestion=False):
    """
    Converting from openff.Molecule to openff.Topology.

    Parameters
    ----------
    item : openff.Molecule
        Source item in openff.Molecule form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openff.Topology
        Resulting object in openff.Topology form.

    .. versionadded:: 1.0.0
    """

    return item.to_topology()
