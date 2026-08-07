from molsysmt._private.smonitor import ArgumentError
from ...variables import is_all
from numpy import ndarray
from argdigest.core.caller import caller_matches, caller_startswith

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        )

def digest_atom_type(atom_type, caller=None):
    """Checks if `atom_type` has the expected type and value.

    Parameters
    ----------
    atom_type : Any
        The `atom_type` argument for digestion.
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
        If the given `atom_type` has not of the correct type or value.
    """

    if atom_type is None and caller_matches(caller, 'add_atom'):
        return None

    if caller is not None:

        if caller.endswith(functions_with_boolean):
            if isinstance(atom_type, bool):
                return atom_type
        elif caller_startswith(caller, 'molsysmt.form.') and caller.count('.to_')==2:
            return atom_type

    if isinstance(atom_type, str):
        return atom_type

    elif isinstance(atom_type, list):
        return atom_type

    elif isinstance(atom_type, tuple):
        return list(atom_type)

    elif isinstance(atom_type, ndarray):
        return atom_type.tolist()

    raise ArgumentError('atom_type', value=atom_type, caller=caller, message=None)

