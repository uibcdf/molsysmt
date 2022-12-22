from molsysmt._private.digestion import digest

@digest(form='file:pdb')
def to_mdanalysis_Topology(item, atom_indices='all', digest=True):

    from . import to_mdanalysis_topology_PDBParser
    from ..mdanalysis_topology_PDBParser import to_mdanalysis_Topology as mdanalysis_topology_PDBParser_to_mdanalysis_Topology

    tmp_item = to_mdanalysis_topology_PDBParser(item, digest=False)
    tmp_item = mdanalysis_topology_PDBParser_to_mdanalysis_Topology(tmp_item,
            atom_indices=atom_indices, digest=False)

    return tmp_item

