from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:prmtop')
@dep_digest('mdtraj')
def to_mdtraj_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from file:prmtop to mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.Topology
        Resulting object in mdtraj.Topology form.


    .. versionadded:: 1.0.0
    """

    from mdtraj import load_prmtop

    tmp_item = load_prmtop(item)

    return tmp_item

