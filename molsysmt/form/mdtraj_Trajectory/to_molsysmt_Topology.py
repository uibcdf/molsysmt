from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_molsysmt_Topology(item, atom_indices='all', check=True):

    if check:

        digest_item(item, 'mdtraj.Trajectory')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import to_mdtraj_Topology
    from .mdtraj_Topology import to_molsysmt_Topology as mdtraj_Topology_to_molsysmt_Topology

    tmp_item = to_mdtraj_Topology(item, check=False)
    tmp_item = mdtraj_Topology_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices,
            check=False)

    return tmp_item

