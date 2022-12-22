from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='mdanalysis.Universe', to_form='mdanalysis.Universe')
def add(to_item, item, digest=True):

    raise NotImplementedMethodError()

