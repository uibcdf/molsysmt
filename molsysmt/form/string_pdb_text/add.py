from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='string:pdb_text', to_form='string:pdb_text', digest=True)
def add(to_item, item):

    raise NotImplementedMethodError()

