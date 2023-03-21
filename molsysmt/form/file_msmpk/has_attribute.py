from molsysmt._private.digestion import digest

@digest(form='file:msmpk')
def has_attribute(molecular_system, attribute):

    from . import attributes

    output = attributes[attribute]

    return output

