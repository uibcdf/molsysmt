from molsysmt._private.arg_digestion import arg_digest
import types

form = 'file:pdb'

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    from .to_molsysmt_PDBFileHandler import to_molsysmt_PDBFileHandler
    from molsysmt.form.molsysmt_PDBFileHandler.get_topological_attributes import get_n_atoms_from_system as aux_get
    tmp_item = to_molsysmt_PDBFileHandler(item, skip_digestion=True)
    return aux_get(tmp_item, skip_digestion=True)

@arg_digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):
    from .to_molsysmt_PDBFileHandler import to_molsysmt_PDBFileHandler
    from molsysmt.form.molsysmt_PDBFileHandler.get_topological_attributes import get_n_groups_from_system as aux_get
    tmp_item = to_molsysmt_PDBFileHandler(item, skip_digestion=True)
    return aux_get(tmp_item, skip_digestion=True)

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
