from ..exceptions import *


def digest_time(time, caller=""):
    """ Check if time is null or a float.

        Parameters
        ----------
        time : None or float
            The time.

        caller: str, optional
            Name of the function or method that is being digested.
            For debugging purposes.

        Returns
        -------
        None or float

        Raises
        ------
        WrongTimeError
            If time is not a float ot is not null.
    """
    if time is None or isinstance(time, (float, bool)):
        return time
    raise WrongTimeError(type(time), caller)
