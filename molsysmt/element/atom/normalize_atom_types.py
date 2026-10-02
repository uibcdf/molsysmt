"""Normalizing explicit chemical atom types and isotope aliases."""

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.atom_types import normalize_atom_type
from molsysmt._private.smonitor import ArgumentError


@arg_digest()
def normalize_atom_types(atom_type, isotope=None, skip_digestion=False):
    """Normalizing chemical atom types and nullable isotope mass numbers.

    Parameters
    ----------
    atom_type : str, list of str, tuple of str or numpy.ndarray
        Chemical element symbol or one-dimensional collection of symbols.
        The aliases ``D`` and ``T`` denote hydrogen with mass numbers 2 and 3.
    isotope : int, list, tuple or numpy.ndarray, default=None
        Explicit mass number in [1, 65535], or None for unspecified. Default
        is None. Collections must align with atom_type; scalar mass numbers
        are not broadcast. Missing entries may be None or pandas.NA.
    skip_digestion : bool, default=False
        Whether to skip argument digestion. Default is False.

    Returns
    -------
    tuple
        ``(atom_type, isotope)``: a string and int or None for scalar input,
        or two new lists of equal length for collection input. An empty
        collection returns ``([], [])``. No input is modified.

    Raises
    ------
    ArgumentError
        If symbols are unsupported, shapes do not align, mass numbers are
        invalid, or an explicit isotope conflicts with D or T.

    Notes
    -----
    In MolSysMT, atom_type denotes the chemical element, independently of
    atom_name and atom_ff_type. This function performs no chemical perception,
    capitalization repair, mass calculation or isotope-stability validation.
    Unspecified isotopes remain unspecified; no reference isotope is inferred.

    See Also
    --------
    is_atom_type : Check canonical chemical element symbols.
    get_atom_type_from_atom_name : Infer elements from standard atom names.

    Examples
    --------
    >>> import molsysmt as msm
    >>> msm.element.atom.normalize_atom_types('D')
    ('H', 2)
    >>> msm.element.atom.normalize_atom_types(['C', 'D', 'T'], isotope=[13, None, 3])
    (['C', 'H', 'H'], [13, 2, 3])

    .. admonition:: Tutorial with more examples

       See :ref:`Tutorial_Atom_Types` for element and isotope conventions.

    .. versionadded:: 1.0.0
    """

    import numpy as np
    import pandas as pd

    scalar = isinstance(atom_type, str)
    values = [atom_type] if scalar else atom_type
    if isotope is None or isotope is pd.NA:
        isotopes = [None] * len(values)
    elif scalar and isinstance(isotope, (int, np.integer)):
        isotopes = [isotope]
    elif not scalar and isinstance(isotope, (list, tuple, np.ndarray)):
        isotopes = isotope
    else:
        raise ArgumentError(
            "isotope",
            value=isotope,
            caller=__name__,
            message="Isotope and atom_type must have matching scalar or collection shapes.",
        )
    if len(isotopes) != len(values):
        raise ArgumentError(
            "isotope",
            value=isotope,
            caller=__name__,
            message="Isotope and atom_type collections must have equal lengths.",
        )
    normalized_types, normalized_isotopes = [], []
    for value, mass_number in zip(values, isotopes):
        try:
            value, mass_number = normalize_atom_type(
                value, None if mass_number is pd.NA else mass_number
            )
        except ValueError as error:
            raise ArgumentError(
                "atom_type", value=atom_type, caller=__name__, message=str(error)
            ) from error
        normalized_types.append(value)
        normalized_isotopes.append(mass_number)
    if scalar:
        return normalized_types[0], normalized_isotopes[0]
    return normalized_types, normalized_isotopes
