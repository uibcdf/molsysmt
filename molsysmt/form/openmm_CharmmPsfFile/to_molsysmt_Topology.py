from molsysmt._private.digestion import digest

@digest(form='openmm.CharmmPsfFile')
def to_molsysmt_Topology(item, atom_indices='all'):

    from . import to_openmm_Topology
    from ..openmm_Topology import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology

    tmp_item = to_openmm_Topology(item)
    tmp_item = openmm_Topology_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices)

    return tmp_item

