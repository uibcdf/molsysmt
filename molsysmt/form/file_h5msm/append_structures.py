from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:h5msm')
def append_structures(item, structure_id=None, time=None, coordinates=None, box=None, skip_digestion=False):
    """
    Appending coordinate structures to an item of form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
    structure_id : object
        Structure identifiers.
    time : numpy.ndarray or quantity
        Simulation time coordinates in picoseconds.
    coordinates : numpy.ndarray or quantity
        Cartesian coordinate array in nanometers.
    box : numpy.ndarray or quantity
        Simulation box vectors in nanometers.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:h5msm
        Resulting object in file:h5msm form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

