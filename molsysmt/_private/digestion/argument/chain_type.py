from ...exceptions import ArgumentError
from ...variables import is_all
import numpy as np

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        'molsysmt.basic.iterator.__init__',
        'iterators.__init__',
        )


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

    if caller.endswith(functions_with_boolean):
        if isinstance(chain_type, bool):
            return chain_type
    elif caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        return chain_type

    if isinstance(chain_type, str):
        return chain_type

    elif isinstance(chain_type, list):
        return chain_type

    elif isinstance(chain_type, tuple):
        return list(chain_type)

    elif isinstance(chain_type, np.ndarray):
        return chain_type.tolist()

    raise ArgumentError('chain_type', value=chain_type, caller=caller, message=None)

