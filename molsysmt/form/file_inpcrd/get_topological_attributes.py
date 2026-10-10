import types

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

form = "file:inpcrd"

# system


@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    """
    Getting n atoms from system in form file:inpcrd.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt._private.files_and_directories import str_filename

    filename = str_filename(item)
    with open(filename, "r") as fff:
        fff.readline()  # title
        # Second line is 'NATOM' (inpcrd) or 'NATOM TIME' (restart)
        n_atoms = int(fff.readline().split()[0])
    return n_atoms


@arg_digest(form=form)
def get_atom_index_from_atom(item, indices="all", skip_digestion=False):
    """Getting source atom-position indices from an AMBER INPCRD file.

    Parameters
    ----------
    item : file:inpcrd
        Input AMBER coordinate file supplying the positional atom axis.
    indices : str, int, list, tuple, or numpy.ndarray, default='all'
        Source positions to return. Preserve their order and repetitions.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of int or none
        Source atom indices, without renumbering a selected subset.
        If indices is None, return None.

    Notes
    -----
    An unrestricted query reads only the header atom count, reusing
    ``get_n_atoms_from_system``. It does not materialize coordinates or infer
    atom IDs, names, connectivity or chemical assignments.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.systems['pentalanine']['pentalanine.inpcrd']
    >>> get_atom_index_from_atom(molsys, indices=[2, 0, 2])
    [2, 0, 2]

    .. versionadded:: 1.0.0
    """
    if indices is None:
        return None
    if is_all(indices):
        n_atoms = get_n_atoms_from_system(item, skip_digestion=True)
        return list(range(n_atoms))
    return list(indices)


# List of functions to be imported
__all__ = [
    name
    for name, obj in globals().items()
    if isinstance(obj, types.FunctionType) and name.startswith("get_")
]
