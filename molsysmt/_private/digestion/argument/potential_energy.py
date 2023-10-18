from molsysmt._private.exceptions import ArgumentError
from molsysmt import pyunitwizard as puw
import numpy as np

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        'molsysmt.basic.iterator.__init__',
        'iterators.__init__',
        )

def digest_potential_energy(potential_energy, caller=None):
    """ Checks if potential_energy arguments has the correct type.

        Parameters
        ---------
        potential_energy: None, integer, list, tuple or ndarray
            The potential_energy argument.

        caller: str, optional
            Name of the function or method that is being digested.

        Returns
        -------
        ndarray
            The potential_energy with correct type

        Raises
        -------
        WrongStepError
            If potential_energy is not a valid argument.

    """

    if caller.endswith(functions_with_boolean):
        if isinstance(potential_energy, bool):
            return potential_energy

    value, unit = puw.get_value_and_unit(potential_energy)

    if not puw.check(unit, dimensionality={'[L]': 2, '[M]': 1, '[T]': -2, '[mol]': -1}):
        raise ArgumentError('potential_energy', value=coordinates, caller=caller, message=None)

    if isinstance(value, (int, np.int64, float, np.float64)):
        return puw.quantity(value, unit, standardized=True)

    raise ArgumentError('potential_energy', value=potential_energy, caller=caller, message=None)

