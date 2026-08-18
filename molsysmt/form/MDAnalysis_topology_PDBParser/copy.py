from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='MDAnalysis.topology.PDBParser')
@dep_digest('MDAnalysis')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form MDAnalysis.topology.PDBParser.

    Parameters
    ----------
    item : MDAnalysis.topology.PDBParser
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    MDAnalysis.topology.PDBParser
        Copied item.
    """

    from MDAnalysis.topology.PDBParser import PDBParser

    tmp_item = PDBParser(item.filename)

    return tmp_item
