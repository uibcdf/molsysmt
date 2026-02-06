from molsysmt.exceptions import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:cif.gz')
def copy(item, output_filename=None, skip_digestion=False):

    if output_filename is None:
        output_filename = item

    raise NotImplementedMethodError()

