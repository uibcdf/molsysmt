from molsysmt.dependencies import requires
from molsysmt._private.digestion import digest

@digest(form='file:pdb')
@requires('MDAnalysis')
def to_MDAnalysis_topology_PDBParser(item, atom_indices='all', skip_digestion=False):

    from MDAnalysis.topology import PDBParser

    tmp_item = PDBParser.PDBParser(item)

    return tmp_item

