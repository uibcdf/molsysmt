from molsysmt._private.digestion import digest

@digest(form='mmcif.PdbxContainers.DataContainer')
def has_attribute(molecular_system, attribute, skip_digestion=False):

    from . import attributes

    output = attributes[attribute]

    return output

