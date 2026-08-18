from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import StructuralInconsistencyError, InternalAlgorithmError, FormatError
from molsysmt import pyunitwizard as puw
import numpy as np

@arg_digest()
def get_box_with_shape(shape='cubic', length='1 nm', n_structures=1, skip_digestion=False):
    """
    Constructing a box matrix for a given shape.


    Parameters
    ----------
    shape : object, default='cubic'
        Argument shape.
    length : object, default='1 nm'
        Argument length.
    n_structures : object, default=1
        Argument n_structures.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    quantity
        Box array of shape `(n_structures, 3, 3)` in the specified length units.


    .. versionadded:: 1.0.0
    """

    length_value, length_unit = puw.get_value_and_unit(length)

    match shape:

        case 'cubic':

            box = np.eye(3, dtype=np.float64)

        case 'truncated octahedral':

            box = np.array([[1.0, 0.0, 0.0],
                            [1.0/3.0, 2.0*np.sqrt(2.0)/3.0, 0.0],
                            [-1.0/3.0, np.sqrt(2.0)/3.0, np.sqrt(6.0)/3.0]],
                          dtype=np.float64)

        case 'rhombic dodecahedral':

            box = np.array([[1.0, 0.0, 0.0],
                            [0.0, 1.0, 0.0],
                            [0.5, 0.5, np.sqrt(2)/2]],
                           dtype=np.float64)

        case _:

            raise InternalAlgorithmError("Unexpected empty state", caller="molsysmt.pbc.get_box_with_shape")
    box = np.reshape(box, (1,3,3))
    box = length_value * box
    box = np.repeat(box, repeats=n_structures, axis=0)
    box = puw.quantity(box, length_unit)
    box = puw.standardize(box)

    return box
