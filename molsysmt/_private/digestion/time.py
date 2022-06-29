from ..exceptions import *


def digest_time(time):
    """ Check if time is null or a float.

        Parameters
        ----------
        time : None or float
            The time.

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
    raise WrongTimeError()
