from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:xtc')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from .to_mdtraj_XTCTrajectoryFile import to_mdtraj_XTCTrajectoryFile
    from molsysmt.form.mdtraj_XTCTrajectoryFile.to_molsysmt_Structures import to_molsysmt_Structures as mdtraj_XTCTrajectoryFile_to_molsysmt_Structures
    import molsysmt as msm

    tmp_item = to_mdtraj_XTCTrajectoryFile(item, skip_digestion=True)
    res_item = mdtraj_XTCTrajectoryFile_to_molsysmt_Structures(tmp_item, atom_indices=atom_indices,
                                                               structure_indices=structure_indices,
                                                               skip_digestion=True)

    msm.form.close(tmp_item)

    return res_item

