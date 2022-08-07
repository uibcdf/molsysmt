from ...exceptions import ArgumentError
from ...variables import is_all

def digest_chain_type(chain_type, caller=None):
    """Checks if `chain_type` has the expected type and value.

    Parameters
    ----------
    chain_type : Any
        The `chain_type` argument for digestion.
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
        If the given `chain_type` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get.get':
        if isinstance(chain_type, bool):
            return chain_type

    raise ArgumentError('chain_type', value=chain_type, caller=caller, message=None)

