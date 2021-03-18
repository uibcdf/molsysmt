def to_openmm_Simulation (item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from .openmm_Topology import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology
    from molsysmt.forms.classes.api_openmm_Topology import to_openmm_Simulation as openmm_Topology_to_openmm_Simulation

    tmp_item = molsysmt_MolSys_to_openmm_Topology(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    molecular_system = molecular_system.combine_with_items(tmp_item)
    tmp_item = openmm_Topology_to_openmm_Simulation(tmp_item, molecular_system=molecular_system, atom_indices='all', frame_indices=0)

    return tmp_item

def from_openmm_Simulation(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.io.topology.classes import from_openmm_Simulation as molsysmt_Topology_from_openmm_Simulation
    from molsysmt.native.io.trajectory.classes import from_openmm_Simulation as molsysmt_Trajectory_from_openmm_Simulation

    tmp_item = MolSys()
    tmp_item.topology = molsysmt_Topology_from_openmm_Simulation(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory = molsysmt_Trajectory_from_openmm_Simulation(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

