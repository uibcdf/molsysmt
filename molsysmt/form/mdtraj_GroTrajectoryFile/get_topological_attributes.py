from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotWithThisFormError
from molsysmt._private.variables import is_all
import types

form = 'mdtraj.GroTrajectoryFile'

def _get_n_atoms(item):
    item._file.seek(0)
    return item.read()[0].shape[1]


@arg_digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False):
    if indices is None:
        return None
    if is_all(indices):
        return list(range(_get_n_atoms(item)))
    return list(indices)


@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    return _get_n_atoms(item)

@arg_digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):
    raise NotWithThisFormError(caller='molsysmt.form.mdtraj_GroTrajectoryFile.get_n_groups_from_system', form=form, requested_attribute='n_groups', message='This form does not store topology information directly. Please convert to a topology-enabled form first.')

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
