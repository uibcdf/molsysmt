"""Checking canonical chemical atom types."""

import numpy as np

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.atom_types import CHEMICAL_ATOM_TYPES


@arg_digest()
def is_atom_type(atom_type, skip_digestion=False):
    """Checking whether strings are canonical chemical element atom types.

    Parameters
    ----------
    atom_type : str, list of str, tuple of str or numpy.ndarray
        Chemical element symbol or one-dimensional collection of symbols.
        Capitalization is significant: ``'Ca'`` is calcium; ``'CA'`` is not.
    skip_digestion : bool, default=False
        Whether to skip argument digestion. Default is False.

    Returns
    -------
    bool or numpy.ndarray
        A boolean for a scalar string, or a one-dimensional boolean array in
        input order. An empty collection returns an array of shape ``(0,)``.

    Raises
    ------
    ArgumentError
        If input is not a string or a one-dimensional collection of strings.

    Notes
    -----
    Checks the 118 chemical element symbols. Atom names, force-field types,
    dummy particles (``Du``, ``X``), unknown markers and isotope aliases
    (``D``, ``T``) are not canonical chemical atom types. Use
    :func:`normalize_atom_types` for the two hydrogen isotope aliases.

    See Also
    --------
    normalize_atom_types : Normalize explicit isotope aliases.
    get_atom_type_from_atom_name : Infer elements from standard atom names.

    Examples
    --------
    >>> import molsysmt as msm
    >>> msm.element.atom.is_atom_type('Ca')
    True
    >>> msm.element.atom.is_atom_type(['C', 'CA', 'OA', 'D']).tolist()
    [True, False, False, False]

    .. admonition:: Tutorial with more examples

       See :ref:`Tutorial_Atom_Types` for element and isotope conventions.

    .. versionadded:: 1.0.0
    """

    if isinstance(atom_type, str):
        return atom_type in CHEMICAL_ATOM_TYPES
    return np.asarray([value in CHEMICAL_ATOM_TYPES for value in atom_type], dtype=bool)
