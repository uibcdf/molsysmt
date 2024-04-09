from molsysmt._private.digestion import digest

@digest()
def is_structural_attribute(attribute, skip_digestion=False):

    from . import attributes

    return attributes[attribute]['structural']

