def from_openmm_Modeller(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from .openmm_Topology import from_openmm_Topology as openmm_Topology_to_molsysmt_Topology
    from molsysmt.forms.classes.api_openmm_Modeller import to_openmm_Topology as openmm_Modeller_to_molsysmt_Topology

    tmp_item = openmm_Modeller_to_molsysmt_Topology(item)
    tmp_item = openmm_Topology_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices)

    return tmp_item

