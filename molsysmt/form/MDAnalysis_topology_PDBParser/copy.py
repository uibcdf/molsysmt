from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='MDAnalysis.topology.PDBParser')
@dep_digest('MDAnalysis')
def copy(item, skip_digestion=False):

    from MDAnalysis.topology.PDBParser import PDBParser

    tmp_item = PDBParser(item.filename)

    return tmp_item
