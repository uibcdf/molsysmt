#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='openmm.CharmmPsfFile'


@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):
    """
    Getting box from system in form openmm.CharmmPsfFile.

    Parameters
    ----------
    item : openmm.CharmmPsfFile
        Source item in openmm.CharmmPsfFile form.
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
    if structure_indices is None or item.box_vectors is None:
        return None

    values = np.asarray(puw.get_value(item.box_vectors))
    unit = puw.get_unit(item.box_vectors)
    output = puw.standardize(values.reshape(1, 3, 3) * unit)
    if not is_all(structure_indices):
        output = output[structure_indices, :, :]
    return output

# List of functions to be imported
import types
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
