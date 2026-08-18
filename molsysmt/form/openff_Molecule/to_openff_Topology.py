from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openff.Molecule')
def to_openff_Topology(item, skip_digestion=False):
    """
    Converting from openff.Molecule to openff.Topology.

    Parameters
    ----------
    item : openff.Molecule
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openff.Topology
        Converted molecular system representation.
    """

    return item.to_topology()
