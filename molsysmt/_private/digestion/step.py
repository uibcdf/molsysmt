from ..exceptions import *


def digest_step(step):
    """ Checks if step is an integer or null.

        Parameters
        ---------
        step: Any
            The step

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
    raise WrongStepError()
