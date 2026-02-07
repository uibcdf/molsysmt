from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.PDBFileHandler')
def copy(item, output_filename=None, skip_digestion=False):

    raise NotImplementedMethodError
