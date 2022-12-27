from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='openmm.Context')
def append_structures(item, structure_id=None, time=None, coordinates=None, box=None):

    raise NotImplementedMethodError()

