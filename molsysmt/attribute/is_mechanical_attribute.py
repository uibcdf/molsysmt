from molsysmt._private.argdigest import arg_digest

@arg_digest()
def is_mechanical_attribute(attribute, skip_digestion=False):

    from . import attributes

    return attributes[attribute]['mechanical']

