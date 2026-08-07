from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:alphafold_id')
def copy(item, skip_digestion=False):

    raise NotImplementedMethodError()

