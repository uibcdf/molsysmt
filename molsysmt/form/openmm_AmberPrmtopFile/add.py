from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openmm.AmberPrmtopFile', to_form='openmm.AmberPrmtopFile')
def add(to_item, item, atom_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

