from molsysmt._private.digestion import digest

@digest(form='file:h5')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all'):

    from . import to_mdtraj_HDF5TrajectoryFile
    from ..mdtraj_HDF5TrajectoryFile import to_molsysmt_Structures as mdtraj_HDF5TrajectoryFile_to_molsysmt_Structures

    tmp_item = to_mdtraj_HDF5TrajectoryFile(item)
    tmp_item = mdtraj_HDF5TrajectoryFile_to_molsysmt_Structures(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

def _to_molsysmt_Structures(item, atom_indices='all', structure_indices='all'):

    return to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)
