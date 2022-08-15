from ...exceptions import ArgumentError
from ...variables import is_all

def digest_inner_bonded_atoms(inner_bonded_atoms, caller=None):
    """Checks if `inner_bonded_atoms` has the expected type and value.

    Parameters
    ----------
    inner_bonded_atoms : Any
        The `inner_bonded_atoms` argument for digestion.
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
        If the given `inner_bonded_atoms` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get.get':
        if isinstance(inner_bonded_atoms, bool):
            return inner_bonded_atoms

    raise ArgumentError('inner_bonded_atoms', value=inner_bonded_atoms, caller=caller, message=None)

