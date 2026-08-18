from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='openff.Topology')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True,
            skip_digestion=False):
    """
    Extracting a subset of atoms or structures from form openff.Topology.

    Parameters
    ----------
    item : openff.Topology
        Source item.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices to extract.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openff.Topology
        Extracted subset in the same form.
    """

    if is_all(atom_indices) and is_all(structure_indices):
        from copy import deepcopy
        return deepcopy(item)
    else:
        raise NotImplementedMethodError()
