from molsysmt._private.arg_digestion import arg_digest
import types

form = 'file:pdb'

@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    from .to_molsysmt_PDBFileHandler import to_molsysmt_PDBFileHandler
    from molsysmt.form.molsysmt_PDBFileHandler.get_structural_attributes import get_coordinates_from_atom as aux_get
    tmp_item = to_molsysmt_PDBFileHandler(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):
    from .to_molsysmt_PDBFileHandler import to_molsysmt_PDBFileHandler
    from molsysmt.form.molsysmt_PDBFileHandler.get_structural_attributes import get_box_from_system as aux_get
    tmp_item = to_molsysmt_PDBFileHandler(item, skip_digestion=True)
    return aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
