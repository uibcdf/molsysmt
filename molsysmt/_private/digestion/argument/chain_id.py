from ...exceptions import ArgumentError
from ...variables import is_all

def digest_chain_id(chain_id, caller=None):
    """Checks if `chain_id` has the expected type and value.

    Parameters
    ----------
    chain_id : Any
        The `chain_id` argument for digestion.
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
        If the given `chain_id` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get.get':
        if isinstance(chain_id, bool):
            return chain_id
    elif caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        return chain_id

    raise ArgumentError('chain_id', caller=caller, message=None)

