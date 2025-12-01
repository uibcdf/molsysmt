
simulation_parameters = {
    'temperature', 'integrator', 'collisions_rate', 'integration_timestep',
    'initial_velocities_to_temperature', 'constraint_tolerance', 'platform', 'cuda_precision'
}


def is_simulation_dict(dictionary):
    """Return True if the dictionary only contains simulation parameter keys."""

    keys=set(dictionary.keys())
    output = (keys <= simulation_parameters)

    return output
