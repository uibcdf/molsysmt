from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.PDBQTFileHandler")
def to_string_pdbqt_text(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """Exporting a validated PDBQT document while preserving declared records.

    Parameters
    ----------
    item : molecular system
        Open PDBQT handler retaining a validated resident document snapshot.
    atom_indices : int, list, tuple or numpy.ndarray, default='all'
        Source atom positions to retain. Native graph extraction uses the native
        canonical subset order.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Source structure positions, independent of MODEL labels. Query/iteration order
        and repetitions are preserved; serialized documents require unique positions.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated inputs.

    Returns
    -------
    str
        Validated PDBQT text with the explicit pdbqt_text: prefix.

    Notes
    -----
    Document conversions preserve only declared PDBQT evidence. Native graph projections omit the format-specific torsion tree only under the stated authorization; they do not infer complete chemistry. Closed handlers reject data queries.

    .. versionadded:: 1.0.0
    """
    payload = item._payload(atom_indices, structure_indices)
    return "pdbqt_text:" + payload
