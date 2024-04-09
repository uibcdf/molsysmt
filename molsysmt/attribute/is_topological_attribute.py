from molsysmt._private.digestion import digest

@digest()
def is_topological_attribute(attribute, skip_digestion=False):

    from . import attributes

    return attributes[attribute]['topological']

