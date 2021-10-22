def to_openmm_System(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from .openmm_Topology import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology
    from molsysmt.forms.api_openmm_Topology import to_openmm_System as openmm_Topology_to_openmm_System

    tmp_item, tmp_molecular_system = molsysmt_MolSys_to_openmm_Topology(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = openmm_Topology_to_openmm_System(tmp_item, molecular_system=tmp_molecular_system, atom_indices='all')

    return tmp_item, tmp_molecular_system
