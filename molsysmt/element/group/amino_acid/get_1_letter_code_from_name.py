from .group_types import name_to_type

aa3_to_aa1 = {
        'ALA': 'A', # Alanine
        'ARG': 'R', # Arginine
        'ASN': 'N', # Asparagine
        'ASP': 'D', # Aspartic Acid
        'CYS': 'C', # Cysteine
        'GLU': 'E', # Glutamic Acid
        'GLN': 'Q', # Glutamine
        'GLY': 'G', # Glycine
        'HIS': 'H', # Histidine
        'ILE': 'I', # Isoleucine
        'LEU': 'L', # Leucine
        'LYS': 'K', # Lysine
        'MET': 'M', # Methionine
        'PHE': 'F', # Phenylalanine
        'PRO': 'P', # Proline
        'PYL': 'O', # Pyrrolysine
        'SER': 'S', # Serine
        'SEC': 'U', # Selenocysteine
        'THR': 'T', # Threonine
        'TRP': 'W', # Tryptophan
        'TYR': 'Y', # Tyrosine
        'VAL': 'V', # Valine
        'ASX': 'B', # Aspartic acid or Asparagine
        'GLX': 'Z', # Glutamic acid or Glutamine
        'XAA': 'X', # Any amino acid
        'XLE': 'J', # Leucine or Isoleucine
        }

def get_1_letter_code_from_name(name):
    """
    Return the one-letter IUPAC code for an amino acid given its three-letter or variant name.

    The function first maps the input name to a canonical three-letter code via
    ``name_to_type``, then converts that code to the standard single-letter
    representation using the IUPAC amino-acid alphabet.

    Parameters
    ----------
    name : str
        Residue name as stored in the topology (e.g. ``'ALA'``, ``'HID'``,
        ``'NALA'``). Variant names (protonation states, N/C-terminal prefixes)
        are resolved to their canonical type before the lookup.

    Returns
    -------
    str
        Single IUPAC letter code for the amino acid (e.g. ``'A'`` for alanine,
        ``'R'`` for arginine). Ambiguity codes (``'B'``, ``'Z'``, ``'X'``,
        ``'J'``) are returned for the corresponding degenerate residue types.

    Raises
    ------
    KeyError
        Raised if ``name`` is not present in the ``name_to_type`` mapping or if
        the resolved canonical name is not present in the ``aa3_to_aa1`` table.

    Notes
    -----
    The complete mapping from three-letter codes to one-letter codes follows the
    IUPAC-IUB nomenclature and includes the 20 standard amino acids as well as
    selenocysteine (``'SEC'`` → ``'U'``), pyrrolysine (``'PYL'`` → ``'O'``), and
    the standard ambiguity codes.

    .. versionadded:: 1.0.0
    """

    aa_type = name_to_type[name]

    return aa3_to_aa1[aa_type]

