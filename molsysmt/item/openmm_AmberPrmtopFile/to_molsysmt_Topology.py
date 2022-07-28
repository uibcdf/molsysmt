from molsysmt._private.digestion import digest

@digest(form='openmm.AmberPrmtopFile')
def to_molsysmt_Topology(item, atom_indices='all'):

    from . import to_openmm_Topology
    from ..api_openmm_Topology import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology

    tmp_item = to_openmm_Topology(item, check=check)
    tmp_item = openmm_Topology_to_molsysmt_Topology(item, atom_indices=atom_indices, check=check)

    return tmp_item

