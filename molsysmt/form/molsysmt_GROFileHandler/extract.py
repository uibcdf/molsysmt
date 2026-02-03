from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.GROFileHandler')
def extract(item, atom_indices='all', structure_indices='all', output_filename=None, copy_if_all=True, skip_digestion=False):

    raise NotImplementedMethodError()

