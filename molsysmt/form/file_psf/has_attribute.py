from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:psf')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):

    from . import attributes

    return bool(attributes.get(attribute, False))
