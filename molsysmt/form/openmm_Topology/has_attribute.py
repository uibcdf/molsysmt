from molsysmt._private.digestion import digest

@digest(form='openmm.Topology')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):

    from . import attributes

    output = attributes[attribute]

    if not include_none:

        if attribute in ['box', 'box_shape', 'box_angles', 'box_lengths', 'box_volume']:
            if molecular_system.getPeriodicBoxVectors() is None:
                output = False

    return output

