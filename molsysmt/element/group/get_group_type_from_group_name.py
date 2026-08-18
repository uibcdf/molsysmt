def get_group_type_from_group_name(group_name, skip_digestion=False):
    """
    Determining the group type classification from a residue or group name.

    Parameters
    ----------
    group_name : str
        Residue or group name string.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    str or None
        Classified group type ('amino_acid', 'ion', 'water', 'lipid', 'nucleotide', 'saccharide', 'small_molecule', 'terminal_capping') or None.

    .. versionadded:: 1.0.0
    """
    from molsysmt.element.group.amino_acid import is_amino_acid
    from molsysmt.element.group.ion import is_ion
    from molsysmt.element.group.water import is_water
    from molsysmt.element.group.terminal_capping import is_terminal_capping
    from molsysmt.element.group.small_molecule import is_small_molecule
    from molsysmt.element.group.nucleotide import is_nucleotide
    from molsysmt.element.group.lipid import is_lipid
    from molsysmt.element.group.saccharide import is_saccharide

    if is_amino_acid(group_name):
        return 'amino_acid'
    elif is_ion(group_name):
        return 'ion'
    elif is_water(group_name):
        return 'water'
    elif is_terminal_capping(group_name):
        return 'terminal_capping'
    elif is_small_molecule(group_name):
        return 'small_molecule'
    elif is_nucleotide(group_name):
        return 'nucleotide'
    elif is_lipid(group_name):
        return 'lipid'
    elif is_saccharide(group_name):
        return 'saccharide'
    else:
        return None
