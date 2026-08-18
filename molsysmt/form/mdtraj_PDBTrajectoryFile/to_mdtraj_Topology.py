from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='mdtraj.PDBTrajectoryFile')
@dep_digest('mdtraj')
def to_mdtraj_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from mdtraj.PDBTrajectoryFile to mdtraj.Topology.

    Parameters
    ----------
    item : mdtraj.PDBTrajectoryFile
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.Topology
        Converted molecular system representation.
    """

    return item.topology
