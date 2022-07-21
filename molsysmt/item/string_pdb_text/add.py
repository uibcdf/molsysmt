from molsysm._private.exception import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='string:pdb_text', to_form='string:pdb_text')
def add(to_item, item):

    raise NotImplementedMethodError()

