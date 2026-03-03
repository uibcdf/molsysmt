from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:dcd')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from ..mdtraj_DCDTrajectoryFile.to_mdtraj_DCDTrajectoryFile import to_mdtraj_DCDTrajectoryFile
    from ..mdtraj_DCDTrajectoryFile.to_molsysmt_MolSys import to_molsysmt_MolSys as mdtraj_DCDTrajectoryFile_to_molsysmt_MolSys

    tmp_item = to_mdtraj_DCDTrajectoryFile(item)
    tmp_item = mdtraj_DCDTrajectoryFile_to_molsysmt_MolSys(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, skip_digestion=True)

    return tmp_item

