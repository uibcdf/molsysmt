from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='pdbfixer.PDBFixer')
def append_structures(item, structure_id=None, time=None, coordinates=None, box=None, skip_digestion=False):
    """
    Appending coordinate structures to an item of form pdbfixer.PDBFixer.

    Parameters
    ----------
    item : pdbfixer.PDBFixer
        Source item in pdbfixer.PDBFixer form.
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
    pdbfixer.PDBFixer
        Resulting object in pdbfixer.PDBFixer form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

