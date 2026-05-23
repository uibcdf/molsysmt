import numpy as np

from molsysmt import pyunitwizard as puw


def _normalize_coordinates_array(values, dtype=np.float64):
    array = np.asarray(values, dtype=dtype)
    from molsysmt._private.smonitor import StructuralInconsistencyError
    if array.ndim == 1:
        if array.shape[0] != 3:
            raise StructuralInconsistencyError("Coordinates must have trailing shape (3,).")
        array = array[np.newaxis, np.newaxis, :]
    elif array.ndim == 2:
        if array.shape[1] != 3:
            raise StructuralInconsistencyError("Coordinates must have trailing shape (3,).")
        array = array[np.newaxis, :, :]
    elif array.ndim == 3:
        if array.shape[2] != 3:
            raise StructuralInconsistencyError("Coordinates must have trailing shape (3,).")
    else:
        raise StructuralInconsistencyError("Coordinates must have rank 1, 2 or 3.")

    return array


def extract_coordinates_value_and_unit(value):
    import molsysmt.configure as config
    dtype = np.float32 if getattr(config, 'precision', 'double') == 'single' else np.float64
    values, unit = puw.get_value_and_unit(
        value,
        value_type="numpy.ndarray",
        dtype=dtype,
    )
    return _normalize_coordinates_array(values, dtype=dtype), unit



def align_coordinates_values_and_unit(coordinates, reference_coordinates):
    import molsysmt.configure as config
    dtype = np.float32 if getattr(config, 'precision', 'double') == 'single' else np.float64
    # Performance path: extract the value and unit of the first set
    coordinates_value, unit = extract_coordinates_value_and_unit(coordinates)
    
    # Align the reference set to the same unit. 
    reference_value = _normalize_coordinates_array(
        puw.get_value(reference_coordinates, to_unit=unit, dtype=dtype),
        dtype=dtype
    )
    return coordinates_value, reference_value, unit

