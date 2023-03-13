from molsysmt._private.digestion import digest

@digest(form='molsysmt.Structures')
def has_attribute(molecular_system, attribute):

    output = False

    # Check attributes list first

    from . import attributes

    if not attributes[attribute]:
        return output

    ###
    ### STRUCTURAL ATTRIBUTES
    ###

    if attribute=='n_structures':
        output = True

    elif attribute in ['structure_index', 'structure_id', 'coordinates']:
        if molecular_system.structures.n_structures :
            output = True

    elif attribute=='time':
        if molecular_system.structures.time is not None:
            output = True

    elif attribute in ['box', 'box_shape', 'box_angles', 'box_lengths', 'box_volume']:
        if molecular_system.structures.box is not None:
            output = True

    elif attribute=='occupancy':
        if molecular_system.structures.occupancy is not None:
            output = True

    elif attribute=='alternate_location':
        if molecular_system.structures.alternate_location is not None:
            output = True

    elif attribute=='b_factor':
        if molecular_system.structures.b_factor is not None:
            output = True


    return output
