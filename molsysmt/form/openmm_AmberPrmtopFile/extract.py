from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='openmm.AmberPrmtopFile')
@dep_digest('openmm')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Extracting a subset of elements or structures from form openmm.AmberPrmtopFile.

    Parameters
    ----------
    item : openmm.AmberPrmtopFile
        Source item in openmm.AmberPrmtopFile form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    copy_if_all : object
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.AmberPrmtopFile
        Resulting object in openmm.AmberPrmtopFile form.

    .. versionadded:: 1.0.0
    """

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all:
            raise NotImplementedMethodError()
        else:
            tmp_item = item
    else:

        raise NotImplementedMethodError()

    return tmp_item

