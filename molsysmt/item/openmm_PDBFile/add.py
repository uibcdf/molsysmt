from molsysm._private.exception import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='openmm.PDBFile', to_form='openmm.PDBFile')
def add(to_item, item):

    raise NotImplementedMethodError()


