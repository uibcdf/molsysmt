from molsysmt._private.digestion import digest

@digest(form='molsysmt.H5MSMFileHandler')
def has_attribute(molecular_system, attribute):

    from . import attributes

    output = attributes[attribute]

    return output

