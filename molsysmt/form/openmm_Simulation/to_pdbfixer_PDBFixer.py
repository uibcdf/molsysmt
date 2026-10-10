from molsysmt._private.argdigest import arg_digest


@arg_digest(form="openmm.Simulation")
def to_pdbfixer_PDBFixer(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """
    Converting from openmm.Simulation to pdbfixer.PDBFixer.


    Parameters
    ----------
    item : molecular system
        OpenMM Simulation supplying topology and current coordinates.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    pdbfixer.PDBFixer
        In-memory fixer containing the selected system.

    Raises
    ------
    OSError
        If an intermediate file cannot be written, read or retired.

    Notes
    -----
    The bridge owns an intermediate PDB in a managed directory through eager
    PDBFixer construction. Success and conversion failures retire that scratch;
    the returned in-memory object does not depend on its continued existence.
    Cleanup errors remain visible. Separately requested file outputs retain
    their caller ownership.


    .. versionadded:: 1.0.0
    """

    from pathlib import Path
    from tempfile import TemporaryDirectory

    from molsysmt.form.file_pdb.to_pdbfixer_PDBFixer import (
        to_pdbfixer_PDBFixer as file_pdb_to_pdbfixer_PDBFixer,
    )

    from .to_file_pdb import to_file_pdb as openmm_Simulation_to_file_pdb

    with TemporaryDirectory(prefix="molsysmt-simulation-pdbfixer-") as directory:
        tmp_file = str(Path(directory) / "input.pdb")
        openmm_Simulation_to_file_pdb(
            item,
            output_filename=tmp_file,
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            skip_digestion=True,
        )
        tmp_item = file_pdb_to_pdbfixer_PDBFixer(tmp_file, skip_digestion=True)

    return tmp_item
