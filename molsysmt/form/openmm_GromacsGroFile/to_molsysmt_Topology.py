from molsysmt._private.digestion import digest

@digest(form='openmm.GromacsGroFile')
def to_molsysmt_Topology(item, atom_indices='all', digest=True):

    from . import to_openmm_Topology
    from ..openmm_Topology import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology

    tmp_item = to_openmm_Topology(item, digest=False)
    tmp_item = openmm_Topology_to_molsysmt_Topology(item, atom_indices=atom_indices, digest=False)

    return tmp_item

