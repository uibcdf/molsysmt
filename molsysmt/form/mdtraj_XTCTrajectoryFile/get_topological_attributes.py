from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import NotWithThisFormError
import types

form = 'mdtraj.XTCTrajectoryFile'

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    raise NotWithThisFormError(caller='molsysmt.form.mdtraj_XTCTrajectoryFile.get_n_atoms_from_system', form=form, requested_attribute='n_atoms', message='This form does not store topology information directly. Please convert to a topology-enabled form first.')

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
