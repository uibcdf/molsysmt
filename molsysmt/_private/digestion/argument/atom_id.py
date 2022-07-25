from ...exceptions import ArgumentError
from ...variables import is_all

def digest_atom_id(atom_id, caller=None):
    """Checks if `atom_id` has the expected type and value.

    Parameters
    ----------
    atom_id : Any
        The `atom_id` argument for digestion.
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
        If the given `atom_id` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(atom_id, bool):
            return atom_id

    raise ArgumentError('atom_id', caller=caller, message=None)

