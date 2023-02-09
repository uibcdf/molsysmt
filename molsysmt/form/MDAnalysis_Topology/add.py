from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='MDAnalysis.Topology', to_form='MDAnalysis.Topology')
def add(to_item, item):

    raise NotImplementedMethodError()

