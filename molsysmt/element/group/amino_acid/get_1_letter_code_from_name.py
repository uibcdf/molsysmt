from .codes import aa3_to_aa1
from .group_types import name_to_type


def get_1_letter_code_from_name(name):
    """
    Return the one-letter IUPAC code for an amino acid given its three-letter or variant name.

    The function first maps the input name to a canonical three-letter code via
    ``name_to_type``, then converts that code to the standard single-letter
    representation using the IUPAC amino-acid alphabet.


    Parameters
    ----------
    name : object
        Argument name.

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
