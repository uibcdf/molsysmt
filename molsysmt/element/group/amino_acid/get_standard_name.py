from .group_types import name_to_type


def get_standard_name(group_name):
    """
    Return the canonical standard amino-acid name for a non-standard residue.

    Uses the comprehensive ``name_to_type`` mapping (derived from MDTraj, ~817
    entries) which covers modified amino acids, D-amino acids, protonation-state
    variants, and other non-canonical residues found in the PDB.

    Parameters
    ----------
    group_name : str
        Residue name as stored in the topology (e.g. ``'MSE'``, ``'SEP'``,
        ``'HID'``).

    Returns
    -------
    str or None
        The standard 3-letter amino-acid code for the nearest standard residue
        (e.g. ``'MET'``, ``'SER'``, ``'HIS'``).
        Returns ``None`` when:

        * ``group_name`` is already a standard amino acid (e.g. ``'ALA'``).
        * ``group_name`` is not in the amino-acid database at all (e.g. water,
          ions, ligands).
        * The residue has no known standard equivalent (maps to ``'XAA'``).

    Examples
    --------
    >>> get_standard_name('MSE')   # selenomethionine
    'MET'
    >>> get_standard_name('SEP')   # phosphoserine
    'SER'
    >>> get_standard_name('ALA')   # already standard
    None
    >>> get_standard_name('HOH')   # water — not an amino acid
    None

    Notes
    -----
    The source table is ``element.group.amino_acid.group_types.name_to_type``.

    .. versionadded:: 1.0.0
    """

    standard = name_to_type.get(group_name)
    if standard is None or standard == 'XAA' or standard == group_name:
        return None
    return standard
