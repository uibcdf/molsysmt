
def digest_single_molecular_system(molecular_system):
    """ Check if an object is a molecular system.

        Parameters
        ----------
        molecular_system : Any
            The molecular system.

        Returns
        -------
        None

        Raises
        ------
        MolecularSystemNeededError
            If the given object is not a molecular system.
    """
    from ..exceptions import MolecularSystemNeededError
    from molsysmt.basic import is_molecular_system

    if not is_molecular_system(molecular_system):
        raise MolecularSystemNeededError()


def digest_multiple_molecular_systems(molecular_systems):
    """ Check if an object is a molecular system.

        Parameters
        ----------
        molecular_systems : Any
            The molecular systems.

        Returns
        -------
        None

        Raises
        ------
        MultipleMolecularSystemsNeededError
            If the given object is not composed of multiple molecular
            systems.
    """
    from ..exceptions import MultipleMolecularSystemsNeededError
    from molsysmt.basic import are_multiple_molecular_systems

    if not are_multiple_molecular_systems(molecular_systems):
        raise MultipleMolecularSystemsNeededError()
