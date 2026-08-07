from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:mol2')
def to_openmm_Topology(item, atom_indices='all', skip_digestion=False):

    from .to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.to_openmm_Topology import to_openmm_Topology as mdtraj_Topology_to_openmm_Topology

    tmp_item = to_mdtraj_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = mdtraj_Topology_to_openmm_Topology(tmp_item, skip_digestion=True)

    return tmp_item
