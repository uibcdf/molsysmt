from molsysmt._private.digestion import digest

@digest(form='pytraj.Topology')
def has_attribute(molecular_system, attribute):

    output = False

    # Check attributes list first

    from . import attributes

    if not attributes[attribute]:
        return output

    return output

