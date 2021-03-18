def to_openmm_System(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from .openmm_Topology import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology
    from molsysmt.forms.classes.api_openmm_Topology import to_openmm_System as openmm_Topology_to_openmm_System

    tmp_item = molsysmt_MolSys_to_openmm_Topology(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    molecular_system = molecular_system.combine_with_items(tmp_item)
    tmp_item = openmm_Topology_to_openmm_System(tmp_item, molecular_system=molecular_system, atom_indices='all')

    return tmp_item
