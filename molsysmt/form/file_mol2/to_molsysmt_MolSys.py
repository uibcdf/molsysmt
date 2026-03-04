from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:mol2')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import MolSys
    from molsysmt.form.file_mol2.to_mdtraj_Trajectory import to_mdtraj_Trajectory as file_mol2_to_mdtraj_Trajectory
    from molsysmt.form.mdtraj_Trajectory.to_molsysmt_MolSys import to_molsysmt_MolSys as mdtraj_Trajectory_to_molsysmt_MolSys

    # Step 1: Open the file into an MDTraj object using the local converter
    tmp_item = file_mol2_to_mdtraj_Trajectory(item, skip_digestion=True)
    
    # Step 2: Convert the MDTraj object to MolSys
    tmp_item = mdtraj_Trajectory_to_molsysmt_MolSys(tmp_item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices, skip_digestion=True)

    return tmp_item
