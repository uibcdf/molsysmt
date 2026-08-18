from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import types
import os
from io import StringIO

form='openmm.PDBFile'

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
        if hasattr(item.file, 'name'):
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
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    """
    Getting coordinates from atom in form openmm.PDBFile.


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
    from openmm.app import PDBFile
    import numpy as np

    item = _ensure_pdbfile(item)

    tmp_positions = item.getPositions()
    tmp_positions = np.array(puw.get_value(tmp_positions, to_unit='nanometers'))
    
    if not is_all(indices):
        tmp_positions = tmp_positions[indices,:]

    output = np.zeros([1, tmp_positions.shape[0], 3])
    output[0,:,:] = tmp_positions
    output = output * puw.unit('nanometers')

    return output

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting box from system in form openmm.PDBFile.


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
    from openmm.app import PDBFile
    import numpy as np

    item = _ensure_pdbfile(item)

    tmp_box = item.getTopology().getPeriodicBoxVectors()
    if tmp_box is not None:
        tmp_box = np.array(puw.get_value(tmp_box, to_unit='nanometers'))
        output = np.zeros([1, 3, 3])
        output[0,:,:] = tmp_box
        output = output * puw.unit('nanometers')
        return output
    return None

@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):
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
def get_time_from_system(item, structure_indices='all', skip_digestion=False):
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
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):
    """
    Getting n structures from system in form openmm.PDBFile.


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
    return 1

# List of functions to be imported
import types
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
