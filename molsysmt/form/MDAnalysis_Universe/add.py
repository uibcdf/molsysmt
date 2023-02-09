from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='MDAnalysis.Universe', to_form='MDAnalysis.Universe')
def add(to_item, item):

    raise NotImplementedMethodError()

