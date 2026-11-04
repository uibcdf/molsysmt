from .codes import aa3_to_aa1
from .group_types import name_to_type


def get_1_letter_code_from_name(name):
    """
    Getting the one-letter code for a canonical or variant amino-acid name.

    Canonical three-letter names, including ambiguity symbols, are resolved
    directly through the shared code table. Other supported names use the
    existing variant-to-canonical mapping before the same conversion.


    Parameters
    ----------
    name : str
        Case-sensitive uppercase canonical or supported variant group name.

    Returns
    -------
    str
        Single-letter code for the amino acid (e.g. ``'A'`` for alanine,
        ``'R'`` for arginine). Ambiguity codes (``'B'``, ``'Z'``, ``'X'``,
        ``'J'``) are returned for the corresponding degenerate residue types.


    Raises
    ------
    KeyError
        Raised if ``name`` is absent from both canonical and variant mappings, or if
        the resolved canonical name is not present in the ``aa3_to_aa1`` table.


    Notes
    -----
    The shared code alphabet [1]_ includes the 20 standard amino acids as well as
    selenocysteine (``'SEC'`` → ``'U'``), pyrrolysine (``'PYL'`` → ``'O'``), and
    the ambiguity codes ``ASX/B``, ``GLX/Z``, ``XAA/X`` and ``XLE/J``.
    ``XLE/J`` expresses leucine/isoleucine ambiguity; it does not select one
    chemical identity or imply that an atomic builder template exists.
    No case normalization, hydrogen addition or chemical conversion is performed.

    References
    ----------
    .. [1] DDBJ, Codes Used in Sequence Description, amino-acid codes.
       https://www.ddbj.nig.ac.jp/ddbj/code-e.html

    Examples
    --------
    >>> get_1_letter_code_from_name('XLE')
    'J'
    >>> get_1_letter_code_from_name('XAA')
    'X'
    >>> get_1_letter_code_from_name('MSE')
    'M'


    .. versionadded:: 1.0.0
    """

    aa_type = name if name in aa3_to_aa1 else name_to_type[name]

    return aa3_to_aa1[aa_type]
