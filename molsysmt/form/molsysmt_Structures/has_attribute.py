from molsysmt._private.digestion import digest

@digest(form='molsysmt.Structures')
def has_attribute(molecular_system, **kwargs):

    arguments = []
    for key in kwargs.keys():
        if kwargs[key]:
            arguments.append(key)

    outputs = []

    for argument in arguments:

        output = False

        ###
        ### STRUCTURAL ATTRIBUTES
        ###

        if argument in ['structure_index', 'structure_id', 'coordinates']:
            if molecular_system.structures.n_structures :
                output = True

        elif argument=='time':
            if molecular_system.structures.time is not None:
                output = True

        elif argument=='box':
            if molecular_system.structures.box is not None:
                output = True

        elif argument=='occupancy':
            if molecular_system.structures.occupancy is not None:
                output = True

        elif argument=='alternate_location':
            if molecular_system.structures.alternate_location is not None:
                output = True

        elif argument=='b_factor':
            if molecular_system.structures.b_factor is not None:
                output = True


        outputs.append(output)

    if len(outputs)==1:
        return outputs[0]
    else:
        return outputs

