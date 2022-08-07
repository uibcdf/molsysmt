from ...exceptions import ArgumentError
from ...variables import is_all

def digest_inner_bond_index(inner_bond_index, caller=None):
    """Checks if `inner_bond_index` has the expected type and value.

    Parameters
    ----------
    inner_bond_index : Any
        The `inner_bond_index` argument for digestion.
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
        If the given `inner_bond_index` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get.get':
        if isinstance(inner_bond_index, bool):
            return inner_bond_index

    raise ArgumentError('inner_bond_index', value=inner_bond_index, caller=caller, message=None)

