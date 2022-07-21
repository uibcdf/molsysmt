from molsysm._private.exception import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:prmtop', to_form='file:prmtop')
def add(to_item, item):

    raise NotImplementedMethodError()

