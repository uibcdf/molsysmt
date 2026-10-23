from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.PDBQTFileHandler")
def has_attribute(
    molecular_system, attribute, include_none=False, skip_digestion=False
):
    """Checking declared and instance-present PDBQT document attributes.

    Parameters
    ----------
    molecular_system : molecular system
        PDBQT input in this adapter's registered form; parsing validates homogeneous model identity.
    attribute : str
        MolSysMT attribute name whose declared support or actual instance presence is queried.
    include_none : bool, default=False
        Return declared capability when True, including attributes absent from this document instance.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated inputs.

    Returns
    -------
    bool
        Whether the declared attribute is supported and, when requested, present.

    Notes
    -----
    Document conversions preserve only declared PDBQT evidence. Native graph projections omit the format-specific torsion tree only under the stated authorization; they do not infer complete chemistry. Closed handlers reject data queries.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_MolSys.has_attribute import has_attribute as native_has

    from .attributes import attributes

    if not attributes.get(attribute, False):
        return False
    if include_none:
        return True
    molecular_system._require_open()
    if attribute in {"n_structures", "coordinates", "structure_index"}:
        return True
    if attribute == "structure_id":
        return any(v is not None for v in molecular_system._document.labels)
    if attribute in {"occupancy", "b_factor"}:
        return attribute in molecular_system._document.present
    return native_has(molecular_system._native(), attribute, skip_digestion=True)
