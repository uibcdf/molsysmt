
syntaxis = [
    'MolSysMT',
    'Amber',
    'MDAnalysis',
    'MDTraj',
    'ParmEd',
    'NGLView',
]

syntaxis_from_lower = {ii.lower(): ii for ii in syntaxis}


def digest_syntaxis(syntaxis):
    """ Helper function to check if the given syntaxis is supported by
        MolSysMt.
    """
    from ..exceptions import WrongSyntaxisError

    if not isinstance(syntaxis, str):
        raise WrongSyntaxisError("syntaxis must be a string.")

    try:
        syntaxis = syntaxis_from_lower[syntaxis.lower()]
        return syntaxis
    except KeyError:
        raise WrongSyntaxisError(f"{syntaxis} is not a valid syntaxis.")


def digest_to_syntaxis(to_syntaxis):

    if to_syntaxis is None:
        return None
    else:
        return digest_syntaxis(to_syntaxis)

