from molsysmt._private.digestion import digest

@digest()
def has_attribute(molecular_system, attribute, digest=True):

    from . import where_is_attribute

    output_item, output_form = where_is_attribute(molecular_system, attribute, digest=False)

    output = False
    if output_item is not None:
        output = True

    return output

