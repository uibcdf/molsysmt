from molsysmt._private.argdigest import arg_digest
import types

form='openmm.AmberPrmtopFile'

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    return item.topology.getNumAtoms()

@arg_digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):
    return item.topology.getNumResidues()

@arg_digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):
    from molsysmt.form.openmm_Topology.get_topological_attributes import get_atom_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
