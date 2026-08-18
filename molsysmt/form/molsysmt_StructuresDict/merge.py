from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(forms='molsysmt.StructuresDict')
def merge(items, atom_indices='all', structure_indices='all'):
    """
    Merging multiple items into a single item of form molsysmt.StructuresDict.


    Parameters
    ----------
    items : object
        Argument items.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.

    Returns
    -------
    molsysmt.StructuresDict
        Resulting object in molsysmt.StructuresDict form.


    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

