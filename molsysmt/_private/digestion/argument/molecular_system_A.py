from molsysmt._private.exceptions import ArgumentError

def digest_molecular_system_A(molecular_system_A, caller=None):
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

    if not is_molecular_system(molecular_system_A):
        raise ArgumentError(molecular_system_A, value=molecular_system_A, caller=caller, message=None)

    return molecular_system_A

