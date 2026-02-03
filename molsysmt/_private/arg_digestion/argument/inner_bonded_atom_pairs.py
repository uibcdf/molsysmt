from ...exceptions import ArgumentError
from ...variables import is_all

def digest_inner_bonded_atom_pairs(inner_bonded_atom_pairs, caller=None):
    """Checks if `inner_bonded_atom_pairs` has the expected type and value.

    Parameters
    ----------
    inner_bonded_atoms_pairs : Any
        The `inner_bonded_atoms_pairs` argument for digestion.
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
        If the given `inner_bonded_atoms_pairs` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get.get':
        if isinstance(inner_bonded_atom_pairs, bool):
            return inner_bonded_atom_pairs

    raise ArgumentError('inner_bonded_atom_pairs', value=inner_bonded_atom_pairs, caller=caller, message=None)

