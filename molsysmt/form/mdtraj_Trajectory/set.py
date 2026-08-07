from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError

form='mdtraj.Trajectory'

@arg_digest(form=form)
def set_coordinates_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):
    raise NotImplementedMethodError()

@arg_digest(form=form)
def set_box_to_system(item, structure_indices='all', value=None, skip_digestion=False):
    raise NotImplementedMethodError()
