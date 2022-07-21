from molsysm._private.exception import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.TrajectoryDict', to_form='molsysmt.TrajectoryDict')
def add(to_item, item):

    raise NotImplementedMethodError()

