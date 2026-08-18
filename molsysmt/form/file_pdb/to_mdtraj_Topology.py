from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:pdb')
def to_mdtraj_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from file:pdb to mdtraj.Topology.


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

    from mdtraj import load_topology
    from ..mdtraj_Topology.extract import extract as extract_mdtraj_Topology

    tmp_item = load_topology(item)
    tmp_item = extract_mdtraj_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

