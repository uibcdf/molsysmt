from ..exceptions import WrongComparisonError

def digest_comparison(comparison, caller=None):
    """ Checks if step arguments has the correct type.

        Parameters
        ---------
        comparison: Any
            The comparison argument.

        caller: str, optional
            Name of the function or method that is being digested.

        Returns
        -------
        ndarray
            The comparison with correct type

        Raises
        -------
        WrongComparisonError
            If comparison is not a valid argument.

    """
    return comparison

