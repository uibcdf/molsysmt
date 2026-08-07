from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotWithThisFormError
import types

form='molsysmt.Topology'

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):
    raise NotWithThisFormError(caller='molsysmt.form.molsysmt_Topology.get_n_structures_from_system', form=form, requested_attribute='n_structures')

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):
    raise NotWithThisFormError(caller='molsysmt.form.molsysmt_Topology.get_box_from_system', form=form, requested_attribute='box')

@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    raise NotWithThisFormError(caller='molsysmt.form.molsysmt_Topology.get_coordinates_from_atom', form=form, requested_attribute='coordinates')

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
