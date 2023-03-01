from molsysmt._private.digestion import digest

@digest(form='molsysmt.StructuresDict')
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

        if argument=='structure_index':
            if argument in molecular_system:
                output = True

        elif argument=='structure_id':
            if argument in molecular_system:
                output = True

        elif argument=='coordinates':
            if argument in molecular_system:
                output = True

        elif argument=='time':
            if argument in molecular_system:
                output = True

        elif argument=='box':
            if argument in molecular_system:
                output = True

        elif argument=='occupancy':
            if argument in molecular_system:
                output = True

        elif argument=='alternate_location':
            if argument in molecular_system:
                output = True

        elif argument=='b_factor':
            if argument in molecular_system:
                output = True


        outputs.append(output)

    if len(outputs)==1:
        return outputs[0]
    else:
        return outputs

