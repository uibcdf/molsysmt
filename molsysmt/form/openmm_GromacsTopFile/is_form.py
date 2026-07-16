
def is_form(item):
    from openmm.app import GromacsTopFile

    return isinstance(item, GromacsTopFile)
