def get_bonded_atom_pairs(group, skip_digestion=False):
    """
    Getting standard intra-group covalent bonded atom pairs for a group.

    Parameters
    ----------
    group : str
        Residue or group name (e.g. 'ALA', 'HOH', 'POPC').
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    list of tuple of str
        List of standard bonded atom name pairs.

    .. versionadded:: 1.0.0
    """
    from molsysmt.element.group.get_group_type_from_group_name import get_group_type_from_group_name
    from molsysmt._private.smonitor import NotImplementedMethodError
    import importlib

    group_type = get_group_type_from_group_name(group)
    if group_type is not None:
        mod = importlib.import_module(f"molsysmt.element.group.{group_type}.get_bonded_atom_pairs")
        return mod.get_bonded_atom_pairs(group)
    else:
        raise NotImplementedMethodError
