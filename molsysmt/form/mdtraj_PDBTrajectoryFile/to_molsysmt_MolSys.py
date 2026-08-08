from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.PDBTrajectoryFile')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import MolSys
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from .to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.to_molsysmt_Topology import to_molsysmt_Topology

    tmp_item = MolSys()
    tmp_item.structures = to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                 structure_indices=structure_indices, skip_digestion=True)
    mdtraj_topology = to_mdtraj_Topology(item, skip_digestion=True)
    tmp_item.topology = to_molsysmt_Topology(mdtraj_topology, skip_digestion=True)

    return tmp_item
