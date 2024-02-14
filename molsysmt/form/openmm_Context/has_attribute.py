from molsysmt._private.digestion import digest

@digest(form='openmm.Context')
def has_attribute(molecular_system, attribute, skip_digestion=False):

    from . import attributes

    output = attributes[attribute]

    return output

