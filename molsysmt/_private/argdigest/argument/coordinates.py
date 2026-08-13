import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError, FormatError, InternalAlgorithmError

functions_where_boolean = (
    "molsysmt.basic.get.get",
    "molsysmt.basic.compare.compare",
    "molsysmt.basic.iterator.__init__",
    ".iterators.__init__",
)


def digest_coordinates(coordinates, caller=None):
    if caller is not None:
        if caller.endswith(functions_where_boolean):
            if isinstance(coordinates, bool):
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
        if not puw.check(unit, dimensionality={"[L]": 1}):
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

        # Convert to nanometers if it has units
        if unit is not None:
            value_nm = puw.get_value(coordinates, to_unit="nm")
            value_nm = np.asarray(value_nm, dtype=np.float64)
            value_nm = value_nm.reshape(value.shape)
        else:
            value_nm = value

        # --- Native Structures Internal Path ---
        if caller is not None and caller.startswith("molsysmt.native.structures"):
            return value_nm

        # Performance: return as quantity in ORIGINAL unit.
        # Avoid forced standardize() unless specifically needed downstream.
        q = puw.quantity(value, unit)

        return q

    except Exception as e:
        raise ArgumentError("coordinates", value=coordinates, caller=caller) from e
