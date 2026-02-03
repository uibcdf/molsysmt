from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.GROFileHandler')
def copy(item, output_filename=None, skip_digestion=False):

    raise NotImplementedMethodError
