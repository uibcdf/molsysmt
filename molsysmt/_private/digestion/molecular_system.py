from ..exceptions import WrongMolecularSystemError
from ..exceptions import WrongMultipleMolecularSystemsError

def digest_single_molecular_system(molecular_system, caller=None):
    """ Check if an object is a molecular system.

        Parameters
        ----------
        molecular_system : Any
            The molecular system object to be checked.
        caller: str, optional
            Name of the function or method that is being digested.

        Returns
        -------
        molecular_system : Any
            The molecular system object.

        Raises
        ------
        MolecularSystemNeededError
            If the given object is not a molecular system.
    """
    from molsysmt.basic import is_molecular_system

    if not is_molecular_system(molecular_system):
        raise WrongMolecularSystemError(caller=caller)
    return molecular_system


def digest_multiple_molecular_systems(molecular_systems, caller=None):
    """ Check if an object is a list or tuple of molecular systems.

        Parameters
        ----------
        molecular_systems : list or tuple
            The lists of molecular systems to be checked.

        caller: str, optional
            Name of the function or method that is being digested.

        Returns
        -------
        molecular_system : list of molecular systems
            The molecular system.

        Raises
        ------
        MultipleMolecularSystemsError
            If the given object is not a list of molecular systems.
    """
    from molsysmt.basic import are_multiple_molecular_systems

    if not are_multiple_molecular_systems(molecular_systems):
        raise WrongMultipleMolecularSystemsNeededError(caller=caller)
    return molecular_systems
