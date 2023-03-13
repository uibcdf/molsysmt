from molsysmt._private.digestion import digest

@digest(form='mdtraj.Trajectory')
def has_attribute(molecular_system, attribute):

    output = False

    # Check attributes list first

    from . import attributes

    if not attributes[attribute]:
        return output

    return output

