from molsysmt._private.digestion import arg_digest
from molsysmt.dependencies import requires

@arg_digest(form='mdtraj.HDF5TrajectoryFile')
@requires('mdtraj')
def to_mdtraj_HDF5TrajectoryFile(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    from .extract import extract

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all, skip_digestion=True)

