from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:pdb')
@dep_digest('MDAnalysis')
def to_MDAnalysis_topology_PDBParser(item, atom_indices='all', skip_digestion=False):
    """
    Converting from file:pdb to MDAnalysis.topology.PDBParser.

    Parameters
    ----------
    item : file:pdb
        Source item in file:pdb form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    MDAnalysis.topology.PDBParser
        Resulting object in MDAnalysis.topology.PDBParser form.

    .. versionadded:: 1.0.0
    """

    from MDAnalysis.topology import PDBParser

    tmp_item = PDBParser.PDBParser(item)

    return tmp_item

