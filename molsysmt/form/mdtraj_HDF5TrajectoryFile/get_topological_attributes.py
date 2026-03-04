from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import NotWithThisFormError
import types

form = 'mdtraj.HDF5TrajectoryFile'

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    return item.topology.n_atoms

@arg_digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):
    return item.topology.n_residues

@arg_digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_atom_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
