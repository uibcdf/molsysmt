from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
import types

form='biopython.PDBStructure'

@arg_digest(form=form)
def get(item, element='system', selection='all', syntax='MolSysMT', structure_indices='all', 
        output_type='values', skip_digestion=False, **kwargs):

    from molsysmt.basic import get as msm_get
    from .to_molsysmt_MolSys import to_molsysmt_MolSys

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)

    return msm_get(tmp_item, element=element, selection=selection, structure_indices=structure_indices,
                   output_type=output_type, skip_digestion=True, **kwargs)

@arg_digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):
    return get(item, element='atom', selection=indices, atom_id=True, skip_digestion=True)

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    return len(list(item.get_atoms()))

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get')]
