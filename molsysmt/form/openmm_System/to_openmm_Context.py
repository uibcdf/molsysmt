from molsysmt._private.digestion import digest

@digest(form='openmm.System')
def to_openmm_Context(item, atom_indices='all', structure_indices='all'):

    from molsysmt.basic import convert, get
    from openmm import Context

    positions = get(molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                    coordinates=True)
    positions = puw.convert(positions[0], to_form='openmm.unit', to_unit='nm')
    simulation = convert(molecular_system, to_form='molsysmt.Simulation')

    integrator = simulation.to_openmm_Integrator()
    platform = simulation.to_openmm_Platform()

    properties = simulation.get_openmm_Context_parameters()

    tmp_item = Context(item, integrator, platform, properties)
    tmp_item.setPositions(positions)
    if simulation.initial_velocities_to_temperature:
        temperature = puw.convert(simulation.temperature, to_form='openmm.unit', to_unit='K')
        tmp_item.setVelocitiesToTemperature(temperature)

    return tmp_item

def _to_openmm_Context(item,  atom_indices='all', structure_indices='all'):

    return to_openmm_Context(item, atom_indices=atom_indices, structure_indices=structure_indices)

