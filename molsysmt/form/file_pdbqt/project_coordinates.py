"""Project coordinates onto a prepared file without reconstructing chemistry."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.argdigest.pdbqt_projection import DIGEST_OPTIONS


@signal(tags=["api", "form"])
@arg_digest(form="file:pdbqt", **DIGEST_OPTIONS)
def project_coordinates(
    item,
    coordinates,
    atom_correspondence,
    structure_indices="all",
    output_filename=None,
    discard_remarks=False,
    chemical_state_provenance=None,
    skip_digestion=False,
):
    """Projecting explicit coordinates onto an indexed prepared PDBQT file.

    Parameters
    ----------
    item : str or pathlib.Path
        Prepared UTF-8 PDBQT file. All source models are validated on opening.
    coordinates : quantity
        Explicit lengths, shape (n_selected_structures, n_prepared_atoms, 3).
        A single structure may use shape (n_prepared_atoms, 3).
    atom_correspondence : array_like of int
        Exhaustive unique (coordinate_atom_index, source_pdbqt_atom_index) pairs.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Unique, nonempty source indices in output order, aligned with coordinates.
    output_filename : str or pathlib.Path, default=None
        Detached text by default; an independent path requests atomic file output.
    discard_remarks : bool, default=False
        Explicitly allow removing all remarks, including stale scores. Otherwise
        any source REMARK causes refusal, including outside selected models.
    chemical_state_provenance : dict, default=None
        Optional detached JSON-compatible caller declaration.
    skip_digestion : bool, default=False
        Whether to skip argument digestion.

    Returns
    -------
    dict
        molecular_system and typed report, with actual payload hashes, axis maps,
        source labels, angstrom precision and metadata/producer provenance.

    Notes
    -----
    The experimental contract, rounding, errors and buffer limits are those of
    PDBQTFileHandler.project_coordinates. Only coordinate columns are replaced;
    source charge precision, types and torsion-tree records are preserved.
    File output streams one model through the existing atomic document writer.
    This does not score, reprepare or certify chemistry.

    See Also
    --------
    molsysmt.native.PDBQTFileHandler.project_coordinates : Full projection contract.

    Examples
    --------
    >>> from pathlib import Path
    >>> from tempfile import TemporaryDirectory
    >>> from molsysmt import pyunitwizard as puw
    >>> body = 'ATOM      1   C1 LIG A   1       1.000   2.000   3.000  1.00  0.00     0.125 C\\nEND\\n'
    >>> with TemporaryDirectory() as directory:
    ...     source = Path(directory) / 'prepared.pdbqt'
    ...     _ = source.write_bytes(body.encode('utf-8'))
    ...     result = project_coordinates(source, puw.quantity([[4, 5, 6]], 'angstrom'), [[0, 0]])
    >>> result['report']['output_to_source_atom_indices']
    [0]

    .. admonition:: User guide

       See :ref:`Tutorial_Project_Prepared_PDBQT`.

    .. versionadded:: 1.0.0
    """
    from molsysmt.native import PDBQTFileHandler

    with PDBQTFileHandler(item, storage_mode="indexed") as handler:
        return handler.project_coordinates(
            coordinates,
            atom_correspondence,
            structure_indices=structure_indices,
            output_filename=output_filename,
            discard_remarks=discard_remarks,
            chemical_state_provenance=chemical_state_provenance,
            skip_digestion=True,
        )
