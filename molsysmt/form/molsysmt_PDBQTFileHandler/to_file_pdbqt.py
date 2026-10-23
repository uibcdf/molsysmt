from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.PDBQTFileHandler")
def to_file_pdbqt(
    item,
    atom_indices="all",
    structure_indices="all",
    output_filename=None,
    skip_digestion=False,
):
    """Exporting a validated PDBQT document while preserving declared records.

    Parameters
    ----------
    item : molecular system
        Open PDBQT handler with resident snapshot or source-bound indexed storage.
    atom_indices : int, list, tuple or numpy.ndarray, default='all'
        Source atom positions to retain. Native graph extraction uses the native
        canonical subset order.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Source structure positions, independent of MODEL labels. Query/iteration order
        and repetitions are preserved; serialized documents require unique positions.
    output_filename : str or pathlib.Path, default=None
        Destination for validated PDBQT text. The original source snapshot is unchanged.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated inputs.

    Returns
    -------
    str or pathlib.Path
        Destination containing the validated selected document.

    Notes
    -----
    Document conversions preserve only declared PDBQT evidence. Native graph projections omit the format-specific torsion tree only under the stated authorization; they do not infer complete chemistry. Closed handlers reject data queries.

    .. versionadded:: 1.0.0
    """
    return item._write_file(output_filename, atom_indices, structure_indices)
