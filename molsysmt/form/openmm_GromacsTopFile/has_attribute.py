from molsysmt._private.digestion import digest

@digest(form='openmm.GromacsTopFile')
def has_attribute(molecular_system, attribute):

    from . import attributes

    output = attributes[attribute]

    return output

