from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openff.Topology')
def has_attribute(item, attribute, include_none=False, skip_digestion=False):

    from .attributes import attributes
    return attributes.get(attribute, False)
