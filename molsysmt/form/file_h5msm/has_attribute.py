from molsysmt._private.digestion import arg_digest

@arg_digest(form='file:h5msm')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=True):

    from . import attributes

    output = attributes[attribute]

    if not include_none:
        pass

    return output

