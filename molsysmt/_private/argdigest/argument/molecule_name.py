from molsysmt._private.smonitor import ArgumentError
from ...variables import is_all
from numpy import ndarray
from argdigest.core.caller import caller_matches, caller_startswith

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        )

def digest_molecule_name(molecule_name, caller=None):
    """Checks if `molecule_name` has the expected type and value.

    Parameters
    ----------
    molecule_name : Any
        The `molecule_name` argument for digestion.
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
        If the given `molecule_name` has not of the correct type or value.
    """

    if molecule_name is None and caller_matches(caller, 'add_molecule'):
        return None

    if caller is not None:

        if caller.endswith(functions_with_boolean):
            if isinstance(molecule_name, bool):
                return molecule_name
        elif caller_startswith(caller, 'molsysmt.form.') and caller.count('.to_')==2:
            return molecule_name

    if isinstance(molecule_name, str):
        return molecule_name

    elif isinstance(molecule_name, list):
        return molecule_name

    elif isinstance(molecule_name, tuple):
        return list(molecule_name)

    if isinstance(molecule_name, ndarray):
        return molecule_name.tolist()

    raise ArgumentError('molecule_name', value=molecule_name, caller=caller, message=None)
