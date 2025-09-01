from molsysmt._private.digestion import digest

@digest(form='nglview.NGLWidget')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):

    from . import attributes

    output = attributes[attribute]

    if not include_none:
        pass

    return output

