from molsysmt._private.digestion import digest

@digest(form='openmm.System')
def to_openmm_Simulation(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.basic import convert, get
    from openmm.app import Simulation

    topology = convert(molecular_system, to_form='openmm.Topology', selection=atom_indices)
    positions = get(molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                    coordinates=True)
    positions = puw.convert(positions[0], to_form='openmm.unit', to_unit='nm')
    simulation = convert(molecular_system, to_form='molsysmt.Simulation')

    integrator = simulation.to_openmm_Integrator()
    platform = simulation.to_openmm_Platform()

    properties = simulation.get_openmm_Simulation_parameters()

    tmp_item = Simulation(topology, item, integrator, platform, properties)
    tmp_item.context.setPositions(positions)
    if simulation.initial_velocities_to_temperature:
        temperature = puw.convert(simulation.temperature, to_form='openmm.unit', to_unit='K')
        tmp_item.context.setVelocitiesToTemperature(temperature)

    return tmp_item

