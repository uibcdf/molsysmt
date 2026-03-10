from molsysmt._private.arg_digestion import arg_digest
import types

form = 'MDAnalysis.AtomGroup'


@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys.get_structural_attributes import get_coordinates_from_atom as aux_get

    tmp_item = to_molsysmt_MolSys(item, structure_indices=structure_indices, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, structure_indices='all', skip_digestion=True)


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
