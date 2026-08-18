from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_id')
def append_structures(item, structure_id=None, time=None, coordinates=None, box=None, skip_digestion=False):
    """
    Appending coordinate structures to an item of form string:pdb_id.

    Parameters
    ----------
    item : string:pdb_id
        Source item in string:pdb_id form.
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
    string:pdb_id
        Resulting object in string:pdb_id form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

