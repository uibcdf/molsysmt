from molsysm._private.exception import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='mdanalysis.Universe', to_form='mdanalysis.Universe')
def add(to_item, item):

    raise NotImplementedMethodError()

