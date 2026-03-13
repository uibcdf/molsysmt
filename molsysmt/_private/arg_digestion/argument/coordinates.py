from molsysmt._private.smonitor import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

functions_where_boolean = (
    'molsysmt.basic.get.get',
    'molsysmt.basic.compare.compare',
    'molsysmt.basic.iterator.__init__',
    '.iterators.__init__'
    )

def digest_coordinates(coordinates, caller=None):

    if caller is not None:
        if caller.endswith(functions_where_boolean):
            if isinstance(coordinates, bool):
                return coordinates

    if coordinates is None:
        return None

    # We use the new argdigest pipeline logic manually here or let argdigest do it
    # For now, we standardize to quantity array with float64
    from argdigest.pipelines.science import to_float64_array

    try:
        if isinstance(coordinates, str):
            coordinates = puw.parse.parse(coordinates)

        value = to_float64_array(coordinates)
        unit = puw.get_unit(coordinates)
        
        if not puw.check(unit, dimensionality={'[L]':1}):
            raise ValueError("Incompatible units for coordinates")

        shape = value.shape

        if len(shape) == 1:
            if shape[0] == 3:
                value = value[np.newaxis, np.newaxis, :]
            else:
                raise ValueError("Wrong shape")
        elif len(shape) == 2:
            if shape[1] == 3:
                value = value[np.newaxis, :, :]
            else:
                raise ValueError("Wrong shape")
        elif len(shape) == 3:
            if shape[2] != 3:
                raise ValueError("Wrong shape")
        else:
            raise ValueError("Wrong dimensions")

        return puw.standardize(puw.quantity(value, unit))

    except Exception as e:
        raise ArgumentError('coordinates', value=coordinates, caller=caller) from e
