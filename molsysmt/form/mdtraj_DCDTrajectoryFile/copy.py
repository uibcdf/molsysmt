from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='mdtraj.DCDTrajectoryFile')
def copy(item, skip_digestion=False):

    raise NotImplementedMethodError()

