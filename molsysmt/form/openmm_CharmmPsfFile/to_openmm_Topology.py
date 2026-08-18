from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.CharmmPsfFile')
def to_openmm_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from openmm.CharmmPsfFile to openmm.Topology.

    Parameters
    ----------
    item : openmm.CharmmPsfFile
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.Topology
        Converted molecular system representation.
    """

    tmp_item = item.topology

    return tmp_item


