from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

from ._header import _read_counts
from .to_molsysmt_StructuresDict import to_molsysmt_StructuresDict


@arg_digest(form="file:trjpk")
def get_n_structures_from_system(item, structure_indices="all", skip_digestion=False):
    """Getting the structure count from the TRJPK header.

    Parameters
    ----------
    item : file:trjpk
        Input file using the existing six-record pickle layout.
    structure_indices : str, int, list, tuple, or numpy.ndarray, default='all'
        Structure positions to include, retaining order and repetitions; None returns None.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    int or none
        Declared structure count, or the number of selected positions.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.systems['two LJ particles']['traj_two_lj_particles.trjpk']
    >>> get_n_structures_from_system(molsys)
    20000

    .. versionadded:: 1.0.0
    """
    if structure_indices is None:
        return None
    if is_all(structure_indices):
        return int(_read_counts(item)[1])
    return len(structure_indices)


@arg_digest(form="file:trjpk")
def get_coordinates_from_atom(
    item, indices="all", structure_indices="all", skip_digestion=False
):
    """Getting coordinates from a TRJPK file.

    Parameters
    ----------
    item : file:trjpk
        Input file using the existing six-record pickle layout.
    indices : str, int, list, tuple, or numpy.ndarray, default='all'
        Atom positions to return, retaining order and repetitions; None returns None.
    structure_indices : str, int, list, tuple, or numpy.ndarray, default='all'
        Structure positions to include, retaining order and repetitions; None returns None.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    quantity or none
        Coordinates with shape (n_structures, n_atoms, 3), stored in nm.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.systems['two LJ particles']['traj_two_lj_particles.trjpk']
    >>> get_coordinates_from_atom(molsys, indices=[1], structure_indices=[2, 0]).shape
    (2, 1, 3)

    .. versionadded:: 1.0.0
    """
    if structure_indices is None or indices is None:
        return None
    data = to_molsysmt_StructuresDict(
        item,
        atom_indices=indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    return data["coordinates"]


@arg_digest(form="file:trjpk")
def get_coordinates_from_system(item, structure_indices="all", skip_digestion=False):
    """Getting coordinates from a TRJPK file.

    Parameters
    ----------
    item : file:trjpk
        Input file using the existing six-record pickle layout.
    structure_indices : str, int, list, tuple, or numpy.ndarray, default='all'
        Structure positions to include, retaining order and repetitions; None returns None.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    quantity or none
        Coordinates with shape (n_structures, n_atoms, 3), stored in nm.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.systems['two LJ particles']['traj_two_lj_particles.trjpk']
    >>> get_coordinates_from_system(molsys, structure_indices=[2, 0]).shape
    (2, 2, 3)

    .. versionadded:: 1.0.0
    """
    if structure_indices is None:
        return None
    data = to_molsysmt_StructuresDict(
        item, structure_indices=structure_indices, skip_digestion=True
    )
    return data["coordinates"]


@arg_digest(form="file:trjpk")
def get_box_from_system(item, structure_indices="all", skip_digestion=False):
    """Getting box from a TRJPK file.

    Parameters
    ----------
    item : file:trjpk
        Input file using the existing six-record pickle layout.
    structure_indices : str, int, list, tuple, or numpy.ndarray, default='all'
        Structure positions to include, retaining order and repetitions; None returns None.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    quantity or none
        Box vectors with shape (n_structures, 3, 3), stored in nm.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.systems['two LJ particles']['traj_two_lj_particles.trjpk']
    >>> get_box_from_system(molsys, structure_indices=[2, 0]).shape
    (2, 3, 3)

    .. versionadded:: 1.0.0
    """
    if structure_indices is None:
        return None
    data = to_molsysmt_StructuresDict(
        item, structure_indices=structure_indices, skip_digestion=True
    )
    return data["box"]


@arg_digest(form="file:trjpk")
def get_time_from_system(item, structure_indices="all", skip_digestion=False):
    """Getting time from a TRJPK file.

    Parameters
    ----------
    item : file:trjpk
        Input file using the existing six-record pickle layout.
    structure_indices : str, int, list, tuple, or numpy.ndarray, default='all'
        Structure positions to include, retaining order and repetitions; None returns None.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    quantity or none
        Structure times with shape (n_structures,), stored in ps.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.systems['two LJ particles']['traj_two_lj_particles.trjpk']
    >>> get_time_from_system(molsys, structure_indices=[2, 0]).shape
    (2,)

    .. versionadded:: 1.0.0
    """
    if structure_indices is None:
        return None
    data = to_molsysmt_StructuresDict(
        item, structure_indices=structure_indices, skip_digestion=True
    )
    return data["time"]


@arg_digest(form="file:trjpk")
def get_structure_id_from_system(item, structure_indices="all", skip_digestion=False):
    """Getting structure id from a TRJPK file.

    Parameters
    ----------
    item : file:trjpk
        Input file using the existing six-record pickle layout.
    structure_indices : str, int, list, tuple, or numpy.ndarray, default='all'
        Structure positions to include, retaining order and repetitions; None returns None.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    numpy.ndarray or none
        Original structure labels aligned with the selected structures.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.systems['two LJ particles']['traj_two_lj_particles.trjpk']
    >>> get_structure_id_from_system(molsys) is None
    True

    .. versionadded:: 1.0.0
    """
    if structure_indices is None:
        return None
    data = to_molsysmt_StructuresDict(
        item, structure_indices=structure_indices, skip_digestion=True
    )
    return data["structure_id"]


__all__ = [name for name in globals() if name.startswith("get_")]
