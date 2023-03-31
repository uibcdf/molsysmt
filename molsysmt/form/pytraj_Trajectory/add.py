from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='pytraj.Trajectory', to_form='pytraj.Trajectory')
def add(to_item, item, atom_indices='all', structure_indices='all'):

    raise NotImplementedMethodError()

