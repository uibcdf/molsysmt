from molsysmt._private.exceptions import ArgumentError
from molsysmt import pyunitwizard as puw
import numpy as np

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        'molsysmt.basic.iterator.__init__',
        'iterators.__init__',
        )

def digest_temperature(temperature, caller=None):
    """ Checks if temperature arguments has the correct type.

        Parameters
        ---------
        temperature: None, integer, list, tuple or ndarray
            The temperature argument.

        caller: str, optional
            Name of the function or method that is being digested.

        Returns
        -------
        ndarray
            The temperature with correct type

        Raises
        -------
        WrongStepError
            If temperature is not a valid argument.

    """

    if caller.endswith(functions_with_boolean):
        if isinstance(temperature, bool):
            return temperature

    if temperature is None:
        return temperature

    value, unit = puw.get_value_and_unit(temperature)

    if not puw.check(unit, dimensionality={'[K]':1}):
        raise ArgumentError('temperature', value=coordinates, caller=caller, message=None)

    if isinstance(value, (int, np.int64, float, np.float64)):
        return puw.quantity(value, unit, standardized=True)

    raise ArgumentError('temperature', value=temperature, caller=caller, message=None)

