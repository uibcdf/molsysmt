from molsysmt._private.digestion import digest

@digest(form='molsysmt.Topology2')
def has_attribute(molecular_system, attribute):

    from . import attributes

    output = attributes[attribute]

    raise NotImplementedError

