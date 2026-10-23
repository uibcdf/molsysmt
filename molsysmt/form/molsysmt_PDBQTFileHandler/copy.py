from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.PDBQTFileHandler")
def copy(item, skip_digestion=False):
    """Copying independent handler ownership without duplicating source text.

    Parameters
    ----------
    item : molecular system
        Open PDBQT handler retaining a validated resident document snapshot.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated inputs.

    Returns
    -------
    PDBQTFileHandler
        Independently owned validated document; immutable source text may be shared.

    Notes
    -----
    Document conversions preserve only declared PDBQT evidence. Native graph projections omit the format-specific torsion tree only under the stated authorization; they do not infer complete chemistry. Closed handlers reject data queries.

    .. versionadded:: 1.0.0
    """
    return item.copy()
