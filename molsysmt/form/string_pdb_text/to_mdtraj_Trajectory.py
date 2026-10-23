from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:pdb_text")
@dep_digest("mdtraj")
def to_mdtraj_Trajectory(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
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


    Notes
    -----
    MDTraj parses a temporary PDB file written by the existing text adapter.
    The adapter owns that scratch directory and removes it on return, reader
    failure or interruption. The input text is not modified.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from pathlib import Path
    >>> source = msm.systems["T4 lysozyme L99A"]["181l.pdb"]
    >>> trajectory = to_mdtraj_Trajectory(Path(source).read_text(), atom_indices=[0, 2])
    >>> trajectory.n_atoms
    2

    .. versionadded:: 1.0.0
    """

    from tempfile import TemporaryDirectory

    from ..file_pdb.to_mdtraj_Trajectory import (
        to_mdtraj_Trajectory as file_pdb_to_mdtraj_Trajectory,
    )
    from .to_file_pdb import to_file_pdb

    with TemporaryDirectory() as directory:
        filename = to_file_pdb(
            item, output_filename=f"{directory}/input.pdb", skip_digestion=True
        )
        return file_pdb_to_mdtraj_Trajectory(
            filename,
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            skip_digestion=True,
        )
