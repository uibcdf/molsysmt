def from_openmm_Modeller(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from .openmm_Topology import from_openmm_Topology as openmm_Topology_to_molsysmt_Topology
    from molsysmt.forms.api_openmm_Modeller import to_openmm_Topology as openmm_Modeller_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = openmm_Modeller_to_molsysmt_Topology(item, molecular_system=molecular_system)
    tmp_item, tmp_molecular_system = openmm_Topology_to_molsysmt_Topology(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices)

    return tmp_item, tmp_molecular_system

