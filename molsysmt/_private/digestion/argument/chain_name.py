from ...exceptions import ArgumentError
from ...variables import is_all
from numpy import ndarray

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        'molsysmt.basic.iterator.__init__',
        'iterators.__init__',
        )


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

    if caller.endswith(functions_with_boolean):
        if isinstance(chain_name, bool):
            return chain_name
    elif caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        return chain_name
    elif '.set.set' in caller:
        if isinstance(chain_name, (int, str, list, tuple, ndarray)):
            return chain_name
    elif caller=='molsysmt.build.define_new_chain.define_new_chain':
        if isinstance(chain_name, str):
            return chain_name
        elif chain_name is None:
            return chain_name
    elif isinstance(chain_name, str):
        return chain_name

    raise ArgumentError('chain_name', value=chain_name, caller=caller, message=None)

