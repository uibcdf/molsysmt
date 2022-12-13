from molsysmt._private.exceptions import ArgumentError
import numpy as np

functions_with_boolean = [
        'molsysmt.basic.get.get',
        'molsysmt.basic.iterator.__init__',
        ]

def digest_time(time, caller=None):
    """ Checks if time arguments has the correct type.

        Parameters
        ---------
        time: None, integer, list, tuple or ndarray
            The time argument.

        caller: str, optional
            Name of the function or method that is being digested.

        Returns
        -------
        ndarray
            The time with correct type

        Raises
        -------
        WrongStepError
            If time is not a valid argument.

    """

    if caller in functions_with_boolean:
        if isinstance(time, bool):
            return time

    if caller.endswith('iterators.__init__'):
        if isinstance(time, bool):
            return time

    if time is None:
        return time
    elif isinstance(time, float):
        return np.array([time])
    elif isinstance(time, (list, tuple)):
        return np.array(time)
    elif isinstance(time, np.ndarray):
        return time

    raise ArgumentError('time', value=time, caller=caller, message=None)

