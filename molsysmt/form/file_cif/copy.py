from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:cif')
def copy(item, output_filename=None, skip_digestion=False):

    if output_filename is None:
        output_filename = item

    raise NotImplementedMethodError()

