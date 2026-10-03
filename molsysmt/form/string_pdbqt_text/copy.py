from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:pdbqt_text")
def copy(item, skip_digestion=False):
    """Copying a validated PDBQT source.

    Parameters
    ----------
    item : str
        Explicit pdbqt_text: string containing one supported PDBQT system.
    skip_digestion : bool, default=False
        Whether to skip argument digestion. Default is False.

    Returns
    -------
    str
        Validated copied contents, preserving the original payload.

    .. versionadded:: 1.0.0
    """
    from .to_string_pdbqt_text import to_string_pdbqt_text

    return to_string_pdbqt_text(item)
