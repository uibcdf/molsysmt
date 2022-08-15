
from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='mdtraj.Topology', to_form='mdtraj.Topology')
def add(to_item, item):

    raise NotImplementedMethodError()

