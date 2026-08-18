from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='openmm.Context'

###### Set

## to atom

@arg_digest(form=form)
def set_coordinates_to_atom(item, indices='all', value=None, skip_digestion=False):

    """
    Setting coordinates to atom on form openmm.Context.

    Parameters
    ----------
    item : openmm.Context
        Source item in openmm.Context form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    value = puw.convert(value[0], to_unit='nanometers', to_form='openmm.unit')

    if is_all(indices):
        item.setPositions(value)
    else:
        positions = item.getState(getPositions=True).getPositions(asNumpy=True)
        positions[indices,:]=value
        item.setPositions(positions)

    pass

###
### System
###

@arg_digest(form=form)
def set_coordinates_to_system(item, value=None, skip_digestion=False):

    """
    Setting coordinates to system on form openmm.Context.

    Parameters
    ----------
    item : openmm.Context
        Source item in openmm.Context form.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    return set_coordinates_to_atom(item, indices='all', value=value)

