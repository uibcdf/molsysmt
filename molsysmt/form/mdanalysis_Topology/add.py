from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='mdanalysis.Topology', to_form='mdanalysis.Topology')
def add(to_item, item, digest=True):

    raise NotImplementedMethodError()

