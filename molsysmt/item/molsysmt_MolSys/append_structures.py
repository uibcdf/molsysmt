from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys')
def append_structures(item, step=None, time=None, coordinates=None, box=None):

    item.structures.append_structures(step=step, time=time, coordinates=coordinates, box=box)

    pass

