from ...exceptions import ArgumentError
from ...variables import is_all
import numpy as np

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.iterator.__init__',
        'iterators.__init__',
        )

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

    if caller is not None:
        if caller.endswith(functions_with_boolean):
            if isinstance(chain_index, bool):
                return chain_index
            else:
                raise ArgumentError('chain_index', value=chain_index, caller=caller, message=None)

    if isinstance(chain_index, (int, np.int64)):
        chain_index=np.ndarray([chain_index])

    if isinstance(chain_index, (tuple, list)):
        chain_index=np.ndarray(chain_index)

    if isinstance(chain_index, np.ndarray):
        return chain_index

    raise ArgumentError('chain_index', value=chain_index, caller=caller, message=None)

