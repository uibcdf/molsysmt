from molsysmt._private.exceptions import ArgumentError
import numpy as np

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
    if time is None:
        return time
    elif isinstance(time, float):
        return np.array([time])
    elif isinstance(time, (list, tuple)):
        return np.array(time)
    elif isinstance(time, np.ndarray):
        return time

    raise ArgumentError('time', caller=caller, message=None)

