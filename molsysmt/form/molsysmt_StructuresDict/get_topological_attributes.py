from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotWithThisFormError
from molsysmt._private.variables import is_all
import types

form = 'molsysmt.StructuresDict'


@arg_digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False):
    if indices is None:
        return None
    if is_all(indices):
        return list(range(item['coordinates'].shape[1]))
    return list(indices)


@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    return item['coordinates'].shape[1]


@arg_digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):
    raise NotWithThisFormError(
        caller='molsysmt.form.molsysmt_StructuresDict.get_n_groups_from_system',
        form=form,
        requested_attribute='n_groups',
    )


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
