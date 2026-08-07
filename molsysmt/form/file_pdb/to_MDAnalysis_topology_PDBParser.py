from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:pdb')
@dep_digest('MDAnalysis')
def to_MDAnalysis_topology_PDBParser(item, atom_indices='all', skip_digestion=False):

    from MDAnalysis.topology import PDBParser

    tmp_item = PDBParser.PDBParser(item)

    return tmp_item

