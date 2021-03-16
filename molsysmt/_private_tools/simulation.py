
simulation_parameters = {
    'temperature', 'integrator', 
}

def is_simulation_dict(dictionary):

    keys=set(dictionary.keys())
    output = (keys <= simulation_parameters)

    return output


