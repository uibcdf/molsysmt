from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest()
def has_hydrogens(molecular_system, selection='all', syntax='MolSysMT', skip_digestion=False):
    """
    Checking if a molecular system or selected subset contains hydrogen atoms.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported form.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection of atoms to inspect.
    syntax : str, default='MolSysMT'
        Selection syntax used.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    bool
        True if any hydrogen atom is present in the selection, False otherwise.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get, select

    if is_all(selection):
        n_Hs = get(molecular_system, selection='atom_type=="H"', n_atoms=True, skip_digestion=True)
    else:
        mask = select(molecular_system, selection=selection, syntax=syntax, skip_digestion=True)
        n_Hs = get(molecular_system, selection='atom_type=="H"', mask=mask, n_atoms=True, skip_digestion=True)

    return n_Hs>0
