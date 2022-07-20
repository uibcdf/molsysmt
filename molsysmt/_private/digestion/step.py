from ..exceptions.step import WrongStepError
import numpy as np

def digest_step(step, caller=None):
    """ Checks if step arguments has the correct type.

        Parameters
        ---------
        step: None, integer, list, tuple or ndarray
            The step argument.

        caller: str, optional
            Name of the function or method that is being digested.

        Returns
        -------
        ndarray
            The step with correct type

        Raises
        -------
        WrongStepError
            If step is not a valid argument.

    """
    if step is None:
        return step
    elif isinstance(step, int):
        return np.array([step])
    elif isinstance(step, (list, tuple)):
        return np.array(step)
    elif isinstance(step, np.ndarray):
        return step

    raise WrongStepError(step, caller=caller)

