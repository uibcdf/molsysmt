from molsysmt._private.digestion import digest

@digest(form='molsysmt.StructuresDict')
def has_attribute(molecular_system, attribute):

    from . import attributes

    output = attributes[attribute]

    ###
    ### STRUCTURAL ATTRIBUTES
    ###

    if attribute=='n_atoms':
        if ('coordinates' not in molecular_system) and ('velocities' not in molecular_system):
            output = False

    if attribute=='structure_id':
        if attribute not in molecular_system:
            output = False

    elif attribute=='coordinates':
        if attribute not in molecular_system:
            output = False

    elif attribute=='velocities':
        if attribute not in molecular_system:
            output = False

    elif attribute=='time':
        if attribute not in molecular_system:
            output = False

    elif attribute in ['box', 'box_shape', 'box_angles', 'box_lengths', 'box_volume']:
        if 'box' not in molecular_system:
            output = False

    elif attribute=='occupancy':
        if attribute not in molecular_system:
            output = False

    elif attribute=='alternate_location':
        if attribute not in molecular_system:
            output = False

    elif attribute=='b_factor':
        if attribute not in molecular_system:
            output = False


    return output
