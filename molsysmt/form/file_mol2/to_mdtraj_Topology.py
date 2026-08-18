from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:mol2')
def to_mdtraj_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from file:mol2 to mdtraj.Topology.

    Parameters
    ----------
    item : file:mol2
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.Topology
        Converted molecular system representation.
    """

    from mdtraj import load_mol2
    from ..mdtraj_Topology.extract import extract as extract_mdtraj_Topology

    tmp_item = load_mol2(item).topology
    tmp_item = extract_mdtraj_Topology(tmp_item, skip_digestion=True)

    return tmp_item

