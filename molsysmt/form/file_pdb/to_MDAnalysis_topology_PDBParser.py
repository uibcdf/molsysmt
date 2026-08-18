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
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    MDAnalysis.topology.PDBParser
        Converted molecular system representation.
    """

    from MDAnalysis.topology import PDBParser

    tmp_item = PDBParser.PDBParser(item)

    return tmp_item

