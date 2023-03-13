from molsysmt._private.digestion import digest

@digest(form='biopython.Seq')
def has_attribute(molecular_system, attribute):

    from . import attributes

    output = attributes[attribute]

    return output

