from molsysmt._private.digestion import digest

@digest(form='openmm.PDBFile')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from .to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    tmp_item = openmm_Topology_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

