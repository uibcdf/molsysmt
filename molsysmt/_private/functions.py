import inspect


def caller_name(skip=3):
    """ Returns the name of the function that called this.

        Parameters
        ----------
        skip: int
            Number of frames to skip.
            Use 2 to get the caller in an exception, or 3 in an exception
            that is derived from another exception.

        Returns
        -------
        str
            Name of the caller function.
    """
    return inspect.stack()[skip].function

def invoked_by_user():

    return True
