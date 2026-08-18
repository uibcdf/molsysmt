from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='openmm.AmberPrmtopFile')
@dep_digest('openmm')
def to_openmm_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from openmm.AmberPrmtopFile to openmm.Topology.

    Parameters
    ----------
    item : openmm.AmberPrmtopFile
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
