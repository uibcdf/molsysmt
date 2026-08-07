from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:bcif')
def copy(item, output_filename=None, skip_digestion=False):

    if output_filename is None:
        output_filename = item

    raise NotImplementedMethodError()

