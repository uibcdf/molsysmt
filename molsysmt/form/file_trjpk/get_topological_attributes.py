from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

from ._header import _read_counts

__all__ = ["get_n_atoms_from_system", "get_atom_index_from_atom"]


@arg_digest(form="file:trjpk")
def get_n_atoms_from_system(item, skip_digestion=False):
    """Getting the atom count from the TRJPK header.

    Parameters
    ----------
    item : file:trjpk
        Input file using the existing six-record pickle layout.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    int
        Declared atom count, without materializing the stored arrays.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.systems['two LJ particles']['traj_two_lj_particles.trjpk']
    >>> get_n_atoms_from_system(molsys)
    2

    .. versionadded:: 1.0.0
    """
    return int(_read_counts(item)[0])


@arg_digest(form="file:trjpk")
def get_atom_index_from_atom(item, indices="all", skip_digestion=False):
    """Getting positional atom indices from a TRJPK file.

    Parameters
    ----------
    item : file:trjpk
        Input file using the existing six-record pickle layout.
    indices : str, int, list, tuple, or numpy.ndarray, default='all'
        Atom positions to return, retaining order and repetitions; None returns None.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of int or none
        Source atom positions, without renumbering a selected subset.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.systems['two LJ particles']['traj_two_lj_particles.trjpk']
    >>> get_atom_index_from_atom(molsys, indices=[1, 0, 1])
    [1, 0, 1]

    .. versionadded:: 1.0.0
    """
    if indices is None:
        return None
    if is_all(indices):
        return list(range(get_n_atoms_from_system(item, skip_digestion=True)))
    return list(indices)
