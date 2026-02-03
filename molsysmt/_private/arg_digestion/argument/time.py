from molsysmt._private.exceptions import ArgumentError
from molsysmt import pyunitwizard as puw
import numpy as np

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        'molsysmt.basic.iterator.__init__',
        'iterators.__init__'
        )

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

    if caller.endswith(functions_with_boolean):
        if isinstance(time, bool):
            return time

    if time is None:
        return time

    if puw.is_quantity(time):
        if puw.check(time, dimensionality={'[T]':1}):
            return puw.standardize(time)
    elif type(time, (list, tuple, np.ndarray)):
        if puw.is_quantity(time[0]):
            time = puw.utils.sequences.concatenate(time, value_type='numpy.ndarray')
            if puw.check(time, dimensionality={'[T]':1}):
                return puw.standardize(time)

    raise ArgumentError('time', value=time, caller=caller, message=None)

