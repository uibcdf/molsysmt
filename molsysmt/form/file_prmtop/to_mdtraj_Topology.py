from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:prmtop')
@dep_digest('mdtraj')
def to_mdtraj_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from file:prmtop to mdtraj.Topology.

    Parameters
    ----------
    item : file:prmtop
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.Topology
        Converted molecular system representation.
    """

    from mdtraj import load_prmtop

    tmp_item = load_prmtop(item)

    return tmp_item

