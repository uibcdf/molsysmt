from ...exceptions import ArgumentError
from ...variables import is_all
from numpy import ndarray

def digest_chain_name(chain_name, caller=None):
    """Checks if `chain_name` has the expected type and value.

    Parameters
    ----------
    chain_name : Any
        The `chain_name` argument for digestion.
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
        If the given `chain_name` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get.get':
        if isinstance(chain_name, bool):
            return chain_name
    elif caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        return chain_name
    elif '.set.set' in caller:
        if isinstance(chain_name, (int, str, list, tuple, ndarray)):
            return chain_name
    elif caller.endswith('.define_new_chain'):
        if chain_name is None:
            return chain_name
        if isinstance(chain_name, (int, str, list, tuple, ndarray)):
            return chain_name
    elif isinstance(chain_name, str):
        return chain_name

    raise ArgumentError('chain_name', value=chain_name, caller=caller, message=None)

