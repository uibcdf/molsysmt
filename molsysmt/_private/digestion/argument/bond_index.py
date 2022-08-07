from ...exceptions import ArgumentError
from ...variables import is_all

def digest_bond_index(bond_index, caller=None):
    """Checks if `bond_index` has the expected type and value.

    Parameters
    ----------
    bond_index : Any
        The `bond_index` argument for digestion.
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
        If the given `bond_index` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get.get':
        if isinstance(bond_index, bool):
            return bond_index

    raise ArgumentError('bond_index', value=bond_index, caller=caller, message=None)

