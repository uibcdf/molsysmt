from ...exceptions import ArgumentError
from ...variables import is_all
import numpy as np

def digest_molecule_type(molecule_type, caller=None):
    """Checks if `molecule_type` has the expected type and value.

    Parameters
    ----------
    molecule_type : Any
        The `molecule_type` argument for digestion.
    caller: str, optional
        Name of the function or method that is being digested.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/#the-any-type

    Returns
    -------
    bool
        Either True or False when caller is `get`.

    Raises
    -------
    ArgumentError
        If the given `molecule_type` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get.get':
        if isinstance(molecule_type, bool):
            return molecule_type
    elif caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        return molecule_type

    if isinstance(molecule_type, str):
        return molecule_type

    elif isinstance(molecule_type, list):
        return molecule_type

    elif isinstance(molecule_type, tuple):
        return list(molecule_type)

    elif isinstance(molecule_type, np.ndarray):
        return molecule_type.tolist()

    raise ArgumentError('molecule_type', value=molecule_type, caller=caller, message=None)

