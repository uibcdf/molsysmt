from molsysmt._private.digestion import digest

@digest(form='molsysmt.StructuresDict')
def has_attribute(molecular_system, attribute):

    from . import attributes

    output = attributes[attribute]

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


    return output
