from molsysmt._private.digestion import digest

@digest(form='file:gro')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    #from . import to_mdtraj_Topology
    #from ..mdtraj_Topology import to_molsysmt_Topology as mdtraj_Topology_to_molsysmt_Topology

    #tmp_item = to_mdtraj_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    #tmp_item = mdtraj_Topology_to_molsysmt_Topology(tmp_item, skip_digestion=True)

    from molsysmt.native import Topology
    from ..molsysmt_Topology import extract

    tmp_item = Topology()

    n_atoms = item.n_atoms
    n_groups = item.n_residues
    n_chains = item.n_chains
    n_bonds = item.n_bonds


    # atoms

    atom_name_array = np.empty(n_atoms, dtype=object)
    atom_id_array = np.empty(n_atoms, dtype=int)
    atom_type_array = np.empty(n_atoms, dtype=object)
    group_index_array = np.empty(n_atoms, dtype=int)
    chain_index_array = np.empty(n_atoms, dtype=int)


    return tmp_item

