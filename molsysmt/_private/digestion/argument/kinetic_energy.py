from molsysmt._private.exceptions import ArgumentError
from molsysmt import pyunitwizard as puw
import numpy as np

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        'molsysmt.basic.iterator.__init__',
        'iterators.__init__',
        )

def digest_kinetic_energy(kinetic_energy, caller=None):
    """ Checks if kinetic_energy arguments has the correct type.

        Parameters
        ---------
        kinetic_energy: None, integer, list, tuple or ndarray
            The kinetic_energy argument.

        caller: str, optional
            Name of the function or method that is being digested.

        Returns
        -------
        ndarray
            The kinetic_energy with correct type

        Raises
        -------
        WrongStepError
            If kinetic_energy is not a valid argument.

    """

    if caller.endswith(functions_with_boolean):
        if isinstance(kinetic_energy, bool):
            return kinetic_energy

    value, unit = puw.get_value_and_unit(kinetic_energy)

    if not puw.check(unit, dimensionality={'[L]': 2, '[M]': 1, '[T]': -2, '[mol]': -1}):
        raise ArgumentError('kinetic_energy', value=coordinates, caller=caller, message=None)

    if isinstance(value, (int, np.int64, float, np.float64)):
        return puw.quantity(value, unit, standardized=True)

    raise ArgumentError('kinetic_energy', value=kinetic_energy, caller=caller, message=None)

