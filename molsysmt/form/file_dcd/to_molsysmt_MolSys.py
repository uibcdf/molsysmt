from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:dcd')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from .to_mdtraj_DCDTrajectoryFile import to_mdtraj_DCDTrajectoryFile
    from molsysmt.form.mdtraj_DCDTrajectoryFile.to_molsysmt_MolSys import to_molsysmt_MolSys as mdtraj_DCDTrajectoryFile_to_molsysmt_MolSys
    import molsysmt as msm

    from molsysmt._private.backend_output import silence_backend_stdout

    # MDTraj's DCD reader prints the detected format on stdout, on open and on read.
    with silence_backend_stdout():
        tmp_item = to_mdtraj_DCDTrajectoryFile(item, skip_digestion=True)
        try:
            res_item = mdtraj_DCDTrajectoryFile_to_molsysmt_MolSys(
                tmp_item,
                atom_indices=atom_indices,
                structure_indices=structure_indices,
                skip_digestion=True,
            )
        finally:
            msm.form.close(tmp_item)

    return res_item
