from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:xtc')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from .to_mdtraj_XTCTrajectoryFile import to_mdtraj_XTCTrajectoryFile
    from molsysmt.form.mdtraj_XTCTrajectoryFile.to_mdtraj_Trajectory import to_mdtraj_Trajectory as mdtraj_XTCTrajectoryFile_to_mdtraj_Trajectory
    import molsysmt as msm

    tmp_item = to_mdtraj_XTCTrajectoryFile(item, skip_digestion=True)
    res_item = mdtraj_XTCTrajectoryFile_to_mdtraj_Trajectory(tmp_item, atom_indices=atom_indices,
                structure_indices=structure_indices, skip_digestion=True)

    msm.form.close(tmp_item)

    return res_item

