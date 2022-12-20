from molsysmt._private.exceptions import ArgumentError
import numpy as np

def digest_structure_id(structure_id, caller=None):
    """ Checks if structure_id arguments has the correct type.

        Parameters
        ---------
        structure_id: None, integer, list, tuple or ndarray
            The structure_id argument.

        caller: str, optional
            Name of the function or method that is being digested.

        Returns
        -------
        ndarray
            The structure_id with correct type

        Raises
        -------
        WrongStepError
            If structure_id is not a valid argument.

    """
    if structure_id is None:
        return structure_id
    elif isinstance(structure_id, (int, np.int64)):
        return np.array([structure_id])
    elif isinstance(structure_id, (list, tuple)):
        return np.array(structure_id)
    elif isinstance(structure_id, np.ndarray):
        return structure_id

    type(structure_id)

    raise ArgumentError('structure_id', value=structure_id, caller=caller, message=None)

