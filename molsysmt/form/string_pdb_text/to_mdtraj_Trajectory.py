from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_text')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from string:pdb_text to mdtraj.Trajectory.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.Trajectory
        Resulting object in mdtraj.Trajectory form.


    .. versionadded:: 1.0.0
    """

    from .to_file_pdb import to_file_pdb    
    from ..file_pdb.to_mdtraj_Trajectory import to_mdtraj_Trajectory as file_pdb_to_mdtraj_Trajectory  

    tmp_item = to_file_pdb(item, skip_digestion=True)
    tmp_item = file_pdb_to_mdtraj_Trajectory(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
                                             skip_digestion=True)

    return tmp_item

