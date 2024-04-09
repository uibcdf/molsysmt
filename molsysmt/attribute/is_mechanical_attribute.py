from molsysmt._private.digestion import digest

@digest()
def is_mechanical_attribute(attribute, skip_digestion=False):

    from . import attributes

    return attributes[attribute]['mechanical']

