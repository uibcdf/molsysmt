import numpy as np
from molsysmt import pyunitwizard as _puw
from molsysmt._private.variables import is_all as _is_all

def set_coordinates_to_atom(item, indices='all', structure_indices='all', value=None):

    """
    Setting coordinates to atom on form molsysmt.StructuresDict.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    value : object, default=None
        Argument value.

    .. versionadded:: 1.0.0
    """
    length_unit = _puw.get_unit(item['coordinates'])
    value = _puw.convert(value, to_unit=length_unit)

    if _is_all(indices):
        if _is_all(structure_indices):
            item['coordinates']=value
        else:
            item['coordinates'][structure_indices,:,:]=value
    else:
        if _is_all(structure_indices):
            item['coordinates'][:,indices,:]=value
        else:
            item['coordinates'][np.ix_(indices,structure_indices)]=value

    pass


