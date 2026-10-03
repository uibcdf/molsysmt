"""Decoding chemical element symbols from explicitly named typing schemes."""

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.autodock_types import decode_atom_ff_type
from molsysmt._private.smonitor import ArgumentError


@arg_digest()
def get_atom_type_from_atom_ff_type(
    atom_ff_type, typing_scheme="autodock4", skip_digestion=False
):
    """Decoding chemical element symbols from explicit force-field type labels.

    Parameters
    ----------
    atom_ff_type : str, list, tuple or numpy.ndarray
        Label or one-dimensional collection of labels. Matching is case sensitive.
    typing_scheme : str, default='autodock4'
        Named label dictionary. Only standard AutoDock4 labels are supported.
    skip_digestion : bool, default=False
        Whether to skip argument digestion. Default is False.

    Returns
    -------
    str or list of str
        Chemical element symbol, or a new list aligned with the input labels.
        Empty input returns an empty list.

    Raises
    ------
    ArgumentError
        If the scheme, labels, or collection shape are unsupported.

    Notes
    -----
    This decodes existing labels; it does not assign AutoDock types, perceive
    aromaticity, classify hydrogen polarity or determine atomic charges.
    Macrocycle glue labels, water pseudoatoms and custom labels are rejected.
    In MolSysMT, atom_type means the chemical element and atom_ff_type means
    a model-specific label. A type such as A therefore yields C.

    See Also
    --------
    normalize_atom_types : Normalize explicit element symbols and isotope aliases.

    Examples
    --------
    >>> import molsysmt as msm
    >>> msm.element.atom.get_atom_type_from_atom_ff_type(['A', 'NA', 'HD', 'Cl'])
    ['C', 'N', 'H', 'Cl']

    .. admonition:: Tutorial with more examples

       See :ref:`Tutorial_Atom_Types` for chemical and model-specific labels.

    .. versionadded:: 1.0.0
    """
    import numpy as np

    if typing_scheme != "autodock4":
        raise ArgumentError("typing_scheme", value=typing_scheme, caller=__name__)
    scalar = isinstance(atom_ff_type, str)
    values = [atom_ff_type] if scalar else atom_ff_type
    if (
        not isinstance(values, (list, tuple, np.ndarray))
        or np.asarray(values, dtype=object).ndim != 1
    ):
        raise ArgumentError("atom_ff_type", value=atom_ff_type, caller=__name__)
    try:
        result = [decode_atom_ff_type(value, typing_scheme) for value in values]
    except ValueError as error:
        raise ArgumentError(
            "atom_ff_type", value=atom_ff_type, caller=__name__, message=str(error)
        ) from error
    return result[0] if scalar else result
