from molsysmt._private.smonitor import InternalAlgorithmError, FormatError
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
        
        # --- Trusted Path for internal kernel helpers ---
        # If the caller is from molsysmt.lib.structure and already passed an ndarray
        # we trust the prep has been done.
        if caller.startswith("molsysmt.lib.structure"):
            if isinstance(coordinates, np.ndarray) and coordinates.dtype == np.float64:
                return coordinates

    if coordinates is None:
        return None

    from argdigest.pipelines.science import to_float64_array

    try:
        if isinstance(coordinates, str):
            coordinates = puw.parse.parse(coordinates)

        value = to_float64_array(coordinates)
        unit = puw.get_unit(coordinates)
        
        # Validation of dimensionality
        if not puw.check(unit, dimensionality={"[L]":1}):
            from molsysmt._private.smonitor import StructuralInconsistencyError
            raise StructuralInconsistencyError("Incompatible units for coordinates")

        shape = value.shape
        if len(shape) == 1:
            if shape[0] == 3:
                value = value[np.newaxis, np.newaxis, :]
            else:
                raise StructuralInconsistencyError("Wrong shape for coordinates", caller=caller)
        elif len(shape) == 2:
            if shape[1] == 3:
                value = value[np.newaxis, :, :]
            else:
                raise StructuralInconsistencyError("Wrong shape for coordinates", caller=caller)
        elif len(shape) == 3:
            if shape[2] != 3:
                raise StructuralInconsistencyError("Wrong shape for coordinates", caller=caller)
        else:
            raise StructuralInconsistencyError("Wrong dimensions for coordinates", caller=caller)

        # Performance: return as quantity in ORIGINAL unit. 
        # Avoid forced standardize() unless specifically needed downstream.
        return puw.quantity(value, unit)

    except Exception as e:
        from molsysmt._private.smonitor import ArgumentError
        raise ArgumentError("coordinates", value=coordinates, caller=caller) from e

