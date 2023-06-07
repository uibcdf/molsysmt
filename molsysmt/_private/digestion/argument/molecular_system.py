from molsysmt._private.exceptions import ArgumentError
from pathlib import PosixPath

def digest_molecular_system(molecular_system, caller=None):
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
    from molsysmt.basic import is_a_molecular_system, are_multiple_molecular_systems

    if isinstance(molecular_system, PosixPath):
        molecular_system = molecular_system.absolute().__str__()

    if isinstance(molecular_system, (list,tuple)):
        for ii in range(len(molecular_system)):
            if isinstance(molecular_system[ii], PosixPath):
                molecular_system[ii] = molecular_system[ii].absolute().__str__()

    if caller=='molsysmt.basic.view.view':
        if is_a_molecular_system(molecular_system):
            return molecular_system
        elif are_multiple_molecular_systems(molecular_system):
            return molecular_system

    if is_a_molecular_system(molecular_system):
        return molecular_system

    raise ArgumentError('molecular_system', value=molecular_system, caller=caller, message=None)

