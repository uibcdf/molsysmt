from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:h5')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from .to_mdtraj_HDF5TrajectoryFile import to_mdtraj_HDF5TrajectoryFile
    from molsysmt.form.mdtraj_HDF5TrajectoryFile.to_molsysmt_Structures import to_molsysmt_Structures as mdtraj_HDF5TrajectoryFile_to_molsysmt_Structures
    import molsysmt as msm

    tmp_item = to_mdtraj_HDF5TrajectoryFile(item, skip_digestion=True)
    try:
        res_item = mdtraj_HDF5TrajectoryFile_to_molsysmt_Structures(
            tmp_item,
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            skip_digestion=True,
        )
    finally:
        msm.form.close(tmp_item)

    return res_item
