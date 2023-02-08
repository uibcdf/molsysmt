from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='mdanalysis.topology_CRDParser', to_form='mdanalysis.topology_CRDParser')
def add(to_item, item):

    raise NotImplementedMethodError()

