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
        Source item in MDAnalysis.topology.PDBParser form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    MDAnalysis.topology.PDBParser
        Resulting object in MDAnalysis.topology.PDBParser form.

    .. versionadded:: 1.0.0
    """

    from MDAnalysis.topology.PDBParser import PDBParser

    tmp_item = PDBParser(item.filename)

    return tmp_item
