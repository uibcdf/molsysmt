from molsysmt._private.digestion import digest

@digest(form='openmm.Topology')
def has_attribute(molecular_system, attribute):

    from . import attributes

    output = attributes[attribute]



    if attribute in ['box', 'box_shape', 'box_angles', 'box_lengths', 'box_volume']:
        if molecular_system.getPeriodicBoxVectors() is None:
            output = False

    return output

