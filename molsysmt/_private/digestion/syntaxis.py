
syntaxis = [
    'MolSysMT',
    'Amber',
    'MDAnalysis',
    'MDTraj',
    'ParmEd',
    'NGLView',
]

syntaxis_from_lower = {ii.lower(): ii for ii in syntaxis}


def digest_syntaxis(syntaxis, caller=""):
    """ Helper function to check if the given syntaxis is supported by
        MolSysMt.

        Parameters
        ----------
        syntaxis : str
            The name of the syntaxis in lower case.

        caller: str, optional
            Name of the function or method that is being digested.
            For debugging purposes.

        Returns
        -------
        syntaxis : str
            The name of the syntaxis respecting capital letters.
    """
    from ..exceptions import WrongSyntaxisError

    if not isinstance(syntaxis, str):
        raise WrongSyntaxisError("syntaxis must be a string.", caller)

    try:
        syntaxis = syntaxis_from_lower[syntaxis.lower()]
    except KeyError:
        raise WrongSyntaxisError(f"{syntaxis} is not a valid syntaxis.", caller)

    return syntaxis


def digest_to_syntaxis(to_syntaxis, caller=""):
    """ Check if to syntaxis is a valid syntaxis. Can also be null.
    """
    if to_syntaxis is None:
        return None
    else:
        return digest_syntaxis(to_syntaxis, caller)
