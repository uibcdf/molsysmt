from ...exceptions import ArgumentError
from ...variables import is_all

def digest_molecule_index(molecule_index, caller=None):
    """Checks if `molecule_index` has the expected type and value.

    Parameters
    ----------
    molecule_index : Any
        The `molecule_index` argument for digestion.
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
        If the given `molecule_index` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get.get':
        if isinstance(molecule_index, bool):
            return molecule_index

    raise ArgumentError('molecule_index', value=molecule_index, caller=caller, message=None)

