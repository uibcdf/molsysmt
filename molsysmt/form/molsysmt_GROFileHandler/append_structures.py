from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import arg_digest

@arg_digest(form='molsysmt.GROFileHandler')
def append_structures(item, structure_id=None, time=None, coordinates=None, box=None, skip_digestion=False):

    raise NotImplementedMethodError()

