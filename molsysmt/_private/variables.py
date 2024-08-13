import numpy as np
from molsysmt import pyunitwizard as puw

def is_all(variable):

    """Checks if the value of a variable is equal to 'all', 'All', or 'ALL'.

    The method returns True if the value of a variable is equal to 'all', 'All', or 'ALL'.

    Parameters
    ----------
    variable: Any
        Input variable to be compared with 'all', 'All', or 'ALL'.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/#the-any-type

    Returns
    -------
    Bool
        True if successful, False otherwise.

    Examples
    --------
    The method accepts any type. It returns True in case the value is 'all', 'All' or 'ALL'.

    >>> is_all('All')
    True

    >>> is_all([0, 1, 2])
    False

    """

    if isinstance(variable, str):
        return variable in ['all', 'All', 'ALL']

    return False

def is_iterable(variable):

    if isinstance(variable, (list, tuple, set, np.ndarray)):
        return True

    return False

def is_iterable_of_iterables(variable):

    if isinstance(variable, (list, tuple, set, np.ndarray)):
        return all([is_iterable(ii) for ii in variable])

    return False

def is_iterable_of_iterables_of_iterables(variable):

    if isinstance(variable, (list, tuple, set, np.ndarray)):
        return all([is_iterable_of_iterables(ii) for ii in variable])

    return False

def is_next(variable):

    if isinstance(variable, str):
        return variable in ['next', 'Next', 'NEXT']

    return False

def is_iterable_of_pairs(variable):

    output = False

    if isinstance(variable, np.ndarray):
        if len(variable.shape)==2:
            if variable.shape[1]==2:
                output = True
    elif isinstance(variable, (list, tuple, set)):
        for ii in variable:
            output = False
            if isinstance(ii, (list, tuple, set)):
                if len(ii) == 2:
                    output = True
            if output == False:
                break

    return output

def is_iterable_of_integers(variable):

    output = False

    if isinstance(variable, np.ndarray):
        if len(variable.shape)==1:
            if np.issubdtype(variable.dtype, np.integer):
                output = True
    elif isinstance(variable, (list, tuple, set)):
        if all(isinstance(ii, int) for ii in variable):
            output = True

    return output

def is_compatible_with_coordinates_value(variable):

    output = False

    if puw.is_quantity(variable):
        value = puw.get_value(variable)
    else:
        value = variable

    if isinstance(value, (list, tuple, set)):

        value = np.ndarray(value)

    if isinstance(value, np.ndarray):

        shape = value.shape

        if len(shape) == 1:
            if shape[0] == 3:
                if value.dtype in (np.int64, np.int32, np.float32, np.float64):
                    output = True
        elif len(shape) == 2:
            if shape[1] == 3:
                if value.dtype in (np.int64, np.int32, np.float32, np.float64):
                    output = True
        elif len(shape) == 3:
            if shape[2] == 3:
                if value.dtype in (np.int64, np.int32, np.float32, np.float64):
                    output = True

    del value

    return output

def is_compatible_with_coordinates_unit(variable):

    output = False

    if puw.is_quantity(variable):
        unit = puw.get_unit(variable)
        if puw.check(unit, dimensionality={'[L]':1}):
            output = True

    return output
        
def is_compatible_with_coordinates(variable):

    output = False

    if is_compatible_with_coordinates_unit(variable):
        if is_compatible_with_coordinates_value(variable):
            output = True

    return True

def make_coordinates_like(variable, standardized=True):

    output = None

    if is_compatible_with_coordinates_unit(variable):
        if is_compatible_with_coordinates_value(variable):

            value, unit = puw.get_value_and_unit(variable)

            if not isinstance(value, np.ndarray):
                value = np.array(value)

            shape = value.shape

            if len(shape) == 1:
                if shape[0] == 3:
                    output = puw.quantity(value[np.newaxis, np.newaxis, :], unit, standardized=standardized)
            elif len(shape) == 2:
                if shape[1] == 3:
                    output = puw.quantity(value[np.newaxis, :, :], unit, standardized=standardized)
            elif len(shape) == 3:
                if shape[2] == 3:
                    output = puw.quantity(value, unit, standardized=standardized)

    if output is None:
        raise ValueError()

    return output

