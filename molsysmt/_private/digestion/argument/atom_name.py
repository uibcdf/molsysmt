from ...exceptions import ArgumentError
from ...variables import is_all

def digest_atom_name(atom_name, caller=None):
    """Checks if `atom_name` has the expected type and value.

    Parameters
    ----------
    atom_name : Any
        The `atom_name` argument for digestion.
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
        If the given `atom_name` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(atom_name, bool):
            return atom_name

    raise ArgumentError('atom_name', caller=caller, message=None)

