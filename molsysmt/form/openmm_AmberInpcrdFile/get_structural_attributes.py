from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import types

form='openmm.AmberInpcrdFile'

@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    """
    Getting coordinates from atom in form openmm.AmberInpcrdFile.

    Parameters
    ----------
    item : openmm.AmberInpcrdFile
        Source item in openmm.AmberInpcrdFile form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices is None or structure_indices is None:
        return None

    # OpenMM returns positions as a list of Vec3 with units
    tmp_positions = item.getPositions()
    # Convert to pure numpy array in nanometers
    tmp_positions = puw.get_value(tmp_positions, to_unit='nanometers')
    tmp_positions = np.array(tmp_positions)
    
    if not is_all(indices):
        tmp_positions = tmp_positions[indices,:]

    output = np.zeros([1, tmp_positions.shape[0], 3])
    output[0,:,:] = tmp_positions
    output = output * puw.unit('nanometers')

    if not is_all(structure_indices):
        output = output[structure_indices, :, :]

    return output

@arg_digest(form=form)
def get_velocities_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    """
    Getting velocities from atom in form openmm.AmberInpcrdFile.

    Parameters
    ----------
    item : openmm.AmberInpcrdFile
        Source item in openmm.AmberInpcrdFile form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices is None or structure_indices is None:
        return None

    # An inpcrd file only carries velocities when it comes from a restart
    try:
        tmp_velocities = item.getVelocities()
    except AttributeError:
        return None

    if tmp_velocities is None:
        return None

    tmp_velocities = puw.get_value(tmp_velocities, to_unit='nanometers/picosecond')
    tmp_velocities = np.array(tmp_velocities)

    if not is_all(indices):
        tmp_velocities = tmp_velocities[indices,:]

    output = np.zeros([1, tmp_velocities.shape[0], 3])
    output[0,:,:] = tmp_velocities
    output = output * puw.unit('nanometers/picosecond')

    if not is_all(structure_indices):
        output = output[structure_indices, :, :]

    return output

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting box from system in form openmm.AmberInpcrdFile.

    Parameters
    ----------
    item : openmm.AmberInpcrdFile
        Source item in openmm.AmberInpcrdFile form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if structure_indices is None:
        return None

    try:
        tmp_box = item.getBoxVectors()
    except AttributeError:
        return None

    if tmp_box is not None:
        tmp_box = puw.get_value(tmp_box, to_unit='nanometers')
        tmp_box = np.array(tmp_box)
        output = np.zeros([1, 3, 3])
        output[0,:,:] = tmp_box
        output = output * puw.unit('nanometers')
        if not is_all(structure_indices):
            output = output[structure_indices, :, :]
        return output
    return None

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):
    """
    Getting n structures from system in form openmm.AmberInpcrdFile.

    Parameters
    ----------
    item : openmm.AmberInpcrdFile
        Source item in openmm.AmberInpcrdFile form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if structure_indices is None:
        return 0
    if is_all(structure_indices):
        return 1
    return len(structure_indices)


@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):
    """
    Getting structure id from system in form openmm.AmberInpcrdFile.

    Parameters
    ----------
    item : openmm.AmberInpcrdFile
        Source item in openmm.AmberInpcrdFile form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
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
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
