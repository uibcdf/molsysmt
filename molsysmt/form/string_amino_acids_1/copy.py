from copy import copy as shallow_copy

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:amino_acids_1")
def copy(item, skip_digestion=False):
    """
    Copying a one-letter amino-acid sequence.

    Parameters
    ----------
    item : str
        One-letter sequence, optionally prefixed with ``amino_acids_1:``.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    str
        The unchanged sequence value. Immutable strings may retain their identity.

    Examples
    --------
    >>> from molsysmt.form.string_amino_acids_1.copy import copy
    >>> copy('ACD')
    'ACD'

    .. versionadded:: 1.0.0
    """
    return shallow_copy(item)
