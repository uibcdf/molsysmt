from molsysmt._private.digestion import digest

@digest(form='file:pdb')
def to_mdtraj_Topology(item, atom_indices='all', digest=True):

    from mdtraj import load_topology
    from ..mdtraj_Topology import extract as extract_mdtraj_Topology

    tmp_item = load_topology(item)
    tmp_item = extract_mdtraj_Topology(tmp_item, atom_indices=atom_indices, digest=False)

    return tmp_item

