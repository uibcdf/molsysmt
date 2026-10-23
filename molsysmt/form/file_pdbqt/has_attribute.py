from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:pdbqt")
def has_attribute(
    molecular_system, attribute, include_none=False, skip_digestion=False
):
    """Checking explicit PDBQT attribute availability.

    Parameters
    ----------
    molecular_system : molecular system
        Supported PDBQT source to inspect.
    attribute : str
        MolSysMT attribute name.
    include_none : bool, default=False
        Whether declared capability alone suffices. Default is False.
    skip_digestion : bool, default=False
        Whether to skip argument digestion. Default is False.

    Returns
    -------
    bool
        Whether the attribute is supported and, when requested, present.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_PDBQTFileHandler.has_attribute import (
        has_attribute as handler_has,
    )
    from molsysmt.native import PDBQTFileHandler

    from .attributes import attributes

    if not attributes.get(attribute, False):
        return False
    if include_none:
        return True
    with PDBQTFileHandler(molecular_system) as handler:
        return handler_has(handler, attribute, skip_digestion=True)
