from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='molsysmt.StructuresDict')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):

    from . import attributes

    output = attributes[attribute]

    if not include_none:

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

        elif attribute in ['temperature', 'potential_energy', 'kinetic_energy']:
            if molecular_system.get(attribute) is None:
                output = False

        elif attribute == 'total_energy':
            if (
                molecular_system.get('potential_energy') is None
                or molecular_system.get('kinetic_energy') is None
            ):
                output = False


    return output
