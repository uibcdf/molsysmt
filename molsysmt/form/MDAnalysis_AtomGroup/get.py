from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
import types

form='MDAnalysis.AtomGroup'

@arg_digest(form=form)
def get(item, element='system', selection='all', syntax='MolSysMT', structure_indices='all', 
        output_type='values', skip_digestion=False, **kwargs):

    from molsysmt.basic import get as msm_get
    
    indices = item.indices
    if not is_all(selection):
        from molsysmt.basic import select
        indices = select(item, selection=selection, syntax=syntax, skip_digestion=True)

    return msm_get(item.universe, element=element, selection=indices, structure_indices=structure_indices,
                   output_type=output_type, skip_digestion=True, **kwargs)

# Explicitly defining the most common getters required by MolSysMT
# These delegate to the generic get() function above.

@arg_digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):
    return get(item, element='atom', selection=indices, atom_id=True, skip_digestion=True)

@arg_digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):
    return get(item, element='atom', selection=indices, atom_name=True, skip_digestion=True)

@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    return get(item, element='atom', selection=indices, structure_indices=structure_indices, 
               coordinates=True, skip_digestion=True)

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    return item.n_atoms

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get')]
