from ..exceptions import *


def digest_step(step, caller=""):
    """ Checks if step is an integer or null.

        Parameters
        ---------
        step: Any
            The step

        caller: str, optional
            Name of the function or method that is being digested.
            For debugging purposes.

        Returns
        -------
        int or None
            The step

        Raises
        -------
        WrongStepError
            If step is not null or not an integer.

    """
    if step is None or isinstance(step, int):
        return step
    raise WrongStepError(type(step), caller)
