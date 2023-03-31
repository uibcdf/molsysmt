from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='openmm.AmberPrmtopFile', to_form='openmm.AmberPrmtopFile')
def add(to_item, item, atom_indices='all'):

    raise NotImplementedMethodError()

