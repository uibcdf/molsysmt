from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='string:pdb_id')
def copy(item):

    raise NotImplementedMethodError()

