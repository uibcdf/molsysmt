trajectory_parameters = {
    'time', 'step', 'coordinates', 'velocities', 'box',
    'potential_energy', 'kinetic_energy', 'total_energy', 'temperature'
}


def is_trajectory_dict(dictionary):

    keys=set(dictionary.keys())
    output = (keys <= trajectory_parameters)

    return output


