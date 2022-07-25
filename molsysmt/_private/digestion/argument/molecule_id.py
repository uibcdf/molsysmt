from ...exceptions import ArgumentError
from ...variables import is_all

def digest_molecule_id(molecule_id, caller=None):
    """Checks if `molecule_id` has the expected type and value.

    Parameters
    ----------
    molecule_id : Any
        The `molecule_id` argument for digestion.
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
        If the given `molecule_id` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(molecule_id, bool):
            return molecule_id

    raise ArgumentError('molecule_id', caller=caller, message=None)

