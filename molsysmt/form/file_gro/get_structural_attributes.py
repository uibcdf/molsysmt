from molsysmt._private.argdigest import arg_digest
import types

form = 'file:gro'

@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    from molsysmt.form.molsysmt_MolSys.get_structural_attributes import get_coordinates_from_atom as aux_get
    from molsysmt.basic import convert
    tmp_item = convert(item, to_form='molsysmt.MolSys', skip_digestion=True)
    return aux_get(tmp_item, indices=indices, structure_indices=structure_indices, skip_digestion=True)

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
