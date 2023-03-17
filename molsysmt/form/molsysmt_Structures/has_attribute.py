from molsysmt._private.digestion import digest

@digest(form='molsysmt.Structures')
def has_attribute(molecular_system, attribute):

    from . import attributes

    output = attributes[attribute]

    ###
    ### STRUCTURAL ATTRIBUTES
    ###

    if attribute=='structure_id':
        if molecular_system.structure_id is None:
            output = False

    elif attribute=='coordinates':
        if molecular_system.coordinates is None:
            output = False

    elif attribute=='velocities':
        if molecular_system.velocities is None:
            output = False

    elif attribute=='time':
        if molecular_system.time is None:
            output = False

    elif attribute in ['box', 'box_shape', 'box_angles', 'box_lengths', 'box_volume']:
        if molecular_system.box is None:
            output = False

    elif attribute=='occupancy':
        if molecular_system.occupancy is None:
            output = False

    elif attribute=='alternate_location':
        if molecular_system.alternate_location is None:
            output = False

    elif attribute=='b_factor':
        if molecular_system.b_factor is None:
            output = False


    return output
