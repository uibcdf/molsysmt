from molsysmt._private.digestion import digest

@digest(form='file:pdb')
def to_MDAnalysis_Topology(item, atom_indices='all'):

    from . import to_MDAnalysis_topology_PDBParser
    from ..MDAnalysis_topology_PDBParser import to_MDAnalysis_Topology as MDAnalysis_topology_PDBParser_to_MDAnalysis_Topology

    tmp_item = to_MDAnalysis_topology_PDBParser(item)
    tmp_item = MDAnalysis_topology_PDBParser_to_MDAnalysis_Topology(tmp_item,
            atom_indices=atom_indices)

    return tmp_item

