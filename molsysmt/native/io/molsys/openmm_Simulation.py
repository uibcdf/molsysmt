def to_openmm_Simulation (item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from .openmm_Topology import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology
    from molsysmt.forms.api_openmm_Topology import to_openmm_Simulation as openmm_Topology_to_openmm_Simulation

    tmp_item, tmp_molecular_system = molsysmt_MolSys_to_openmm_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = openmm_Topology_to_openmm_Simulation(tmp_item, tmp_molecular_system, atom_indices='all', frame_indices=0)

    return tmp_item, tmp_molecular_system

def from_openmm_Simulation(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.io.topology import from_openmm_Simulation as molsysmt_Topology_from_openmm_Simulation
    from molsysmt.native.io.trajectory import from_openmm_Simulation as molsysmt_Trajectory_from_openmm_Simulation

    tmp_item = MolSys()
    tmp_item.topology, _ = molsysmt_Topology_from_openmm_Simulation(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory, _ = molsysmt_Trajectory_from_openmm_Simulation(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    if tmp_molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

