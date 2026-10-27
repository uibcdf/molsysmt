import types

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

form = "mdtraj.GroTrajectoryFile"


def _read_complete_source(item, atom_indices=None):
    """Read an independent input so the caller's opaque text cursor is untouched."""
    from .copy import _open_reader

    # Attribute reads never mutate topology, so keep the provider's read-only
    # topology reference instead of copying a potentially large graph per query.
    reader = _open_reader(item)
    try:
        return reader.read(atom_indices=atom_indices)
    finally:
        reader.close()


@arg_digest(form=form)
def get_coordinates_from_atom(
    item, indices="all", structure_indices="all", skip_digestion=False
):
    """
    Getting coordinates from atom in form mdtraj.GroTrajectoryFile.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    tmp_item = _read_complete_source(
        item, atom_indices=indices if not is_all(indices) else None
    )
    output = tmp_item[0]  # shape (n_frames, n_atoms, 3), nanometers

    if not is_all(structure_indices):
        output = output[structure_indices, :, :]

    output = output * puw.unit("nanometer")
    return output


@arg_digest(form=form)
def get_coordinates_from_system(item, structure_indices="all", skip_digestion=False):
    """Getting all atom coordinates without consuming a GRO reader.

    Parameters
    ----------
    item : mdtraj.GroTrajectoryFile
        Caller-owned readable GRO handler. Its current cursor is preserved.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process. Order and repetitions
        are retained.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    PyUnitWizard quantity
        Coordinates with shape (n_structures, n_atoms, 3), in nanometers.

    Notes
    -----
    Delegates to the atom-coordinate reader on the complete atom population.
    Independent read handles are closed on success and failure; this query
    neither changes the source topology nor advances its iteration position.

    Examples
    --------
    >>> import molsysmt as msm
    >>> reader = msm.convert(msm.systems['nglview']['md_1u19.gro'],
    ...                      to_form='mdtraj.GroTrajectoryFile')
    >>> get_coordinates_from_system(reader).ndim
    3
    >>> reader.close()

    .. versionadded:: 1.0.0
    """
    return get_coordinates_from_atom(
        item, structure_indices=structure_indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_box_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting box from system in form mdtraj.GroTrajectoryFile.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    tmp_item = _read_complete_source(item)
    unitcell_vectors = tmp_item[2]  # shape (n_frames, 3, 3), nanometers

    if unitcell_vectors is not None and len(unitcell_vectors) > 0:
        output = unitcell_vectors * puw.unit("nanometer")
        if not is_all(structure_indices):
            output = output[structure_indices, :, :]
        return output
    return None


@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting n structures from system in form mdtraj.GroTrajectoryFile.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(structure_indices):
        tmp_item = _read_complete_source(item)
        return tmp_item[0].shape[0]
    else:
        return len(structure_indices)


@arg_digest(form=form)
def get_time_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting time from system in form mdtraj.GroTrajectoryFile.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    tmp_item = _read_complete_source(item)
    if tmp_item[1] is not None:
        output = tmp_item[1] * puw.unit("picosecond")
        if not is_all(structure_indices):
            output = output[structure_indices]
        return output
    return None


@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting structure id from system in form mdtraj.GroTrajectoryFile.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return None


# List of functions to be imported
__all__ = [
    name
    for name, obj in globals().items()
    if isinstance(obj, types.FunctionType) and name.startswith("get_")
]
