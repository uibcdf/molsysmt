from molsysmt._private.exceptions import ArgumentError

def digest_reference_molecular_system(reference_molecular_system, caller=None):
    """ Check if an object is a molecular system.

        Parameters
        ----------
        reference_molecular_system : Any
            The molecular system object to be checked.
        caller: str, optional
            Name of the function or method that is being digested.

        Returns
        -------
        reference_molecular_system : Any
            The molecular system object.

        Raises
        ------
        MolecularSystemNeededError
            If the given object is not a molecular system.
    """
    from molsysmt.basic import is_a_molecular_system, are_multiple_molecular_systems

    if caller=='molsysmt.basic.view.view':
        if is_a_molecular_system(reference_molecular_system):
            return reference_molecular_system
        elif are_multiple_molecular_systems(reference_molecular_system):
            return reference_molecular_system

    if is_a_molecular_system(reference_molecular_system):
        return reference_molecular_system

    raise ArgumentError('reference_molecular_system', value=reference_molecular_system, caller=caller, message=None)

