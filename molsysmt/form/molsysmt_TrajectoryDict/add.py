from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.TrajectoryDict', to_form='molsysmt.TrajectoryDict')
def add(to_item, item, digest=True):

    raise NotImplementedMethodError()

