from molsysm._private.exception import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.Structures')
def append_structures(item, step=None, time=None, coordinates=None, box=None):

    item.append_structures(step=step, time=time, coordinates=coordinates, box=box)

    pass

