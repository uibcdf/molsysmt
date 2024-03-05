from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='molsysmt.PDBFileHandler')
def copy(item, output_filename=None, skip_digestion=False):

    raise NotImplementedMethodError
