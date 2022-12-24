from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='string:aminoacids3')
def append_structures(item, structure_id=None, time=None, coordinates=None, box=None, digest=True):

    raise NotImplementedMethodError()


