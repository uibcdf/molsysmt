import simtk.unit as unit

def to_openmm_Simulation (item, atom_indices='all', frame_indices='all', topology_item=None,
                          trajectory_item=None, coordinates_item=None, box_item=None, forcefield=None,
                          non_bonded_method='no_cutoff', non_bonded_cutoff=None, constraints=None,
                          rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                          flexible_constraints=False, integrator='Langevin', temperature='300.0 K',
                          collisions_rate='1.0 1/ps', integration_timestep= '2.0 fs',
                          platform='CUDA', **kwargs):

    from .openmm_Topology import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology
    from molsysmt.forms.classes.api_openmm_Topology import to_openmm_Simulation as openmm_Topology_to_openmm_Simulation
    from molsysmt import get

    tmp_item = molsysmt_MolSys_to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)

    if trajectory_item is None:
        trajectory_item = item

    coordinates = get(trajectory_item, target='atom', selection=atom_indices,
            frame_indices=frame_indices, coordinates=True)

    tmp_item = openmm_Topology_to_openmm_Simulation(tmp_item, trajectory_item=coordinates,
        atom_indices='all', frame_indices=0, forcefield=forcefield, non_bonded_method=non_bonded_method,
        non_bonded_cutoff=non_bonded_cutoff, constraints=constraints, rigid_water=rigid_water,
        remove_cm_motion=remove_cm_motion, hydrogen_mass=hydrogen_mass,
        switch_distance=switch_distance, flexible_constraints=flexible_constraints,
        integrator=integrator, temperature=temperature, collisions_rate=collisions_rate,
        integration_timestep=integration_timestep, platform=platform, **kwargs)

    return tmp_item

def from_openmm_Simulation(item, atom_indices='all', frame_indices='all', topology_item=None,
                           trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.io.topology.classes import from_openmm_Simulation as molsysmt_Topology_from_openmm_Simulation
    from molsysmt.native.io.trajectory.classes import from_openmm_Simulation as molsysmt_Trajectory_from_openmm_Simulation

    tmp_item = MolSys()
    tmp_item.topology = molsysmt_Topology_from_openmm_Simulation(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory = molsysmt_Trajectory_from_openmm_Simulation(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item
