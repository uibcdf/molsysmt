from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:pir')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):

    from . import attributes

    output = attributes[attribute]

    if not include_none:
        pass

    return output
