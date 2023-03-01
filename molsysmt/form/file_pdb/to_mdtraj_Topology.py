from molsysmt._private.digestion import digest

@digest(form='file:pdb')
def to_mdtraj_Topology(item, atom_indices='all'):

    from mdtraj import load_topology
    from ..mdtraj_Topology import extract as extract_mdtraj_Topology

    tmp_item = load_topology(item)
    tmp_item = extract_mdtraj_Topology(tmp_item, atom_indices=atom_indices)

    return tmp_item

def _to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_mdtraj_Topology(item, atom_indices=atom_indices)

