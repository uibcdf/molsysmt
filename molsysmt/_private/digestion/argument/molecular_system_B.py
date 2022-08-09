from molsysmt._private.exceptions import ArgumentError

def digest_molecular_system_B(molecular_system_B, caller=None):
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
    from molsysmt.basic import is_a_molecular_system

    if not is_a_molecular_system(molecular_system_B):
        raise ArgumentError(molecular_system_B, value=molecular_system_B, caller=caller, message=None)

    return molecular_system_B

