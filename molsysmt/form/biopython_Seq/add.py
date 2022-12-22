from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='biopython.Seq', to_form='biopython.Seq')
def add(to_item, item, digest=True):

    raise NotImplementedMethodError()

