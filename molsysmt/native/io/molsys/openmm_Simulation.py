
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

