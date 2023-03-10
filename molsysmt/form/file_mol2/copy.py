from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:mol2')
def extract(item, output_filename=None):

    if output_filename is None:
        output_filename = item

    raise NotImplementedMethodError()

