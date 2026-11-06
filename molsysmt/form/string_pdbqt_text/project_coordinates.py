"""Project coordinates onto explicit prepared text through the shared handler."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.argdigest.pdbqt_projection import DIGEST_OPTIONS


@signal(tags=["api", "form"])
@arg_digest(form="string:pdbqt_text", **DIGEST_OPTIONS)
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
    """Projecting mapped lengths onto an explicit prepared PDBQT text snapshot.

    Parameters
    ----------
    item : str
        Prepared text with the explicit pdbqt_text: prefix.
    coordinates : quantity
        Explicit lengths, shape (n_selected_structures, n_prepared_atoms, 3).
        A single structure may use shape (n_prepared_atoms, 3).
    atom_correspondence : array_like of int
        Exhaustive unique (coordinate_atom_index, source_pdbqt_atom_index) pairs.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Unique, nonempty source indices in output order, aligned with coordinates.
    output_filename : str or pathlib.Path, default=None
        Detached text by default; an explicit path requests atomic file output.
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
        molecular_system and typed report with payload hashes, explicit maps,
        source labels, angstrom precision and metadata/producer provenance.

    Notes
    -----
    Uses the experimental PDBQTFileHandler.project_coordinates contract and
    preserves all non-coordinate atom fields and tree meaning. Resident source
    text, coordinate input, one-model work buffers and any full text output have
    separate memory costs. This does not reconstruct a complete chemical graph.

    See Also
    --------
    molsysmt.native.PDBQTFileHandler.project_coordinates : Full projection contract.

    Examples
    --------
    >>> from molsysmt import pyunitwizard as puw
    >>> source = 'pdbqt_text:ATOM      1   C1 LIG A   1       1.000   2.000   3.000  1.00  0.00     0.125 C\\nEND\\n'
    >>> result = project_coordinates(source, puw.quantity([[4, 5, 6]], 'angstrom'), [[0, 0]])
    >>> result['report']['output_to_source_atom_indices']
    [0]

    .. admonition:: User guide

       See :ref:`Tutorial_Project_Prepared_PDBQT`.

    .. versionadded:: 1.0.0
    """
    from molsysmt.native import PDBQTFileHandler

    with PDBQTFileHandler(item) as handler:
        return handler.project_coordinates(
            coordinates,
            atom_correspondence,
            structure_indices=structure_indices,
            output_filename=output_filename,
            discard_remarks=discard_remarks,
            chemical_state_provenance=chemical_state_provenance,
            skip_digestion=True,
        )
