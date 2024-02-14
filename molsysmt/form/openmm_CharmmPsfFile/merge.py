from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='openmm.CharmmPsfFile', to_form='openmm.CharmmPsfFile')
def merge(items, atom_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

