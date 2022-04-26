from molsysmt._private.digestion import digest_item, digest_atom_indices

def to_mdanalysis_Topology(item, atom_indices='all', check=True):

    if check:

        digest_item(item, 'file:pdb')
        atom_indices = digest_atom_indices(atom_indices)

    from . import to_mdanalysis_topology_PDBParser
    from ..mdanalysis_topology_PDBParser import to_mdanalysis_Topology as mdanalysis_topology_PDBParser_to_mdanalysis_Topology

    tmp_item = to_mdanalysis_topology_PDBParser(item, check=False)
    tmp_item = mdanalysis_topology_PDBParser_to_mdanalysis_Topology(tmp_item, atom_indices=atom_indices, check=False)

    return tmp_item

