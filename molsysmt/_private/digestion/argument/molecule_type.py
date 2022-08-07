from ...exceptions import ArgumentError
from ...variables import is_all

def digest_molecule_type(molecule_type, caller=None):
    """Checks if `molecule_type` has the expected type and value.

    Parameters
    ----------
    molecule_type : Any
        The `molecule_type` argument for digestion.
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
        If the given `molecule_type` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get.get':
        if isinstance(molecule_type, bool):
            return molecule_type

    raise ArgumentError('molecule_type', value=molecule_type, caller=caller, message=None)

