from molsysm._private.exception import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='pdbfixer.PDBFixer', to_form='pdbfixer.PDBFixer')
def add(to_item, item):

    raise NotImplementedMethodError()

