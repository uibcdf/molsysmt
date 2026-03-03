from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:pdb')
def to_MDAnalysis_Topology(item, atom_indices='all', skip_digestion=False):

    from .to_MDAnalysis_topology_PDBParser import to_MDAnalysis_topology_PDBParser
    from ..MDAnalysis_topology_PDBParser.to_MDAnalysis_Topology import to_MDAnalysis_Topology as MDAnalysis_topology_PDBParser_to_MDAnalysis_Topology

    tmp_item = to_MDAnalysis_topology_PDBParser(item, skip_digestion=True)
    tmp_item = MDAnalysis_topology_PDBParser_to_MDAnalysis_Topology(tmp_item,
            atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

