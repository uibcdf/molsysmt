from molsysmt._private.digestion import digest

@digest(form='file:xtc')
def to_molsysmt_StructuresOld(item, atom_indices='all', structure_indices='all'):

    from . import to_mdtraj_XTCTrajectoryFile
    from ..mdtraj_XTCTrajectoryFile import to_molsysmt_StructuresOld as mdtraj_XTCTrajectoryFile_to_molsysmt_StructuresOld

    tmp_item = to_mdtraj_XTCTrajectoryFile(item)
    tmp_item = mdtraj_XTCTrajectoryFile_to_molsysmt_StructuresOld(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

