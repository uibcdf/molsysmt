from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='MDAnalysis.topology.CRDParser', to_form='MDAnalysis.topology.CRDParser')
def add(to_item, item):

    raise NotImplementedMethodError()

