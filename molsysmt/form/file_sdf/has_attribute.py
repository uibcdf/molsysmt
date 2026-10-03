from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:sdf")
def has_attribute(
    molecular_system, attribute, include_none=False, skip_digestion=False
):
    """Checking whether an explicit SDF attribute is available.

    Parameters
    ----------
    molecular_system : str or pathlib.Path
        Single-record SDF file to inspect.
    attribute : str
        MolSysMT attribute name to query.
    include_none : bool, default=False
        Whether declared capability is sufficient, regardless of stored values.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    bool
        Whether the adapter supports the attribute and, when requested, has values.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.ctfile import read_sdf
    from molsysmt.form.molsysmt_MolSys.has_attribute import has_attribute as native_has

    from ._native import to_native
    from .attributes import attributes

    if not attributes.get(attribute, False):
        return False
    if include_none:
        return True
    item = to_native(
        read_sdf(molecular_system, allow_stereo=True), discard_properties=True
    )
    return native_has(
        item, attribute=attribute, include_none=False, skip_digestion=True
    )
