from molsysmt._private.arg_digestion import arg_digest
import types

form='openmm.PDBFile'

@arg_digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):
    from molsysmt.form.openmm_Topology import get_atom_id_from_atom as aux_get
    return aux_get(item.getTopology(), indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):
    from molsysmt.form.openmm_Topology import get_atom_name_from_atom as aux_get
    return aux_get(item.getTopology(), indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_atom_type_from_atom(item, indices='all', skip_digestion=False):
    from molsysmt.form.openmm_Topology import get_atom_type_from_atom as aux_get
    return aux_get(item.getTopology(), indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    return item.getTopology().getNumAtoms()

@arg_digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):
    return item.getTopology().getNumResidues()

# ... add more if needed, or use a generic delegation loop if we want full parity ...

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
