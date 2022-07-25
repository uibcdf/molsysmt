from ...exceptions import ArgumentError
from ...variables import is_all

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
        Either True or False when caller is `molsysmt.basic.get`.

    Raises
    -------
    ArgumentError
        If the given `molecule_name` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(molecule_name, bool):
            return molecule_name

    raise ArgumentError('molecule_name', caller=caller, message=None)

