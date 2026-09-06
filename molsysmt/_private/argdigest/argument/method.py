from molsysmt._private.smonitor import ArgumentError

# The only surface taking a `method` argument is the potential energy minimization,
# and its OpenMM backend exposes a single algorithm through LocalEnergyMinimizer.
_supported_methods = {'l-bfgs': 'L-BFGS'}


def digest_method(method, caller=None):
    """ Check the name of the minimization method.

        Parameters
        ----------
        method : str
            The name of the method.

        caller : str, optional
            Name of the function or method that is being digested.

        Returns
        -------
        str
            The canonical name of the method.

        Raises
        ------
        ArgumentError
            If the method is not a string or its name is not supported.
    """

    if isinstance(method, str):
        try:
            return _supported_methods[method.lower()]
        except KeyError:
            pass

    raise ArgumentError('method', value=method, caller=caller, message=None)
