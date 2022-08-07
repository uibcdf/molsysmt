from molsysmt._private.exceptions import ArgumentError

def digest_molecular_systems(molecular_systems, caller=None):
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
        raise ArgumentError(molecular_systems, value=molecular_systems, caller=caller, message=None)

    return molecular_systems
