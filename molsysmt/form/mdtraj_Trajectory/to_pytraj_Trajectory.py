from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.Trajectory')
def to_pytraj_Trajectory(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from mdtraj.Trajectory to pytraj.Trajectory.

    Parameters
    ----------
    item : mdtraj.Trajectory
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    pytraj.Trajectory
        Converted molecular system representation.
    """

    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys.to_pytraj_Trajectory import to_pytraj_Trajectory as molsysmt_MolSys_to_pytraj_Trajectory

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                  skip_digestion=True)
    tmp_item = molsysmt_MolSys_to_pytraj_Trajectory(tmp_item, skip_digestion=True)

    return tmp_item

