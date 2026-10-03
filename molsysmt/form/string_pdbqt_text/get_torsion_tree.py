from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:pdbqt_text")
def get_torsion_tree(item, skip_digestion=False):
    """Reading a declared PDBQT torsion tree with source atom indices.

    Parameters
    ----------
    item : str
        Explicit pdbqt_text: string containing one supported PDBQT system.
    skip_digestion : bool, default=False
        Whether to skip argument digestion. Default is False.

    Returns
    -------
    dict or None
        Typed arrays of fragment memberships, oriented branch atom/fragment pairs,
        exact source atom_ids and declared TORSDOF. None for a rigid receptor.

    Notes
    -----
    The schema is molsysmt.pdbqt-torsion-tree@1. ROOT is fragment 0.
    Atom indices refer to source file order, independently of atom serial IDs.
    This is format-specific declared evidence, not complete connectivity or
    rotatable-bond perception. TORSDOF need not equal the active branch count.
    Every call returns detached arrays; retain this dictionary separately when
    projecting to native domains. The native writer validates the exact atom
    ID axis and rejects stale mappings after selection or reordering.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.pdbqt import read

    return read(item, text=True)["torsion_tree"]
