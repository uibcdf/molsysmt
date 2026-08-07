from molsysmt._private.argdigest import arg_digest
import types

form='file:prmtop'

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    from .to_openmm_AmberPrmtopFile import to_openmm_AmberPrmtopFile
    from molsysmt.form.openmm_AmberPrmtopFile.get_topological_attributes import get_n_atoms_from_system as aux_get
    tmp_item = to_openmm_AmberPrmtopFile(item, skip_digestion=True)
    return aux_get(tmp_item, skip_digestion=True)

@arg_digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):
    from .to_openmm_AmberPrmtopFile import to_openmm_AmberPrmtopFile
    from molsysmt.form.openmm_AmberPrmtopFile.get_topological_attributes import get_atom_id_from_atom as aux_get
    tmp_item = to_openmm_AmberPrmtopFile(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
