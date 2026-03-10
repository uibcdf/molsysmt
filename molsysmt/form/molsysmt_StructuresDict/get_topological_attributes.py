from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import NotWithThisFormError
import types

form = 'molsysmt.StructuresDict'


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
