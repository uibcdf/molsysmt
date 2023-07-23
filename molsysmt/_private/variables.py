from numpy import ndarray

def is_all(variable):

    """Checks if the value of a variable is equal to 'all', 'All', or 'ALL'.

    The method returns True if the value of a variable is equal to 'all', 'All', or 'ALL'.

    Parameters
    ----------
    variable: Any
        Input variable to be compared with 'all', 'All', or 'ALL'.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/#the-any-type

    Returns
    -------
    Bool
        True if successful, False otherwise.

    Examples
    --------
    The method accepts any type. It returns True in case the value is 'all', 'All' or 'ALL'.

    >>> is_all('All')
    True

    >>> is_all([0, 1, 2])
    False

    """

    if isinstance(variable, str):
        return variable in ['all', 'All', 'ALL']

    return False

def is_iterable_of_iterables(variable):

    if isinstance(variable, (list, tuple, set, ndarray)):
        return all([isinstance(ii, (list, tuple, set, ndarray)) for ii in variable])

    return False


def is_next(variable):

    if isinstance(variable, str):
        return variable in ['next', 'Next', 'NEXT']

    return False

