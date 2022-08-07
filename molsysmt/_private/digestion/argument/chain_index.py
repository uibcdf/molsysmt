from ...exceptions import ArgumentError
from ...variables import is_all

def digest_chain_index(chain_index, caller=None):
    """Checks if `chain_index` has the expected type and value.

    Parameters
    ----------
    chain_index : Any
        The `chain_index` argument for digestion.
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
        If the given `chain_index` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get.get':
        if isinstance(chain_index, bool):
            return chain_index

    raise ArgumentError('chain_index', value=chain_index, caller=caller, message=None)

