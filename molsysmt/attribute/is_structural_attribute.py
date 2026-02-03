from molsysmt._private.arg_digestion import arg_digest

@arg_digest()
def is_structural_attribute(attribute, skip_digestion=False):

    from . import attributes

    return attributes[attribute]['structural']

