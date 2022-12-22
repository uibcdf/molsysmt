from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.Structures')
def append_structures(item, structure_id=None, time=None, coordinates=None, box=None, digest=True):

    item.append_structures(structure_id=structure_id, time=time, coordinates=coordinates, box=box, digest=False)

    pass

