import os
import types
from io import StringIO

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

form = "openmm.PDBFile"


def _ensure_pdbfile(item):
    from openmm.app import PDBFile

    if isinstance(item, str):
        is_file = False
        if len(item) < 1024:
            try:
                if os.path.isfile(item):
                    is_file = True
            except Exception:
                pass

        if is_file:
            return PDBFile(item)
        else:
            return PDBFile(StringIO(item))
    elif isinstance(item, os.PathLike):
        return PDBFile(str(item))
    elif str(type(item)).endswith("PDBFileHandler'>"):
        if hasattr(item.file, "name"):
            try:
                if os.path.isfile(item.file.name):
                    return PDBFile(item.file.name)
            except Exception:
                pass
        # Fallback to content or buffer
        item.file.seek(0)
        return PDBFile(item.file)
    return item


@arg_digest(form=form)
def get_coordinates_from_atom(
    item, indices="all", structure_indices="all", skip_digestion=False
):
    """Getting selected PDB model coordinates.

    Parameters
    ----------
    item : openmm.PDBFile
        Loaded PDB hierarchy and its coordinate models.
    indices : str or list of int, default='all'
        Atom positions to query, preserving request order and repetitions.
    structure_indices : str or list of int, default='all'
        Model positions on the structure axis, preserving request order and
        repetitions. An empty list returns a zero-length structure axis.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    quantity
        Coordinates of shape (n_structures, n_atoms, 3), standardized through
        PyUnitWizard. The factory length unit is nm.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from openmm.app import PDBFile
    >>> molsys = PDBFile(str(msm.systems['Trp-Cage']['1l2y.pdb']))
    >>> get_coordinates_from_atom(molsys, indices=[0], structure_indices=[0, 0]).shape
    (2, 1, 3)

    .. versionadded:: 1.0.0
    """
    import numpy as np

    item = _ensure_pdbfile(item)

    models = np.arange(item.getNumFrames())
    if not is_all(structure_indices):
        models = models[structure_indices]
    output = np.asarray(
        [
            puw.get_value(item.getPositions(frame=int(index)), to_unit="nm")
            for index in models
        ]
    ).reshape(len(models), item.topology.getNumAtoms(), 3)
    if not is_all(indices):
        output = output[:, indices, :]
    return puw.standardize(puw.quantity(output, "nm"))


@arg_digest(form=form)
def get_box_from_system(item, structure_indices="all", skip_digestion=False):
    """Getting the common PDB box for each selected structure.

    Parameters
    ----------
    item : openmm.PDBFile
        Loaded PDB hierarchy with an optional periodic box.
    structure_indices : str or list of int, default='all'
        Model positions defining the output structure axis. The single stored
        topology box is repeated along that selected axis.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    quantity or none
        Box vectors of shape (n_structures, 3, 3) in the configured standard
        length unit (nm by default), or None when the source has no box.

    .. versionadded:: 1.0.0
    """
    import numpy as np

    item = _ensure_pdbfile(item)

    tmp_box = item.getTopology().getPeriodicBoxVectors()
    if tmp_box is not None:
        tmp_box = np.array(puw.get_value(tmp_box, to_unit="nanometers"))
        count = get_n_structures_from_system(
            item, structure_indices=structure_indices, skip_digestion=True
        )
        output = np.repeat(tmp_box[np.newaxis, :, :], count, axis=0)
        return puw.standardize(puw.quantity(output, "nm"))
    return None


@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting structure id from system in form openmm.PDBFile.


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


@arg_digest(form=form)
def get_time_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting time from system in form openmm.PDBFile.


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


@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices="all", skip_digestion=False):
    """Getting the number of selected PDB coordinate models.

    Parameters
    ----------
    item : openmm.PDBFile
        Loaded PDB hierarchy and its coordinate models.
    structure_indices : str or list of int, default='all'
        Model positions to count. Repeated positions count as repeated query
        entries; an empty list returns zero.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    int
        Number of coordinate models on the selected structure axis.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from openmm.app import PDBFile
    >>> molsys = PDBFile(str(msm.systems['Trp-Cage']['1l2y.pdb']))
    >>> get_n_structures_from_system(molsys, structure_indices=[2, 0])
    2

    .. versionadded:: 1.0.0
    """
    import numpy as np

    item = _ensure_pdbfile(item)
    count = item.getNumFrames()
    if is_all(structure_indices):
        return count
    return len(np.arange(count)[structure_indices])


# List of functions to be imported
__all__ = [
    name
    for name, obj in globals().items()
    if isinstance(obj, types.FunctionType) and name.startswith("get_")
]
