from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_id')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from string:alphafold_id to mdtraj.Trajectory.

    Parameters
    ----------
    item : string:alphafold_id
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.Trajectory
        Converted molecular system representation.
    """

    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys.to_mdtraj_Trajectory import to_mdtraj_Trajectory as molsysmt_MolSys_to_mdtraj_Trajectory

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices,
            structure_indices=structure_indices, skip_digestion=True)
    tmp_item = molsysmt_MolSys_to_mdtraj_Trajectory(tmp_item, skip_digestion=True)

    return tmp_item

