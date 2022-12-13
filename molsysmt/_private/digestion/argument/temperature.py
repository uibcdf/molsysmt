from molsysmt._private.exceptions import ArgumentError
import numpy as np

functions_with_boolean = (
        'molsysmt.basic.get.get',
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

    raise ArgumentError('temperature', value=temperature, caller=caller, message=None)

